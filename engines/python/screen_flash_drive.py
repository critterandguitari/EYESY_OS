import threading
import subprocess
import os
import shutil
import pygame
from screen import Screen
from widget_menu import WidgetMenu, MenuItem

class ScreenFlashDrive(Screen):
    def __init__(self, eyesy):
        super().__init__(eyesy)
        self.state = "idle"  # "idle" or "running"
        self.title = "Manage USB Drive"
        self.footer = chr(0x2680) + "     = Cancel     " + chr(0x2682) + "   = Up/Down     " + chr(0x2683) + "  = Enter"

        self.menu = WidgetMenu(eyesy, [
            MenuItem('Backup SD card to USB drive', self.start_backup),
            MenuItem('Eject USB drive', self.eject),
            MenuItem('Reload', self.restart),
            MenuItem('◀  Exit', self.goto_home)
        ])
        self.menu.off_y = 43
        self.font = pygame.font.Font("font.ttf", 16)
        self.font_small = pygame.font.Font("font.ttf", 12)
        self.logs = []

    def before(self):
        self.menu.selected_index = 3
        self.logs = []
        self.ensure_usb_mounted()
        pass

    def after(self):
        pass

    def handle_events(self):
        if self.state == "idle":
            self.menu.handle_events()

    def render(self, surface):     

        #msg_xy = (32, 68)
        #color = (200, 200, 200)
        #message = "Backup Modes, Scenes, Settings, and Screen Grabs?"
        #rendered_text = self.font.render(message, True, color)
        #surface.blit(rendered_text, msg_xy)
        self.menu.render(surface)

        line_height = self.font_small.get_linesize()
        for i, log in enumerate(self.logs[-10:]):  # Show last 10 log entries
            text_surface = self.font_small.render(log, True, (200, 200, 200))  # White text
            surface.blit(text_surface, (32, 200 + i * line_height))

    def restart(self):
        self.eyesy.restart = True
 
    def eject(self):
        self.logs = []  # Clear previous logs
        self.log("Ejecting USB drive...")
        subprocess.run(["sudo", "umount", "/usbdrive"])
        self.log("Safe to remove.")

   
    def log(self, message):
        """Append a message to logs and trigger a screen update."""
        self.logs.append(message)

    def start_backup(self):
        """Start the backup process in a separate thread."""
        if self.state == "running":
            return  # Prevent multiple backups from running at once

        self.logs = []  # Clear previous logs
        self.state = "running"
        self.log("Starting backup...")

        backup_thread = threading.Thread(target=self.backup, daemon=True)
        backup_thread.start()

    def backup(self):
        """Performs the backup process in a separate thread."""
        if not self.ensure_usb_mounted():
            self.log("USB drive not found or failed to mount.")
            self.state = "idle"
            return

        backup_folder = self.create_backup_folder()
        if not backup_folder:
            self.log("Failed to create backup folder.")
            self.state = "idle"
            return

        self.copy_directories(backup_folder)

        self.log("Syncing drive...")
        subprocess.run(["sync"])

        #self.log("Unmounting drive...")
        #subprocess.run(["sudo", "umount", "/usbdrive"])

        self.log("Backup complete.")
        self.state = "idle"

    def ensure_usb_mounted(self):
        """Ensure the USB drive is mounted."""
        usb_device = self.get_usb_device()
        if not usb_device:
            self.log("No USB device found.")
            return False

        if not os.path.exists("/usbdrive"):
            self.log("mount point /usbdrive not found on system")
            return False

        if "/usbdrive" in subprocess.getoutput("mount"):
            self.log("USB mounted mounted.")
            if self.eyesy.running_from_usb : self.log("EYESY running patches from USB")
            return True

        result = subprocess.run(["sudo", "mount", "-o", "uid=1000,gid=1000", usb_device, "/usbdrive"],
                                capture_output=True, text=True)
        if result.returncode == 0:
            self.log(f"Mounted {usb_device} at /usbdrive.")
            return True
        else:
            self.log(f"Mount failed: {result.stderr}")
            return False

    def get_usb_device(self):
        """Find the first USB storage device."""
        devices = subprocess.getoutput("lsblk -o KNAME,TYPE | grep 'disk' | awk '{print $1}'").splitlines()
        for dev in devices:
            if "sd" in dev:  # Typical USB storage devices start with "sd"
                return f"/dev/{dev}1"  # Assuming first partition
        return None

    def create_backup_folder(self):
        """Create the next numbered backup folder."""
        backup_path = "/usbdrive/backups"
        if not os.path.exists(backup_path):
            self.log(f"Creating folder for backups")
            try:
                os.makedirs(backup_path)
                return backup_folder
            except Exception as e:
                self.log(f"Error creating backup folder: {e}")
                return None

        existing_folders = [
            int(f) for f in os.listdir(backup_path)
            if f.isdigit() and len(f) == 4
        ]
        next_number = max(existing_folders, default=0) + 1
        backup_folder = os.path.join(backup_path, f"{next_number:04d}")

        try:
            os.makedirs(backup_folder)
            self.log(f"Created backup folder: {backup_folder}")
            return backup_folder
        except Exception as e:
            self.log(f"Error creating backup folder: {e}")
            return None

    def copy_directories(self, dest_folder):
        """Copy the four directories to the backup folder."""
        paths = {
            "Grabs": "/sdcard/Grabs/",
            "Modes": "/sdcard/Modes/",
            "Scenes": "/sdcard/Scenes/",
            "System": "/sdcard/System/"
        }

        for name, src in paths.items():
            if os.path.exists(src):
                dest = os.path.join(dest_folder, name)
                try:
                    shutil.copytree(src, dest)
                    self.log(f"Copied {name} to backup.")
                except Exception as e:
                    self.log(f"Error copying {name}: {e}")
            else:
                self.log(f"Skipping {name}, does not exist.")

    def goto_home(self):
        self.eyesy.switch_menu_screen("home")

