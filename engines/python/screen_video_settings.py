from screen import Screen
from widget_menu import WidgetMenu, MenuItem

class ScreenVideoSettings(Screen):
    def __init__(self, app_state):
        super().__init__(app_state)
        self.state = "idle" 
        self.title = "Video Settings"
        self.new_video_res = 0

        self.menu = WidgetMenu(app_state, [
            MenuItem('HDMI Resolution  ▶', self.select_res),
            MenuItem('Select NTSC / PAL  ▶', self.select_compvid),
            MenuItem('◀  Exit', self.goto_home)
        ])
        self.menu.off_y = 43
        
        self.menu_select_res = WidgetMenu(app_state, [
            MenuItem(self.app_state.RESOLUTIONS[0]["name"], self.select_res_callback(0)),
            MenuItem(self.app_state.RESOLUTIONS[1]["name"], self.select_res_callback(1)),
            MenuItem(self.app_state.RESOLUTIONS[2]["name"], self.select_res_callback(2)),
            MenuItem(self.app_state.RESOLUTIONS[3]["name"], self.select_res_callback(3)),
            MenuItem(self.app_state.RESOLUTIONS[4]["name"], self.select_res_callback(4)),
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
         
        self.menu_confirm_res = WidgetMenu(app_state, [
            MenuItem('Yes', self.confirm_res),
            MenuItem('◀  Cancel', self.goto_home)
        ])
        self.menu_confirm_res.off_y = 75

    def before(self):
        self.menu_select_res.set_selected_index(self.app_state.config["video_resolution"])
        self.state = "idle"

    def after(self):
        self.app_state.save_config_file()

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
            reso = self.app_state.RESOLUTIONS[self.app_state.config["video_resolution"]]["name"]
            message = f"Select Resolution for HDMI. Currently {reso} "
            rendered_text = font.render(message, True, color)
            surface.blit(rendered_text, msg_xy)
            self.menu_select_res.render(surface)
        elif self.state == "select_compvid" :
            message = "Select Composite Video Settings"
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
            if res != self.app_state.config["video_resolution"] :
                self.new_video_res = res
                self.state = "confirm_res"
        return callback

    def confirm_res(self):
        self.app_state.config["video_resolution"] = self.new_video_res
        self.app_state.save_config_file()
        self.app_state.restart = True


    def select_res(self):
        self.state = "select_res"

    def select_compvid(self):
        self.state = "select_compvid"

    def goto_home(self):
        self.app_state.switch_menu_screen("home")

