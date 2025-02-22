from screen import Screen
import pygame
import subprocess
import osd

def wifi_connected():
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



class ScreenTest(Screen):
    def __init__(self, eyesy):
        super().__init__(eyesy)
        self.title = "Factory Test"
        self.footer =  chr(0x2680) + "     = Cancel     "

        self.highlighted_controls = set()

        self.button_press_counts = {
            "top0": 0, "top1": 0, "top2": 0,
            "bottom0": 0, "bottom1": 0, "bottom2": 0, "bottom3": 0, "bottom4": 0, "bottom5": 0, "bottom6": 0
        }

        self.previous_button_states = {
            "top0": False, "top1": False, "top2": False,
            "bottom0": False, "bottom1": False, "bottom2": False, "bottom3": False, "bottom4": False, "bottom5": False, "bottom6": False
        }

        self.knob_min_reached = {"knob0": False, "knob1": False, "knob2": False, "knob3": False, "knob4": False}
        self.knob_max_reached = {"knob0": False, "knob1": False, "knob2": False, "knob3": False, "knob4": False}
        
        self.wifi_good = False
        self.midi_good = False
        self.audio_good = False
        self.audio_good_r = False
    

    def before(self):
        self.wifi_good = wifi_connected()
        self.midi_good = False
        self.audio_good = False
        self.audio_good_r = False
        
        self.highlighted_controls = set()
        self.button_press_counts = {
            "top0": 0, "top1": 0, "top2": 0,
            "bottom0": 0, "bottom1": 0, "bottom2": 0, "bottom3": 0, "bottom4": 0, "bottom5": 0, "bottom6": 0
        }

        self.previous_button_states = {
            "top0": False, "top1": False, "top2": False,
            "bottom0": False, "bottom1": False, "bottom2": False, "bottom3": False, "bottom4": False, "bottom5": False, "bottom6": False
        }

        self.knob_min_reached = {"knob0": False, "knob1": False, "knob2": False, "knob3": False, "knob4": False}
        self.knob_max_reached = {"knob0": False, "knob1": False, "knob2": False, "knob3": False, "knob4": False}

    def handle_events(self):
        self.handle_control_events(self.eyesy)

    def handle_control_events(self, events):
        # Mappings
        button_map = {
            "top0": events.key1_press,
            "top1": events.key2_press,
            "top2": events.key3_press,
            "bottom0": events.key4_press,
            "bottom1": events.key5_press,
            "bottom2": events.key6_press,
            "bottom3": events.key7_press,
            "bottom4": events.key8_press,
            "bottom5": events.key9_press,
            "bottom6": events.key10_press
        }

        knob_map = {
            "knob0": events.knob_hardware[0],
            "knob1": events.knob_hardware[1],
            "knob2": events.knob_hardware[2],
            "knob3": events.knob_hardware[3],
            "knob4": events.knob_hardware[4]
        }

        # Handle button presses
        for ctrl_id, is_pressed in button_map.items():
            prev_state = self.previous_button_states[ctrl_id]
            if not prev_state and is_pressed:
                # Rising edge
                self.button_press_counts[ctrl_id] += 1
                if self.button_press_counts[ctrl_id] == 3:
                    self.highlighted_controls.add(ctrl_id)
            self.previous_button_states[ctrl_id] = is_pressed

        # Handle knobs (check extremes)
        epsilon = 0 #0.01
        for ctrl_id, value in knob_map.items():
            if value <= epsilon:
                self.knob_min_reached[ctrl_id] = True

            # Only allow max to be reached if min was reached first
            if self.knob_min_reached.get(ctrl_id, False) and value >= 1.0 - epsilon:
                self.knob_max_reached[ctrl_id] = True

            if self.knob_min_reached.get(ctrl_id, False) and self.knob_max_reached.get(ctrl_id, False):
                self.highlighted_controls.add(ctrl_id)

    def check_audio_midi(self):
        if not self.audio_good :
            if self.eyesy.audio_peak > 20000: self.audio_good = True
        if not self.audio_good_r :
            if self.eyesy.audio_peak_r > 20000: self.audio_good_r = True
        if not self.midi_good:
            if  self.eyesy.midi_notes[60] > 0 and self.eyesy.midi_notes[62] > 0 and self.eyesy.midi_notes[64] > 0 : 
                self.midi_good = True

    def render(self, surface):

        self.check_audio_midi()

        msg_xy = (32, 90)
        if self.wifi_good :
            message = "USB WiFi Pass" 
            rendered_text = self.eyesy.font.render(message, True, self.eyesy.GREEN)
        else :
            message = "USB WiFi Not Connected" 
            rendered_text = self.eyesy.font.render(message, True, self.eyesy.RED)
        surface.blit(rendered_text, msg_xy)

        msg_xy = (32, 110)
        if self.midi_good :
            message = "MIDI In Connection Pass" 
            rendered_text = self.eyesy.font.render(message, True, self.eyesy.GREEN)
        else :
            message = "MIDI In Connection Problem" 
            rendered_text = self.eyesy.font.render(message, True, self.eyesy.RED)
        surface.blit(rendered_text, msg_xy)
        
        msg_xy = (32, 130)
        if self.audio_good :
            message = "Audio In L Connection Pass" 
            rendered_text = self.eyesy.font.render(message, True, self.eyesy.GREEN)
        else :
            message = "Audio In L Connection Problem" 
            rendered_text = self.eyesy.font.render(message, True, self.eyesy.RED)
        surface.blit(rendered_text, msg_xy)

        msg_xy = (32, 150)
        if self.audio_good_r :
            message = "Audio In R Connection Pass" 
            rendered_text = self.eyesy.font.render(message, True, self.eyesy.GREEN)
        else :
            message = "Audio In R Connection Problem" 
            rendered_text = self.eyesy.font.render(message, True, self.eyesy.RED)
        surface.blit(rendered_text, msg_xy)

        osd.draw_midi(surface, self.eyesy, 350, 110)
        osd.draw_vu_480(surface, self.eyesy, 350, 150)
        self.draw_controls(surface, self.highlighted_controls)

    def draw_controls(self, surface, highlighted):
        # Use the same logic as before, just passing `highlighted`
        WHITE = (200, 200, 200)

        panel_x, panel_y = 140, 200
        panel_width, panel_height = 355, 200

        pygame.draw.rect(surface, WHITE, (panel_x, panel_y, panel_width, panel_height), width=1)

        grid_rows = 11
        grid_cols = 11
        cell_width = panel_width / grid_cols
        cell_height = panel_height / grid_rows

        def grid_pos(row, col):
            x = panel_x + (col + 0.5)*cell_width
            y = panel_y + (row + 0.5)*cell_height
            return (int(x), int(y))

        button_radius = 12
        knob_radius = 16
        HIGHLIGHT_COLOR = (0, 255, 0)

        top_button_positions = [("top0", (2, 1)),
                                ("top1", (2, 6)),
                                ("top2", (2, 8))]

        mid_knob_positions = [("knob0", (5, 1)),
                              ("knob1", (5, 3)),
                              ("knob2", (5, 5)),
                              ("knob3", (5, 7)),
                              ("knob4", (5, 9))]

        bottom_button_positions = [("bottom0", (8, 1)),
                                   ("bottom1", (8, 2)),
                                   ("bottom2", (8, 4)),
                                   ("bottom3", (8, 5)),
                                   ("bottom4", (8, 6)),
                                   ("bottom5", (8, 8)),
                                   ("bottom6", (8, 9))]

        def draw_control(control_id, row_col, radius):
            r, c = row_col
            px = int(panel_x + (c + 0.5)*cell_width)
            py = int(panel_y + (r + 0.5)*cell_height)

            # If highlighted, fill first
            if control_id in highlighted:
                pygame.draw.circle(surface, HIGHLIGHT_COLOR, (px, py), radius, width=0)
            # Draw outline
            pygame.draw.circle(surface, WHITE, (px, py), radius, width=1)

        for ctrl_id, pos in top_button_positions:
            draw_control(ctrl_id, pos, button_radius)

        for ctrl_id, pos in mid_knob_positions:
            draw_control(ctrl_id, pos, knob_radius)

        for ctrl_id, pos in bottom_button_positions:
            draw_control(ctrl_id, pos, button_radius)
