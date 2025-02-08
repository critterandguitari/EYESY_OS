import subprocess
import re
from screen import Screen
from widget_menu import WidgetMenu, MenuItem


CMDLINE_PATH = "/boot/firmware/cmdline.txt"
TV_NORM_PREFIX = "vc4.tv_norm="

def get_tv_norm():
    # Extract the current tv_norm value from cmdline.txt.
    try:
        with open(CMDLINE_PATH, "r") as f:
            match = re.search(rf"{TV_NORM_PREFIX}(\S+)", f.read())
            if match:
                return match.group(1)  # Return value after vc4.tv_norm=
    except FileNotFoundError:
        pass
    return "NTSC"  # Default if not found (though we assume it's always there)

def set_tv_norm(mode):
    # Replace the existing vc4.tv_norm= value with a new mode in cmdline.txt.
    try:
        subprocess.run(
            f"sudo sed -i 's/{TV_NORM_PREFIX}\\S\\+/{TV_NORM_PREFIX}{mode}/' {CMDLINE_PATH}",
            shell=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error modifying {CMDLINE_PATH}: {e}")


class ScreenVideoSettings(Screen):
    def __init__(self, eyesy):
        super().__init__(eyesy)
        self.state = "idle" 
        self.title = "Video Settings"
        self.footer =  chr(0x2680) + "     = Cancel     " + chr(0x2682) + "   = Up/Down     " + chr(0x2683) + "  = Enter"
        self.new_video_res = 0

        self.menu = WidgetMenu(eyesy, [
            MenuItem('HDMI Resolution  ▶', self.select_res),
            MenuItem('Composite Video Settings  ▶', self.select_compvid),
            MenuItem('◀  Exit', self.goto_home)
        ])
        self.menu.off_y = 43
        
        self.menu_select_res = WidgetMenu(
            eyesy,
            [MenuItem(res["name"], self.select_res_callback(i)) for i, res in enumerate(self.eyesy.RESOLUTIONS)] 
            + [MenuItem('◀  Exit', self.goto_home)]
        )
        
        self.menu_select_res.off_y = 75
        
        self.menu_select_compvid = WidgetMenu(
            eyesy,
            [MenuItem(res, self.select_compvid_callback(res)) for i, res in enumerate(self.eyesy.COMPVIDS)] 
            + [MenuItem('◀  Exit', self.goto_home)]
        )
        
        self.menu_select_compvid.off_y = 75
        self.menu_select_compvid.visible_items  = 12
         
        self.menu_confirm_res = WidgetMenu(eyesy, [
            MenuItem('Yes', self.confirm_res),
            MenuItem('◀  Cancel', self.goto_home)
        ])
        self.menu_confirm_res.off_y = 75
        
        self.current_compvid = ""

    def before(self):
        self.menu_select_res.set_selected_index(self.eyesy.config["video_resolution"])
        self.menu_select_compvid.set_selected_index(len(self.menu_select_compvid.items) - 1)
        self.menu_confirm_res.set_selected_index(1)
        self.current_compvid = get_tv_norm()
        self.state = "idle"

    def after(self):
        pass

    def handle_events(self):
        if self.state == "idle":
            self.menu.handle_events()
        elif self.state == "select_res":
            self.menu_select_res.handle_events()
        elif self.state == "select_compvid":
            self.menu_select_compvid.handle_events()
        elif self.state == "confirm_res":
            self.menu_confirm_res.handle_events()

    def render(self, surface):

        msg_xy = (32, 68)
        font = self.menu.font
        color = (200, 200, 200)
        if self.state == "idle":
            self.menu.render(surface)
        elif self.state == "select_res" :
            reso = self.eyesy.RESOLUTIONS[self.eyesy.config["video_resolution"]]["name"]
            message = f"Select resolution for HDMI. Currently {reso} "
            rendered_text = font.render(message, True, color)
            surface.blit(rendered_text, msg_xy)
            self.menu_select_res.render(surface)
        elif self.state == "select_compvid" :
            message = f"Select composite video format. Currently {self.current_compvid}"
            rendered_text = font.render(message, True, color)
            surface.blit(rendered_text, msg_xy)
            self.menu_select_compvid.render(surface)
        elif self.state == "confirm_res" :
            message = "New screen resolution selected, restart video?"
            rendered_text = font.render(message, True, color)
            surface.blit(rendered_text, msg_xy)
            self.menu_confirm_res.render(surface)

    def select_res_callback(self, res):
        def callback():
            if res != self.eyesy.config["video_resolution"] :
                self.new_video_res = res
                self.state = "confirm_res"
        return callback

    def select_compvid_callback(self, compvid):
        def callback():
            print(f"setting compvid {compvid}")
            set_tv_norm(compvid)
            self.current_compvid = compvid
        return callback

    def confirm_res(self):
        self.eyesy.config["video_resolution"] = self.new_video_res
        self.eyesy.save_config_file()
        self.eyesy.restart = True

    def select_res(self):
        self.state = "select_res"

    def select_compvid(self):
        self.state = "select_compvid"

    def goto_home(self):
        self.eyesy.switch_menu_screen("home")

