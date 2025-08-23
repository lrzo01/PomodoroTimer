import threading
import time

class PomodoroTimer:
    def __init__(self, work_interval=25, break_interval=5):
        self.work_interval = work_interval * 60
        self.break_interval = break_interval * 60
        self.current_state = "work"
        self.is_paused = False
        self.is_running = True

        self.time_remaining = self.work_interval

        threading.Thread(target=self.timer, daemon=True).start()

    def configure(self, work_interval=None, break_interval=None):
        if work_interval is not None:
            self.work_interval = work_interval * 60
        if break_interval is not None:
            self.break_interval = break_interval * 60

    def getCurrentTimeString(self):
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        return f"{minutes:02d}:{seconds:02d}"

    def timer(self):
        while self.is_running:
            time.sleep(1)
            if not self.is_paused:
                self.time_remaining -= 1

                if self.current_state == "work" and self.time_remaining <= 0:
                    self.current_state = "break"
                    self.time_remaining = self.break_interval

                elif self.current_state == "break" and self.time_remaining <= 0:
                    self.current_state = "work"
                    self.time_remaining = self.work_interval
