import pygame
import subprocess
import time
import re

class WidgetNetlogs():
    def __init__(self, app_state):
        self.app_state = app_state
        self.font = pygame.font.Font("font.ttf", 10)
        self.logs = []
        self.last_log_time = 0  # Timestamp of the last log fetch
        self.x_offset = 10
        self.y_offset = 10

    def fetch_logs(self):
        """Fetch logs from journalctl."""
        try:
            result = subprocess.run(
                ["journalctl", "-u", "NetworkManager", "-n", "10", "--no-pager", "--output=cat"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if result.returncode == 0:
                # Clean up each line by removing "[numbers]"
                raw_logs = result.stdout.strip().split("\n")
                self.logs = [re.sub(r"\[\d+(\.\d+)?\]", "", line).strip() for line in raw_logs]
            else:
                self.logs = ["Error fetching logs: " + result.stderr.strip()]
        except FileNotFoundError:
            self.logs = ["Error: journalctl not found."]

    def before(self):
        self.fetch_logs()  # Initial log fetch

    def render(self, surface):
        current_time = time.time()
        if current_time - self.last_log_time > 1:  # Fetch logs once per second
            self.fetch_logs()
            self.last_log_time = current_time

        line_height = self.font.get_linesize()
        for i, log in enumerate(self.logs):
            text_surface = self.font.render(log, True, (200, 200, 200))  # White text
            surface.blit(text_surface, (self.x_offset, self.y_offset + i * line_height))

