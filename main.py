"""
THERMOPROP
Thermophysical Properties Calculator

Version: 2.3.0
Author: Faiq Raedaya
Date: 2026-05-20

Changelog:
- 1.0.0 - 2025-05-03
    - Initial build with basic functionality
- 2.0.0 - 2025-05-28
    - Full rewrite with improved functionality and user interface
- 2.1.0 - 2025-05-29
    - Separated helper classes into individual files
- 2.2.0 - 2025-06-23
    - Fixed UI not running backend calculations
- 2.3.0 - 2026-05-20
    - Migrated to PySide6
    - Removed custom style
    - Removed quick calc dialog and help/about
"""

import sys
import os

from PySide6.QtWidgets import QApplication
from src.thermoprop.main_window import MainWindow

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("ThermoProp")
    app.setApplicationVersion("2.3.0")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
