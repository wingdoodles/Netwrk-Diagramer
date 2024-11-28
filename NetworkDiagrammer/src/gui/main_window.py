
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QMenuBar, QStatusBar, QToolBar)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon
from .scan_panel import ScanPanel
from .diagram_view import DiagramView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Diagrammer")
        self.setMinimumSize(1200, 800)
        
        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)
        
        # Initialize UI components
        self.setup_toolbar()
        self.setup_scan_panel()
        self.setup_diagram_view()
        self.setup_menubar()
        self.setup_statusbar()
        
    def setup_toolbar(self):
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(toolbar)
        
        # Add scan action
        scan_action = QAction("Start Scan", self)
        scan_action.setStatusTip("Start network scan")
        scan_action.triggered.connect(self.start_scan)
        toolbar.addAction(scan_action)
        
        # Add export action
        export_action = QAction("Export", self)
        export_action.setStatusTip("Export network diagram")
        export_action.triggered.connect(self.export_diagram)
        toolbar.addAction(export_action)
        
    def setup_scan_panel(self):
        self.scan_panel = ScanPanel()
        self.layout.addWidget(self.scan_panel, 1)
        
    def setup_diagram_view(self):
        self.diagram_view = DiagramView()
        self.layout.addWidget(self.diagram_view, 4)
        
    def setup_menubar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New Scan")
        file_menu.addAction("Export Diagram")
        file_menu.addSeparator()
        file_menu.addAction("Exit")
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        tools_menu.addAction("Settings")
        tools_menu.addAction("Refresh")
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("Documentation")
        help_menu.addAction("About")
        
    def setup_statusbar(self):
        self.statusBar().showMessage("Ready")
        
    def start_scan(self):
        self.statusBar().showMessage("Scanning network...")
        # Will implement scanning logic later
        
    def export_diagram(self):
        self.statusBar().showMessage("Exporting diagram...")
        # Will implement export logic later
