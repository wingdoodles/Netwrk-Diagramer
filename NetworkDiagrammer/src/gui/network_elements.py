from PyQt6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsLineItem
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPen, QBrush, QColor, QPainter, QFont

class NetworkNode(QGraphicsEllipseItem):
    def __init__(self, device_info):
        super().__init__(0, 0, 60, 60)
        self.device_info = device_info
        self.setup_node()
        
    def setup_node(self):
        # Visual settings
        self.setZValue(1)
        self.setBrush(self.get_node_color())
        self.setPen(QPen(Qt.GlobalColor.black, 2))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        
    def get_node_color(self):
        # Color coding based on device type
        if 'server' in self.device_info.os_type.lower():
            return QBrush(QColor(255, 100, 100))  # Red for servers
        elif 'windows' in self.device_info.os_type.lower():
            return QBrush(QColor(100, 100, 255))  # Blue for Windows
        elif 'linux' in self.device_info.os_type.lower():
            return QBrush(QColor(100, 255, 100))  # Green for Linux
        return QBrush(QColor(200, 200, 200))      # Gray for others
        
    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        painter.setFont(QFont('Arial', 8))
        
        # Draw IP address
        text_rect = QRectF(-10, -20, 80, 20)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.device_info.ip_address)
        
        # Draw hostname
        text_rect = QRectF(-10, 60, 80, 20)
        display_name = self.device_info.hostname[:15] + '...' if len(self.device_info.hostname) > 15 else self.device_info.hostname
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, display_name)

class NetworkEdge(QGraphicsLineItem):
    def __init__(self, start_pos, end_pos):
        super().__init__(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
        self.setup_edge()
        
    def setup_edge(self):
        self.setZValue(0)  # Edges behind nodes
        self.setPen(QPen(QColor(150, 150, 150), 2, Qt.PenStyle.SolidLine))
        
    def update_position(self, start_pos, end_pos):
        self.setLine(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
