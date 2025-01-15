import subprocess
import threading
import time
import pygame
from screen import Screen
from widget_menu import WidgetMenu, MenuItem
from widget_netlogs import WidgetNetlogs
from widget_keyboard import WidgetKeyboard

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

def connect_pw(ssid, device='wlan0', password=''):
    cmd = ["sudo", "nmcli", "device", "wifi", "connect", ssid, "password", password]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # If we reach here, the command succeeded
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        # Command failed
        error_output = e.stderr if e.stderr else e.stdout
        print(f"Error connecting to {ssid}: {error_output}")
        return False, error_output

def connect(ssid, device='wlan0'):
    cmd = ["sudo", "nmcli", "device", "wifi", "connect", ssid]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # If we reach here, the command succeeded
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        # Command failed
        error_output = e.stderr if e.stderr else e.stdout
        print(f"Error connecting to {ssid}: {error_output}")
        return False, error_output

class ScreenWiFi(Screen):

    def __init__(self, app_state):
        super().__init__(app_state)
        self.title = "WiFi Setup"
        self.menu = WidgetMenu(app_state, [])
        self.ssids = []
        self.connected = False
        self.state = "init"  
        self.current_ssid = "Not Connected"
        self.target_ssid = None
        self.connection_error = None
        self.pending_password = None
        self.keyboard = None  # Will hold the KeyboardScreen instance when needed
        self.netlogs = WidgetNetlogs(app_state)
        self.netlogs.x_offset = 50
        self.netlogs.y_offset = 300
        self.menu.off_y = 75

    def before(self):
        
        #self.netlogs.before()
        # return state to init unless there is an operation happening
        if self.state not in {"scanning", "connecting", "disconnecting"} : self.state = "init"

    def render(self, surface):
        
        font = self.menu.font
        color = (200, 200, 200)
        # If we are in enter_password state, just render the keyboard
        if self.state == "enter_password":
            # Let the keyboard handle its own rendering
            message = f"Enter password for {self.target_ssid}"
            msg_xy = (32, 68)
            rendered_text = font.render(message, True, color)
            surface.blit(rendered_text, msg_xy)
            self.keyboard.render(surface)
            return

        # otherwise we show the netlogs
        message = "Logs"
        msg_xy = (32, 275)
        rendered_text = font.render(message, True, color)
        surface.blit(rendered_text, msg_xy)
        self.netlogs.render(surface)

        # then show stuff depeinding on state
        msg_xy = (32, 68)
        if self.state == "init":
            self.connected = is_connected()
            self.current_ssid = get_current_network()
            if self.connected:
                self.build_connected_menu()
                self.state = "idle"
            else:
                self.start_scanning()
                self.state = "scanning"

        elif self.state == "scanning":
            message = "Looking for networks..."
            rendered_text = font.render(message, True, color)
            surface.blit(rendered_text, msg_xy)

        elif self.state == "connecting":
            message = f"Connecting to {self.target_ssid}..."
            rendered_text = font.render(message, True, color)
            surface.blit(rendered_text, msg_xy)

        elif self.state == "disconnecting":
            message = "Disconnecting..."
            rendered_text = font.render(message, True, color)
            surface.blit(rendered_text, msg_xy)

        elif self.state == "idle":
            self.menu.render(surface)
            message = f"Connected to: {self.current_ssid}"
            rendered_text = font.render(message, True, color)
            surface.blit(rendered_text, msg_xy)

        elif self.state == "select_net":
            self.menu.render(surface)
            message = f"Select WiFi Network"
            rendered_text = font.render(message, True, color)
            surface.blit(rendered_text, msg_xy)

        elif self.state == "dialog":
            self.menu.render(surface)
            message = f"Disconnect from: {self.current_ssid}?"
            rendered_text = font.render(message, True, color)
            surface.blit(rendered_text, msg_xy)

    def handle_events(self):
        # If we are in enter_password state, just let the keyboard handle events
        if self.state == "enter_password":
            self.keyboard.handle_events()
            return
        
        # same if dialog
        if self.state == "dialog":
            self.menu.handle_events()
            return

        # otherwise seclect from menu, but not during an action
        if self.state == "idle" or self.state == "select_net":
            self.menu.handle_events_speeder()

    def build_connected_menu(self):
        self.menu.items = [
            MenuItem('Disconnect', self.disconnect_confirm_callback),
            MenuItem('◀  Exit', self.exit_menu)
        ]
        self.menu.set_selected_index(1)

    def build_not_connected_menu(self):
        # Insert SSIDs plus Exit
        self.menu.items = [MenuItem('◀  Exit', self.exit_menu)]
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
                self.state = "idle"
            else:
                self.build_not_connected_menu()
                self.state = "select_net"


        threading.Thread(target=do_scan, daemon=True).start()

    def disconnect_confirm_callback(self):

        self.menu.items = [
            MenuItem('Yes', self.disconnect_callback),
            MenuItem('◀  Cancel', self.disconnect_confirm_no)
        ]
        self.menu.set_selected_index(1)
        self.state = "dialog"
   
    def disconnect_confirm_no(self):
        self.state = "init"

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
        self.state = "connecting"

        def do_connect():
            success, output = connect(ssid)
            print("connection status: " + output)
            if not success:
                print("enabling keyboard")
                self.request_password()
                return
                # Check if the error indicates a password is needed
                #error_output = str(error)
                # This is just an example check. Actual nmcli errors may differ.
                # Common errors might mention "No suitable security found" or "secrets were required"
                #if "secrets were required" in error_output or "No suitable connection" in error_output:
                    # Show the keyboard screen to enter password
                #    self.request_password()
                #    return
                #else:
                    # Some other error: just rebuild not connected menu
                #    self.build_not_connected_menu()
                #    self.state = "idle"
                #    self.target_ssid = None
                #    return

            # If no error, we are connected now
            time.sleep(1)
            self.state = "init"
            self.target_ssid = None

        threading.Thread(target=do_connect, daemon=True).start()

    def request_password(self):
        # Create the keyboard screen, passing a callback that will be called when password is entered
        self.keyboard = WidgetKeyboard(self.app_state, connect_callback=self.password_entered_callback, cancel_callback=self.password_cancel_callback)
        self.state = "enter_password"

    def password_cancel_callback(self):
        self.state = "init"

    def password_entered_callback(self, password):
        # Password entered by user in KeyboardScreen
        # Now attempt connecting again with the password
        self.state = "connecting"

        def do_password_connect():
            success, output = connect_pw(self.target_ssid, password=password)
            # Destroy keyboard reference
            self.keyboard = None

            if not success:
                # If still error, then just show not connected menu
                self.build_not_connected_menu()
                self.state = "select_net"
                self.target_ssid = None
                print("some pw connect error")
                return

            print("sucess connecting")
            time.sleep(1)
            self.state = "init"
            self.target_ssid = None

        threading.Thread(target=do_password_connect, daemon=True).start()

    def select_ssid_callback(self, ssid):
        def callback():
            self.connect_callback(ssid)
        return callback

    def exit_menu(self):
        self.app_state.switch_menu_screen("home")

