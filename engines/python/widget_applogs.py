import pygame
import subprocess
import time
import re

class WidgetApplogs():
    def __init__(self, eyesy):
        self.eyesy = eyesy
        self.font = pygame.font.Font("font.ttf", 10)
        self.logs = []
        self.last_log_time = 0  # Timestamp of the last log fetch
        self.x_offset = 10
        self.y_offset = 10

    def fetch_logs(self):
        """fetch logs from journalctl."""
        try:
            result = subprocess.run(
                ["journalctl", "-u", "eyesypy", "-n", "20", "--no-pager", "--output=cat"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if result.returncode == 0:
                # Clean up each line by removing "[numbers]" and alsa underrun 
                raw_logs = result.stdout.strip().split("\n")
                self.logs = [
                    re.sub(r"\[\d+(\.\d+)?\]", "", line).strip()
                    for line in raw_logs
                    if "(snd_pcm_recover) underrun occurred" not in line
                ]

            else:
                self.logs = ["Error fetching logs: " + result.stderr.strip()]
        except FileNotFoundError:
            self.logs = ["Error: journalctl not found."]

    def before(self):
        self.fetch_logs()  # Initial log fetch

    def render(self, surface):
        current_time = time.time()
        if current_time - self.last_log_time > 1:  # fetch logs once per second
            self.fetch_logs()
            self.last_log_time = current_time

        line_height = self.font.get_linesize()
        for i, log in enumerate(self.logs):
            text_surface = self.font.render(log, True, (200, 200, 200))  # White text
            surface.blit(text_surface, (self.x_offset, self.y_offset + i * line_height))

