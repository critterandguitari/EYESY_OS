import subprocess
import threading
import time
import pygame
from screen import Screen
from menu import Menu, MenuItem

def list_wifi_ssids():
    try:
        result = subprocess.run(
            ["nmcli", "-t", "-f", "SSID", "dev", "wifi"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        ssids = {ssid.strip() for ssid in result.stdout.splitlines() if ssid.strip()}
        return sorted(ssids)
    except subprocess.CalledProcessError as e:
        print(f"Error listing WiFi networks: {e}")
        return []
    except subprocess.TimeoutExpired:
        print("Timed out waiting for nmcli to list networks")
        return []

def get_current_network():
    try:
        result = subprocess.run(
            ["nmcli", "-t", "-f", "ACTIVE,SSID", "dev", "wifi"],
            capture_output=True,
            text=True,
            check=True
        )

        for line in result.stdout.splitlines():
            line = line.strip()
            if line.startswith("yes:"):
                ssid = line.split(":", 1)[1]
                return ssid
        return "Not Connected"
    except subprocess.CalledProcessError as e:
        print(f"Error getting current network: {e}")
        return "Not Connected"

def is_connected():
    try:
        result = subprocess.run(
            ["nmcli", "-t", "-f", "ACTIVE", "dev", "wifi"],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.splitlines():
            if line.strip() == "yes":
                return True
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error checking connection status: {e}")
        return False

def disconnect_wifi(device='wlan0'):
    try:
        subprocess.run(["sudo", "nmcli", "device", "disconnect", device], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error disconnecting WiFi: {e}")

def connect(ssid, device='wlan0'):
    try:
        subprocess.run(["sudo", "nmcli", "device", "wifi", "connect", ssid], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error connecting to {ssid}: {e}")

class SSIDMenu(Screen):
    def __init__(self, app_state):
        super().__init__(app_state)
        self.menu = Menu(app_state, [])
        self.ssids = []
        self.connected = False
        # States: "init", "scanning", "idle", "connecting", "disconnecting"
        self.state = "init"  
        self.current_ssid = "Not Connected"
        self.target_ssid = None  # SSID we attempt to connect to

    def before(self):
        # Called once when the screen is displayed
        #self.connected = is_connected()
        #self.current_ssid = get_current_network()
        # re get info only if we are in idle state 
        if self.state == "idle":
            # Check if connected
            self.connected = is_connected()
            self.current_ssid = get_current_network()
            if self.connected:
                # Build menu for connected state
                self.build_connected_menu()
                self.state = "idle"
            else:
                # Not connected, start scanning
                self.start_scanning()
                self.state = "scanning"

    def handle_events(self):
        # Only handle events if idle
        if self.state == "idle":
            self.menu.handle_events()

    def render(self, surface):
        font = self.menu.font

        pygame.draw.rect(surface, (0,0,0), (20, 20, 600, 440))
        # State machine: decide what to do or show based on current state
        if self.state == "init":
            # Check if connected
            self.connected = is_connected()
            self.current_ssid = get_current_network()
            if self.connected:
                # Build menu for connected state
                self.build_connected_menu()
                self.state = "idle"
            else:
                # Not connected, start scanning
                self.start_scanning()
                self.state = "scanning"

        elif self.state == "scanning":
            # Show scanning message
            message = "Looking for networks..."
            rendered_text = font.render(message, True, (255, 255, 255))
            surface.blit(rendered_text, (50, 280))
            # The scanning thread will update self.state to "idle" when done

        elif self.state == "connecting":
            # Show connecting message
            message = f"Connecting to {self.target_ssid}..."
            rendered_text = font.render(message, True, (255, 255, 255))
            surface.blit(rendered_text, (50, 280))
            # The connecting thread will set state to "idle" after done

        elif self.state == "disconnecting":
            # Show disconnecting message
            message = "Disconnecting..."
            rendered_text = font.render(message, True, (255, 255, 255))
            surface.blit(rendered_text, (50, 280))
            # The disconnecting thread will set state to "idle" after done

        elif self.state == "idle":
            # Render the menu and current network status
            self.menu.render(surface)
            message = f"Connected to: {self.current_ssid}"
            rendered_text = font.render(message, True, (255, 255, 255))
            surface.blit(rendered_text, (50, 280))

    def build_connected_menu(self):
        self.menu.items = [
            MenuItem('Disconnect', self.disconnect_callback),
            MenuItem('< Exit', self.exit_menu)
        ]
        self.menu.set_selected_index(0)

    def build_not_connected_menu(self):
        # Insert SSIDs plus Exit
        self.menu.items = [MenuItem('< Exit', self.exit_menu)]
        for ssid in self.ssids:
            self.menu.items.insert(-1, MenuItem(ssid, self.select_ssid_callback(ssid)))
        self.menu.set_selected_index(0)

    def start_scanning(self):
        def do_scan():
            ssids = list_wifi_ssids()
            self.ssids = ssids
            self.connected = is_connected()
            self.current_ssid = get_current_network()

            # Once done, decide what menu to show
            if self.connected:
                self.build_connected_menu()
            else:
                self.build_not_connected_menu()

            self.state = "idle"

        threading.Thread(target=do_scan, daemon=True).start()

    def disconnect_callback(self):
        # Disconnect in a thread
        def do_disconnect():
            print("disconnecting")
            disconnect_wifi()
            time.sleep(1)
            self.current_ssid = "Not Connected"
            self.ssids = []  # clear old ssids
            print("disconnected")
            self.state = "init"

        self.state = "disconnecting"
        threading.Thread(target=do_disconnect, daemon=True).start()

    def connect_callback(self, ssid):
        self.target_ssid = ssid

        def do_connect():
            connect(ssid)
            time.sleep(1)
            self.connected = is_connected()
            self.current_ssid = get_current_network()
            if self.connected:
                self.build_connected_menu()
            else:
                # Maybe connection failed, rebuild not connected menu
                # Potentially re-scan or show old ssids
                self.build_not_connected_menu()
            self.state = "idle"
            self.target_ssid = None

        self.state = "connecting"
        threading.Thread(target=do_connect, daemon=True).start()

    def select_ssid_callback(self, ssid):
        def callback():
            self.connect_callback(ssid)
        return callback

    def exit_menu(self):
        self.app_state.switch_menu_screen("home")

