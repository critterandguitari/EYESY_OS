from screen import Screen
from menu import Menu, MenuItem
import subprocess
import threading
import pygame

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
        self.ssids_fetched = False
        self.loading = False  # Flag to indicate if we're currently fetching SSIDs
        self.ssids = []

    def handle_events(self):
        self.menu.handle_events()

    def update(self):
        pass

    def before(self):
        # Instead of fetching SSIDs here (which blocks), just mark that we need to fetch them
        self.ssids_fetched = False
        self.ssids = []
        self.loading = True

        # Clear existing menu items except the exit option
        self.menu.items = [item for item in self.menu.items if item.text == '< Exit']

    def render(self, surface):
        # If we haven't fetched SSIDs yet, display a loading message
        if not self.ssids_fetched:
            pygame.draw.rect(surface, (0,0,0), (20, 20, 440, 440))
            if self.loading:
                # Show loading message
                # For simplicity, just render text directly with your menu's font or a separate method
                font = self.menu.font
                loading_text = font.render("Looking for networks...", True, (255, 255, 255))
                surface.blit(loading_text, (50, 50))
                
                # Fetch SSIDs in a separate thread to avoid blocking
                self.loading = False
                threading.Thread(target=self.fetch_ssids).start()
            else:
                # While waiting for the thread, just keep showing loading message
                font = self.menu.font
                loading_text = font.render("Looking for networks...", True, (255, 255, 255))
                surface.blit(loading_text, (50, 50))
        else:
            # SSIDs are fetched, render the menu
            self.menu.render(surface)

    def fetch_ssids(self):
        # Run list_wifi_ssids in a thread
        self.ssids = list_wifi_ssids()

        # Insert menu items for each SSID
        for ssid in self.ssids:
            self.menu.items.insert(-1, MenuItem(ssid, self.select_ssid_callback(ssid)))

        self.ssids_fetched = True

    def exit_menu(self):
        self.app_state.switch_menu_screen("home")

    def select_ssid_callback(self, ssid):
        def callback():
            self.app_state.selected_ssid = ssid
            print(f"Selected SSID: {ssid}")
            # You may want to switch screens or perform another action here.
        return callback

