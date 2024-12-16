from screen import Screen
from menu import Menu, MenuItem
import subprocess
import re


def list_wifi_ssids():
    try:
        # Run nmcli command to list WiFi SSIDs
        result = subprocess.run(
            ["nmcli", "-t", "-f", "SSID", "dev", "wifi"],
            capture_output=True,
            text=True,
            check=True
        )
        # Filter out empty lines and duplicates
        ssids = {ssid.strip() for ssid in result.stdout.splitlines() if ssid.strip()}
        return sorted(ssids)
    except subprocess.CalledProcessError as e:
        print(f"Error listing WiFi networks: {e}")
        return []

class SSIDMenu(Screen):
    def __init__(self, app_state):
        super().__init__(app_state)
        self.menu = Menu(app_state, [
            MenuItem('< Exit', self.exit_menu)
        ])

    def handle_events(self):
        self.menu.handle_events()
        # Handle other keys if needed

    def update(self):
        pass  # Update logic if needed

    def before(self):
        # Fetch SSIDs
        ssids = list_wifi_ssids()
        
        # Clear existing menu items except the exit option
        self.menu.items = [item for item in self.menu.items if item.text == '< Exit>']
        
        # Add menu items for each SSID
        for ssid in ssids:
            self.menu.items.insert(-1, MenuItem(ssid, self.select_ssid_callback(ssid)))

    def render(self, surface):
        self.menu.render(surface)

    def exit_menu(self):
        self.app_state.switch_menu_screen("home")

    def select_ssid_callback(self, ssid):
        # Return a callback that sets the selected SSID
        def callback():
            self.app_state.selected_ssid = ssid
            print(f"Selected SSID: {ssid}")  # Debug print
            # Optionally, switch screen or perform other actions
        return callback

