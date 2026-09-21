from __future__ import annotations

from pathlib import Path
from typing import Optional

from PySide6.QtCore import QObject, QPoint, Qt, QUrl, Signal, Slot
from PySide6.QtGui import QColor
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QWidget


class PetBridge(QObject):
    """Python <-> HTML bridge used by the pet UI."""

    drag_started = Signal()
    drag_finished = Signal()

    def __init__(self, window: "PetWindow") -> None:
        super().__init__(window)
        self.window = window

    @Slot(float, float)
    def move_pet(self, dx: float, dy: float) -> None:
        """Move the native desktop window by a JS-provided delta."""
        current = self.window.pos()
        self.window.move(current.x() + round(dx), current.y() + round(dy))

    @Slot()
    def begin_drag(self) -> None:
        self.drag_started.emit()

    @Slot()
    def end_drag(self) -> None:
        self.drag_finished.emit()


class PetWindow(QWidget):
    """Transparent, always-on-top desktop window containing the HTML/CSS pet."""

    def __init__(self, pet_config: dict):
        super().__init__()
        self.pet_config = pet_config
        self.current_state = "normal"
        self._drag_offset: Optional[QPoint] = None

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
            | Qt.WindowDoesNotAcceptFocus
        )

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.resize(220, 180)

        self.view = QWebEngineView(self)
        self.view.setGeometry(self.rect())
        self.view.setAttribute(Qt.WA_TranslucentBackground)
        self.view.setStyleSheet("background: transparent;")
        self.view.settings().setAttribute(
            QWebEngineSettings.ShowScrollBars,
            False
        )
        self.view.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessFileUrls,
            True
        )
        self.view.setContextMenuPolicy(Qt.NoContextMenu)

        page = self.view.page()
        page.setBackgroundColor(QColor(0, 0, 0, 0))

        self.bridge = PetBridge(self)
        self.channel = QWebChannel(self.view.page())
        self.channel.registerObject("doompets", self.bridge)
        self.view.page().setWebChannel(self.channel)

        html_path = (
            Path(__file__).resolve().parents[2]
            / "pets"
            / "mochi"
            / "index.html"
        )

        if not html_path.exists():
            raise FileNotFoundError(
                f"Pet UI not found: {html_path}"
            )

        self.view.load(
            QUrl.fromLocalFile(str(html_path))
        )

        self.view.installEventFilter(self)

        self._send_config_once_loaded()

        self.view.loadFinished.connect(
            lambda _ok: self._send_config_once_loaded()
        )

    def _send_config_once_loaded(self) -> None:
        import json

        payload = json.dumps(
            self.pet_config.get("messages", {})
        )

        js = (
            f"window.doompetsSetMessages({payload});"
        )

        self.view.page().runJavaScript(js)

        self.set_state(self.current_state)

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self.view.setGeometry(self.rect())

    def set_state(self, state: str) -> None:
        self.current_state = state

        messages = (
            self.pet_config
            .get("messages", {})
            .get(state, ["..."])
        )

        message = messages[0] if messages else "..."

        import json

        self.view.page().runJavaScript(
            f"window.doompetsSetState("
            f"{json.dumps(state)}, "
            f"{json.dumps(message)}"
            f");"
        )

    def place_bottom_right(self) -> None:
        screen = (
            QApplication
            .primaryScreen()
            .availableGeometry()
        )

        self.move(
            screen.right() - self.width() - 24,
            screen.bottom() - self.height() - 24,
        )