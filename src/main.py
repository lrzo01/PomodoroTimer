import rumps
import threading
import time
import json
import os
from timer.timer import PomodoroTimer
from AppKit import NSApplication, NSApplicationActivationPolicyAccessory
import ServiceManagement

CONFIG_FILE = "pomodoro_config.json"
BUNDLE_ID = "com.lrzo01.PomodoroTimer"  

class PomodoroTimerClient(rumps.App):
    def __init__(self):
        super().__init__("00:00", menu=["Start on Login", None, "Pause", None, "Settings"])

        NSApplication.sharedApplication().setActivationPolicy_(NSApplicationActivationPolicyAccessory)

        self.config = self.load_config()
        work_interval = self.config.get("work_interval", 25)
        break_interval = self.config.get("break_interval", 5)
        start_on_login = self.config.get("start_on_login", False)

        self.pomodoro = PomodoroTimer(work_interval=work_interval, break_interval=break_interval)
        self.thread = threading.Thread(target=self.update_loop, daemon=True)
        self.thread.start()

        self.menu["Start on Login"].state = start_on_login

        if start_on_login:
            self.enable_start_on_login(True)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_config(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config, f, indent=4)

    def update_loop(self):
        while True:
            if self.pomodoro.current_state == "work":
                self.icon = "assets/work.png"
            else:
                self.icon = "assets/break.png"
            self.title = self.pomodoro.getCurrentTimeString()
            time.sleep(0.5)

    @rumps.clicked("Pause")
    def pause(self, sender):
        if self.pomodoro.is_paused:
            self.pomodoro.is_paused = False
            sender.title = "Pause"
        else:
            self.pomodoro.is_paused = True
            sender.title = "Resume"

    @rumps.clicked("Settings")
    def settings(self, sender):
        work = rumps.Window("Work interval (minutes):", "Settings", ok="Save").run()
        break_ = rumps.Window("Break interval (minutes):", "Settings", ok="Save").run()

        try:
            work_val = int(work.text)
            break_val = int(break_.text)
            self.pomodoro.configure(work_interval=work_val, break_interval=break_val)

            self.config["work_interval"] = work_val
            self.config["break_interval"] = break_val
            self.save_config()

            rumps.notification("Pomodoro Timer", "Settings Updated", 
                               f"Work: {work_val} min, Break: {break_val} min")
        except ValueError:
            rumps.alert("Invalid input! Please enter integer values.")

    @rumps.clicked("Start on Login")
    def start_on_login(self, sender):
        sender.state = not sender.state
        self.config["start_on_login"] = sender.state
        self.save_config()
        self.enable_start_on_login(sender.state)

    def enable_start_on_login(self, enable: bool):
        success = ServiceManagement.SMLoginItemSetEnabled(BUNDLE_ID, enable)
        if not success:
            print("Failed to modify login item")

if __name__ == "__main__":
    PomodoroTimerClient().run()
