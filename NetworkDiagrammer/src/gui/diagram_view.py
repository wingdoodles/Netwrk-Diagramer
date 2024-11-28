
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from .network_elements import NetworkNode, NetworkEdge
import math

class DiagramView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setup_view()
        
    def setup_view(self):
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        
    def update_network_diagram(self, devices):
        self.scene.clear()
        if not devices:
            return
            
        # Calculate positions in a circular layout
        positions = self.calculate_positions(devices)
        
        # Create nodes and edges
        self.create_nodes(devices, positions)
        self.create_edges(devices, positions)
        
        # Fit the view to all items
        self.fitInView(self.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
        
    def calculate_positions(self, devices):
        positions = {}
        device_count = len(devices)
        radius = 200
        
        for i, device in enumerate(devices):
            angle = (2 * math.pi * i) / device_count
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            positions[device.ip_address] = (x, y)
            
        return positions

    def create_nodes(self, devices, positions):
        self.nodes = {}
        for device in devices:
            pos = positions[device.ip_address]
            node = NetworkNode(device)
            node.setPos(pos[0], pos[1])
            self.scene.addItem(node)
            self.nodes[device.ip_address] = node
            
    def create_edges(self, devices, positions):
        self.edges = []
        for i, device1 in enumerate(devices):
            for device2 in devices[i+1:]:
                if self.should_connect(device1, device2):
                    pos1 = positions[device1.ip_address]
                    pos2 = positions[device2.ip_address]
                    edge = NetworkEdge(pos1, pos2)
                    self.scene.addItem(edge)
                    self.edges.append(edge)
                    
    def should_connect(self, device1, device2):
        # Basic subnet check - can be enhanced for more sophisticated connection logic
        ip1_parts = device1.ip_address.split('.')
        ip2_parts = device2.ip_address.split('.')
        return ip1_parts[0:3] == ip2_parts[0:3]
        
    def wheelEvent(self, event):
        zoom_factor = 1.15
        if event.angleDelta().y() > 0:
            self.scale(zoom_factor, zoom_factor)
        else:
            self.scale(1/zoom_factor, 1/zoom_factor)
            
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            event = QMouseEvent(QEvent.Type.MouseButtonPress,
                              event.pos(),
                              Qt.MouseButton.LeftButton,
                              Qt.MouseButton.LeftButton,
                              Qt.KeyboardModifier.NoModifier)
        super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        super().mouseReleaseEvent(event)
        
    def refresh_layout(self):
        """Recalculate and update node positions"""
        if not self.nodes:
            return
            
        positions = self.calculate_positions(list(self.nodes.values()))
        
        # Update node positions
        for ip, node in self.nodes.items():
            pos = positions[ip]
            node.setPos(pos[0], pos[1])
            
        # Update edge positions
        for edge in self.edges:
            start_node = edge.sourceNode()
            end_node = edge.destNode()
            edge.update_position(start_node.pos(), end_node.pos())        
    self.scene.setSceneRect(self.scene.itemsBoundingRect())

    def export_diagram(self, filename):
        """Export the current diagram as an image"""
        image = QImage(self.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)
        
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.scene.render(painter)
        painter.end()
        
        image.save(filename)
        
    def highlight_node(self, ip_address):
        """Highlight a specific node"""
        if ip_address in self.nodes:
            node = self.nodes[ip_address]
            effect = QGraphicsDropShadowEffect()
            effect.setColor(QColor(255, 215, 0))  # Golden glow
            effect.setBlurRadius(20)
            effect.setOffset(0)
            node.setGraphicsEffect(effect)
            
    def clear_highlights(self):
        """Clear all node highlights"""
        for node in self.nodes.values():
            node.setGraphicsEffect(None)
