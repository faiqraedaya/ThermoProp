"""
THERMOPROP 
Thermophysical Properties Calculator

Version: 2.2.0
Author: Faiq Raedaya
Date: 2025-05-29

Changelog:
- 2025-05-28: Full rewrite with improved functionality and user interface
- 2025-05-29: Separated helper classes into individual files
- 2025-06-23: Fixed UI not running backend calculations 
"""

import sys
from PyQt5.QtWidgets import QApplication

from main_window import MainWindow

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("ThermoProp")
    app.setApplicationVersion("2.2.0")
    app.setOrganizationName("MES")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()