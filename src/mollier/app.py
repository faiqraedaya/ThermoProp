"""
MOLLIER
Thermophysical Properties Calculator

Application entry point.
"""

import logging
import sys

from PySide6.QtWidgets import QApplication

from .gui.icons import app_icon
from .gui.main_window import MainWindow
from .gui.theme import apply_mpl_theme, apply_theme

__version__ = "2.7.0"


def _set_windows_app_id():
    """Give the process its own taskbar identity on Windows.

    Without an explicit AppUserModelID, Windows groups the window under the
    Python interpreter and shows the interpreter's icon in the taskbar.
    """
    if sys.platform != "win32":
        return
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "Mollier.Mollier")
    except (AttributeError, OSError):
        logging.getLogger(__name__).warning(
            "Could not set the Windows AppUserModelID")


def main():
    """Main application entry point"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    _set_windows_app_id()
    app = QApplication(sys.argv)
    app.setApplicationName("Mollier")
    app.setWindowIcon(app_icon())
    app.setApplicationVersion(__version__)

    # theme.py is the sole styling authority; nothing else sets a stylesheet.
    apply_theme(app)
    apply_mpl_theme()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
