from screen import Screen
from widget_menu import WidgetMenu, MenuItem

class ScreenVideoSettings(Screen):
    def __init__(self, app_state):
        super().__init__(app_state)
        self.state = "idle" 
        self.title = "Video Settings"

        self.menu = WidgetMenu(app_state, [
            MenuItem('HDMI Resolution  ▶', self.select_res),
            MenuItem('Select NTSC / PAL  ▶', self.select_compvid),
            MenuItem('◀  Exit', self.goto_home)
        ])
        self.menu.off_y = 43
        
        self.menu_select_res = WidgetMenu(app_state, [
            MenuItem(self.app_state.resolutions[0]["name"], self.select_res_callback(self.app_state.resolutions[0]["res"])),
            MenuItem(self.app_state.resolutions[1]["name"], self.select_res_callback(self.app_state.resolutions[1]["res"])),
            MenuItem(self.app_state.resolutions[2]["name"], self.select_res_callback(self.app_state.resolutions[2]["res"])),
            MenuItem(self.app_state.resolutions[3]["name"], self.select_res_callback(self.app_state.resolutions[3]["res"])),
            MenuItem(self.app_state.resolutions[4]["name"], self.select_res_callback(self.app_state.resolutions[4]["res"])),
            MenuItem('◀  Exit', self.goto_home)
        ])
        self.menu_select_res.off_y = 75
        
        self.menu_select_compvid = WidgetMenu(app_state, [
            MenuItem('NTSC', self.select_res),
            MenuItem('PAL', self.select_res),
            MenuItem('SECAM', self.select_res),
            MenuItem('◀  Exit', self.goto_home)
        ])
        self.menu_select_compvid.off_y = 75

    def select_res_callback(self, res):
        def callback():
            #self.set_res(res)
            print(res)
        return callback

    def before(self):
        self.state = "idle"

    def handle_events(self):
        if self.state == "idle":
            self.menu.handle_events()
        elif self.state == "select_res":
            self.menu_select_res.handle_events()
        elif self.state == "select_compvid":
            self.menu_select_compvid.handle_events()

    def render(self, surface):

        msg_xy = (32, 68)
        font = self.menu.font
        color = (200, 200, 200)
        if self.state == "idle":
            self.menu.render(surface)
        elif self.state == "select_res" :
            message = "Select Resolution for HDMI. Currently 1280 x 720" #f"Connecting to {self.target_ssid}..."
            rendered_text = font.render(message, True, color)
            surface.blit(rendered_text, msg_xy)
            self.menu_select_res.render(surface)
        elif self.state == "select_compvid" :
            message = "Select Composite Video Settings"#f"Connecting to {self.target_ssid}..."
            rendered_text = font.render(message, True, color)
            surface.blit(rendered_text, msg_xy)
            self.menu_select_compvid.render(surface)

    def select_res(self):
        self.state = "select_res"

    def select_compvid(self):
        self.state = "select_compvid"

    def goto_home(self):
        self.app_state.switch_menu_screen("home")

