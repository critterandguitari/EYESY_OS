import os
import shutil

# Define source directories
GRABS_PATH = "/sdcard/Grabs/"
MODES_PATH = "/sdcard/Modes/"
SCENES_PATH = "/sdcard/Scenes/"
SYSTEM_PATH = "/sdcard/System/"
SOURCE_DIRS = [GRABS_PATH, MODES_PATH, SCENES_PATH, SYSTEM_PATH]

# Define backup location
USB_BACKUP_PATH = "/usbdrive/Backups"

def ensure_backup_dir():
    """Ensure the /usbdrive/backups directory exists."""
    if not os.path.exists(USB_BACKUP_PATH):
        os.makedirs(USB_BACKUP_PATH)

def get_next_backup_folder():
    """Find the highest 4-digit numbered folder in /usbdrive/backups and return the next one."""
    existing_folders = [
        int(f) for f in os.listdir(USB_BACKUP_PATH) 
        if f.isdigit() and len(f) == 4
    ]
    next_number = max(existing_folders, default=0) + 1
    return os.path.join(USB_BACKUP_PATH, f"{next_number:04d}")

def copy_directories(dest_folder):
    """Copy each directory into the backup folder."""
    os.makedirs(dest_folder, exist_ok=True)
    for src in SOURCE_DIRS:
        if os.path.exists(src):
            dest = os.path.join(dest_folder, os.path.basename(src.rstrip('/')))
            shutil.copytree(src, dest)
            print(f"Copied {src} to {dest}")
        else:
            print(f"Skipping {src}, does not exist.")

if __name__ == "__main__":
    ensure_backup_dir()
    backup_folder = get_next_backup_folder()
    copy_directories(backup_folder)
    print(f"Backup completed at {backup_folder}")

