import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem
import pyqtgraph.opengl as gl
from PyQt5.QtCore import Qt


class BiomecanicaUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Análisis Biomecánico 3D")
        self.setGeometry(100, 100, 1400, 800)

        # Widget central
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # --- Panel Izquierdo: Gráfico 3D ---
        self.view3D = gl.GLViewWidget()
        self.view3D.setCameraPosition(distance=300)
        self.view3D.setBackgroundColor('w')

        # --- Panel Derecho: Tabla de Ángulos ---
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Articulación", "Ángulo (°)"])
        
        #Modificamos la estetica de la leyenda 
        self.table.setStyleSheet("QTableWidget { background-color: #f0f0f0; font-size: 14px; } QHeaderView::section { background-color: #d0d0d0; font-weight: bold; padding: 4px; border: 1px solid #a0a0a0; }")
        # Estética
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        

        # Añadir widgets al layout
        main_layout.addWidget(self.view3D, stretch=3)
        main_layout.addWidget(self.table, stretch=1)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def create_skeleton(self):
        """Dibuja un esqueleto simple con segmentos entre keypoints."""
        pass
    
    def update_angles(self, angles):
        """Actualiza la tabla de angulos con los valores proporcionados."""
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BiomecanicaUI()
    window.show()
    sys.exit(app.exec_())
    
    
    



