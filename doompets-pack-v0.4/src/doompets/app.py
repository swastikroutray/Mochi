from time import monotonic
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from .config import load_pet
from .pet import PetWindow
from .scorer import classify_window, score, state_for
from .tracker import active_window_title


class DoomPetApp:
    def __init__(self) -> None:
        self.qt = QApplication([])
        self.window = PetWindow(load_pet())
        self.window.place_bottom_right()
        self.window.show()

        self.last_tick = monotonic()
        self.doom_minutes = 0.0
        self.productive_minutes = 0.0
        self.productive_streak = 0.0

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)
        self.tick()

    def tick(self) -> None:
        now = monotonic()
        delta_minutes = (now - self.last_tick) / 60.0
        self.last_tick = now

        category = classify_window(active_window_title())
        if category == "doom":
            self.doom_minutes += delta_minutes
            self.productive_streak = 0.0
        elif category == "productive":
            self.productive_minutes += delta_minutes
            self.productive_streak += delta_minutes
        else:
            self.productive_streak = 0.0

        current_score = score(self.doom_minutes, self.productive_minutes)
        self.window.set_state(state_for(current_score, self.productive_streak))

    def run(self) -> int:
        return self.qt.exec()
