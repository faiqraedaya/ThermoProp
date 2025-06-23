"""
About dialog implementation for ThermoProp application
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class AboutDialog(QDialog):
    """About dialog for the application"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About ThermoProp")
        self.setFixedSize(400, 300)
        self.setModal(True)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("ThermoProp v2.2.0")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(
            "Enhanced Thermophysical Properties Calculator\n"
            "For Risk and Safety Engineering Applications\n"
            "with Mixture Support"
        )
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("margin: 10px;")
        layout.addWidget(desc_label)
        
        # Copyright
        copyright_label = QLabel("© 2025 Faiq Raedaya")
        copyright_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(copyright_label)
        
        # Requirements
        req_label = QLabel(
            "Requirements:\n"
            "• CoolProp\n"
            "• PyQt5\n"
            "• matplotlib\n"
            "• pandas\n"
            "• numpy\n"
            "• scipy"
        )
        req_label.setAlignment(Qt.AlignCenter)
        req_label.setStyleSheet("margin: 10px;")
        layout.addWidget(req_label)
        
        # Close button
        button_layout = QHBoxLayout()
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
