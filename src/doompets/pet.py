from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtCore import QObject, QPoint, Qt, QUrl, Signal, Slot
from PySide6.QtGui import QColor, QKeyEvent, QWheelEvent
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QSizePolicy, QWidget


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

        self.window.move(
            current.x() + round(dx),
            current.y() + round(dy),
        )

    @Slot()
    def begin_drag(self) -> None:
        self.drag_started.emit()

    @Slot()
    def end_drag(self) -> None:
        self.drag_finished.emit()


class PetWebView(QWebEngineView):
    """Web view that prevents browser-style zooming."""

    def wheelEvent(self, event: QWheelEvent) -> None:
        # Block Ctrl + mouse-wheel zoom.
        if event.modifiers() & Qt.ControlModifier:
            event.accept()
            return

        super().wheelEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # Block common browser zoom shortcuts:
        # Ctrl + Plus
        # Ctrl + Minus
        # Ctrl + Equals
        # Ctrl + 0
        if event.modifiers() & Qt.ControlModifier:
            if event.key() in (
                Qt.Key_Plus,
                Qt.Key_Minus,
                Qt.Key_Equal,
                Qt.Key_0,
            ):
                event.accept()
                return

        super().keyPressEvent(event)


class PetWindow(QWidget):
    """Transparent, always-on-top desktop window containing the HTML/CSS pet."""

    PET_WIDTH = 170
    PET_HEIGHT = 140

    def __init__(self, pet_config: dict):
        super().__init__()

        self.pet_config = pet_config
        self.current_state = "normal"

        # True only after the HTML page has fully loaded.
        self._page_ready = False

        self._drag_offset: QPoint | None = None

        # ---------------------------------
        # Window configuration
        # ---------------------------------

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
            | Qt.WindowDoesNotAcceptFocus
        )

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        # Completely fixed native window size.
        self.setFixedSize(
            self.PET_WIDTH,
            self.PET_HEIGHT,
        )

        self.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed,
        )

        # ---------------------------------
        # Web view
        # ---------------------------------

        self.view = PetWebView(self)

        # Keep WebEngine zoom at 100%.
        self.view.setZoomFactor(1.0)

        self.view.setGeometry(
            0,
            0,
            self.PET_WIDTH,
            self.PET_HEIGHT,
        )

        self.view.setAttribute(
            Qt.WA_TranslucentBackground
        )

        self.view.setStyleSheet(
            "background: transparent;"
        )

        self.view.settings().setAttribute(
            QWebEngineSettings.ShowScrollBars,
            False,
        )

        self.view.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessFileUrls,
            True,
        )

        self.view.setContextMenuPolicy(
            Qt.NoContextMenu
        )

        # ---------------------------------
        # Transparent page
        # ---------------------------------

        page = self.view.page()

        page.setBackgroundColor(
            QColor(0, 0, 0, 0)
        )

        # ---------------------------------
        # Python <-> JavaScript bridge
        # ---------------------------------

        self.bridge = PetBridge(self)

        self.channel = QWebChannel(page)

        self.channel.registerObject(
            "doompets",
            self.bridge,
        )

        page.setWebChannel(self.channel)

        # ---------------------------------
        # Load HTML
        # ---------------------------------

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

        # IMPORTANT:
        # Connect BEFORE loading the page.
        self.view.loadFinished.connect(
            self._on_page_loaded
        )

        self.view.load(
            QUrl.fromLocalFile(
                str(html_path)
            )
        )

    # ---------------------------------
    # Page loading
    # ---------------------------------

    def _on_page_loaded(self, ok: bool) -> None:
        """Called when the HTML page finishes loading."""

        if not ok:
            print(
                "DoomPets: Failed to load pet UI."
            )
            return

        self._page_ready = True

        # JavaScript is now safe to call.
        self._send_config_once_loaded()

    def _send_config_once_loaded(self) -> None:
        """Send pet configuration to the JavaScript UI."""

        if not self._page_ready:
            return

        messages = self.pet_config.get(
            "messages",
            {},
        )

        payload = json.dumps(messages)

        self.view.page().runJavaScript(
            f"window.doompetsSetMessages({payload});"
        )

        # Restore current state.
        self.set_state(
            self.current_state
        )

    # ---------------------------------
    # State
    # ---------------------------------

    def set_state(self, state: str) -> None:
        """Change pet state and its speech bubble."""

        self.current_state = state

        # Never call JS before page load.
        if not self._page_ready:
            return

        messages = (
            self.pet_config
            .get("messages", {})
            .get(state, ["..."])
        )

        message = (
            messages[0]
            if messages
            else "..."
        )

        state_json = json.dumps(state)
        message_json = json.dumps(message)

        self.view.page().runJavaScript(
            f"window.doompetsSetState("
            f"{state_json}, "
            f"{message_json}"
            f");"
        )

    # ---------------------------------
    # Fixed size
    # ---------------------------------

    def resizeEvent(self, event) -> None:
        """Keep the WebEngine exactly the size of the pet window."""

        super().resizeEvent(event)

        self.view.setGeometry(
            0,
            0,
            self.PET_WIDTH,
            self.PET_HEIGHT,
        )

        # Prevent any external resize attempt.
        if (
            self.width() != self.PET_WIDTH
            or self.height() != self.PET_HEIGHT
        ):
            self.setFixedSize(
                self.PET_WIDTH,
                self.PET_HEIGHT,
            )

    # ---------------------------------
    # Position
    # ---------------------------------

    def place_bottom_right(self) -> None:
        """Place pet at bottom-right of the primary screen."""

        screen = (
            QApplication
            .primaryScreen()
            .availableGeometry()
        )

        self.move(
            screen.right()
            - self.width()
            - 24,

            screen.bottom()
            - self.height()
            - 24,
        )