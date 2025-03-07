import subprocess
import threading
import time
import re
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
        # Run iwconfig and capture the output
        result = subprocess.run(
            ["iwconfig"],
            capture_output=True,
            text=True,
            check=True
        )
        # Search for the ESSID in the output
        for line in result.stdout.splitlines():
            if "ESSID" in line:
                essid = line.split("ESSID:")[-1].strip().strip('"')
                if essid and essid != "off/any":
                    return essid
        return "Not Connected"
    except subprocess.CalledProcessError as e:
        print(f"Error getting current network: {e}")
        return "Not Connected"

def is_connected():
    try:
        # Run iwconfig and capture the output
        result = subprocess.run(
            ["iwconfig"],
            capture_output=True,
            text=True,
            check=True
        )
        # Search for ESSID and check if connected
        for line in result.stdout.splitlines():
            if "ESSID" in line:
                essid = line.split("ESSID:")[-1].strip().strip('"')
                if essid and essid != "off/any":
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

def get_local_ip_ifconfig():
    try:
        # Run the `ifconfig` command and get the output
        result = subprocess.run(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise Exception(result.stderr.strip())

        # Extract IP addresses using a regex (looks for IPv4 addresses)
        ip_pattern = re.compile(r'inet\s+(\d+\.\d+\.\d+\.\d+)')
        ips = ip_pattern.findall(result.stdout)

        # Exclude 127.0.0.1 (loopback) and return the first match
        for ip in ips:
            if ip != '127.0.0.1':
                return ip
        return "Not Connected"
    except Exception as e:
        return f"Error: {e}"

def wifi_adapter_found():
    try:
        output = subprocess.check_output(["nmcli", "device"], text=True)
        return any("wifi" in line for line in output.splitlines())
    except subprocess.CalledProcessError:
        return False  # nmcli failed, assume no adapter

class ScreenWiFi(Screen):

    def __init__(self, eyesy):
        super().__init__(eyesy)
        self.title = "WiFi Setup"
        self.footer =  chr(0x2680) + "     = Cancel     " + chr(0x2682) + "   = Up/Down     " + chr(0x2683) + "  = Enter"
        self.footer =  chr(0x2680) + "     = Cancel     "+ chr(0x2681) +"   = Right/Left     "  + chr(0x2682) + "   = Up/Down     " + chr(0x2683) + "  = Enter"
        self.menu = WidgetMenu(eyesy, [])
        self.ssids = []
        self.connected = False
        self.state = "init"  
        self.current_ssid = "Not Connected"
        self.target_ssid = None
        self.connection_error = None
        self.pending_password = None
        self.keyboard = None  # Will hold the KeyboardScreen instance when needed
        self.netlogs = WidgetNetlogs(eyesy)
        self.netlogs.x_offset = 50
        self.netlogs.y_offset = 260
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
                if wifi_adapter_found():
                    self.start_scanning()
                    self.state = "scanning"
                else:
                    self.build_nowifi_menu()
                    self.state = "nowifi"

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
            message = f"Connected to: {self.current_ssid}" + "            IP: " + self.eyesy.ip
            rendered_text = font.render(message, True, color)
            surface.blit(rendered_text, msg_xy)

        elif self.state == "select_net":
            self.menu.render(surface)
            message = f"Select WiFi Network"
            rendered_text = font.render(message, True, color)
            surface.blit(rendered_text, msg_xy)

        elif self.state == "nowifi":
            self.menu.render(surface)
            message = f"WiFi Adapter Not Found" + "            IP: " + self.eyesy.ip
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
        if self.state == "idle" or self.state == "select_net" or self.state == "nowifi":
            self.menu.handle_events()

    def build_nowifi_menu(self):
        self.menu.items = [
            MenuItem('◀  Exit', self.exit_menu)
        ]
        self.menu.set_selected_index(0)
        self.eyesy.ip = get_local_ip_ifconfig()

    def build_connected_menu(self):
        self.menu.items = [
            MenuItem('Disconnect', self.disconnect_confirm_callback),
            MenuItem('◀  Exit', self.exit_menu)
        ]
        self.menu.set_selected_index(1)
        self.eyesy.ip = get_local_ip_ifconfig()

    def build_not_connected_menu(self):
        # Insert SSIDs plus Exit
        self.menu.items = [MenuItem('◀  Exit', self.exit_menu)]
        for ssid in self.ssids:
            self.menu.items.insert(-1, MenuItem(ssid, self.select_ssid_callback(ssid)))
        self.menu.set_selected_index(0)
        self.eyesy.ip = get_local_ip_ifconfig()

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
        self.keyboard = WidgetKeyboard(self.eyesy, connect_callback=self.password_entered_callback, cancel_callback=self.password_cancel_callback)
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
        self.eyesy.switch_menu_screen("home")

