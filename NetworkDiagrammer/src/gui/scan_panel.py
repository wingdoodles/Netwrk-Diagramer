
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, 
                            QLineEdit, QPushButton, QLabel, QComboBox)
from PyQt6.QtCore import pyqtSignal

class ScanPanel(QWidget):
    scan_started = pyqtSignal(str)  # Signal to emit IP range
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Scan Configuration Group
        scan_group = QGroupBox("Scan Configuration")
        scan_layout = QVBoxLayout()
        
        # IP Range input
        ip_label = QLabel("IP Range:")
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("192.168.1.0/24")
        
        # Scan type selector
        scan_type_label = QLabel("Scan Type:")
        self.scan_type = QComboBox()
        self.scan_type.addItems(["Quick Scan", "Full Scan", "Custom"])
        
        # Scan button
        self.scan_button = QPushButton("Start Scan")
        self.scan_button.clicked.connect(self.start_scan)
        
        # Add widgets to layout
        scan_layout.addWidget(ip_label)
        scan_layout.addWidget(self.ip_input)
        scan_layout.addWidget(scan_type_label)
        scan_layout.addWidget(self.scan_type)
        scan_layout.addWidget(self.scan_button)
        scan_group.setLayout(scan_layout)
        
        # Add group to main layout
        layout.addWidget(scan_group)
        layout.addStretch()
        self.setLayout(layout)
        
    def start_scan(self):
        ip_range = self.ip_input.text()
        if ip_range:
            self.scan_started.emit(ip_range)
