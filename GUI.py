import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QTableWidget, QTableWidgetItem, QMessageBox, QPushButton
)
from PyQt5.QtCore import QTimer
import pyqtgraph.opengl as gl
from PyQt5.QtWidgets import QHeaderView, QAction, QActionGroup, QMenu
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtGui import QPalette, QColor


class BiomecanicaUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Análisis Biomecánico 3D")
        self.setGeometry(100, 100, 1800, 900)

        # --- Barra de menu ---
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Archivo")
        visualization_menu = menubar.addMenu("Visualización")
        config_menu = menubar.addMenu("Configuración")
        help_menu = menubar.addMenu("Ayuda")

        #Exportar datos
        export_action = QAction("Exportar Datos", self)
        file_menu.addAction(export_action)

        # Seleccion de vista
        visualization_group = QActionGroup(self)
        visualization_group.setExclusive(True)
        view_2d_action = QAction("Vista Imagen", self, checkable=True, checked=True)
        view_3d_action = QAction("Vista 3D", self, checkable=True)
        visualization_group.addAction(view_2d_action)
        visualization_group.addAction(view_3d_action)
        visualization_menu.addAction(view_2d_action)
        visualization_menu.addAction(view_3d_action)

        #TODO: Implementar la acciones de cambio de vista
        # view_2d_action.triggered.connect(self.show_2d_view)
        # view_3d_action.triggered.connect(self.show_3d_view)

        #Menu de configuracion
        self.list_cam = ["Cam 1", "Cam 2", "Cam 3", "Cam 4"]
        # self.ObtainCamAvailable() TODO:

        #Visualizar camaras disponibles
        cam_menu = QMenu("Cámaras Disponibles", self)
        for cam in self.list_cam:
            action = QAction(cam, self)
            cam_menu.addAction(action)

        config_menu.addMenu(cam_menu)

        #Paguina de configuracion de vista
        cam_vista = {
            "Vista Derecha":"",
            "Vista Izquierda":"",
            "vista Trasera":"",
            "Vista Frontal":"",
        }
        conf_cam_menu = QAction("Configuración de Cámaras", self)
        #conf_cam_menu.triggered.connect(self.MenuConfigCam) TODO: Implementar la pagina de configuracion de camaras
        config_menu.addAction(conf_cam_menu)

        # Acción salir
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Repo
        repo_action = QAction("Repositorio", self)
        repo_action.triggered.connect(lambda: QMessageBox.information(self, "Repositorio",
                                                                        "Visita nuestro repositorio en GitHub:\n\n"
                                                                        "https://github.com/tu-repo"))
        help_menu.addAction(repo_action)

        # Acción acerca de
        about_action = QAction("Acerca de...", self)
        about_action.triggered.connect(lambda: QMessageBox.information(self, "Acerca de",
                                                                        "Aplicación de Bikefitting basada en visión artificial.\n\n"
                                                                        "Desarrollada por: Castro-3034-tbr\n\n"
                                                                        "Versión 1.0\n\n"))
        help_menu.addAction(about_action)

        # --- Panel principal ---
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # Panel en blanco (izquierda)
        self.blank_panel = QWidget()
        self.blank_panel.setMinimumWidth(500)
        palette = self.blank_panel.palette()
        palette.setColor(QPalette.Window, QColor('white'))
        self.blank_panel.setAutoFillBackground(True)
        self.blank_panel.setPalette(palette)

        main_layout.addWidget(self.blank_panel, stretch=3)

        # Panel derecho (tabla y botones)
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Articulación", "Ángulo (°)", "Máximo (°)", "Mínimo (°)"])
        self.table.setStyleSheet(
            "QTableWidget { background-color: #f0f0f0; font-size: 14px; } "
            "QHeaderView::section { background-color: #d0d0d0; font-weight: bold; padding: 4px; border: 1px solid #a0a0a0; }"
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumWidth(400)

        self.joints = {
            "Tobillo R": [0, 0, 0],
            "Tobillo L": [0, 0, 0],
            "Rodilla R": [0, 0, 0],
            "Rodilla L": [0, 0, 0],
            "Cadera R": [0, 0, 0],
            "Cadera L": [0, 0, 0],
            "Hombro R": [0, 0, 0],
            "Hombro L": [0, 0, 0],
            "Codo R": [0, 0, 0],
            "Codo L": [0, 0, 0],
            "Muñeca R": [0, 0, 0],
            "Muñeca L": [0, 0, 0],
            "Cuello": [0, 0, 0]
        }

        self.table.setRowCount(len(self.joints))
        for row, joint in enumerate(self.joints):
            self.table.setItem(row, 0, QTableWidgetItem(joint))

        self.table.setMinimumHeight(400)
        self.table.resizeRowsToContents()

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        right_layout.addWidget(self.table)

        #Boton de análisis
        boton_info = QPushButton("Analisis")
        #boton_info.clicked.connect() TODO: Implementar la accion del boton de analisis
        right_layout.addWidget(boton_info)

        #Añadimos el panel derecho al layout principal
        main_layout.addWidget(right_panel, stretch=1)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def ObtainCamAvailable(self):
        """Obtener las cámaras disponibles y agregarlas al menú de configuración."""

        #Obtenemos las cámaras disponibles
        cameras = QCameraInfo.availableCameras()
        self.list_cam = [cam.description() for cam in cameras]
        if not self.list_cam:
            self.list_cam.append("No hay cámaras disponibles")
            return

    def update_angles(self, angles):
        for joint, angle in angles.items():
            actual = angle
            max_val = self.joints[joint][1]
            min_val = self.joints[joint][2]

            row = list(self.joints.keys()).index(joint)
            self.table.setItem(row, 1, QTableWidgetItem(f"{actual:.2f}"))

            if actual > max_val:
                self.joints[joint][1] = actual
            if actual < min_val or min_val == 0:
                self.joints[joint][2] = actual

            self.table.setItem(row, 2, QTableWidgetItem(f"{self.joints[joint][1]:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{self.joints[joint][2]:.2f}"))

        self.table.resizeRowsToContents()


def update_test_angles(window: BiomecanicaUI):
    angles = {}
    for joint in window.joints:
        new_angle = np.random.uniform(30, 160)
        window.joints[joint][0] = new_angle
        angles[joint] = new_angle
    window.update_angles(angles)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BiomecanicaUI()
    window.show()

    timer = QTimer()
    timer.timeout.connect(lambda: update_test_angles(window))
    timer.start(1000)

    sys.exit(app.exec_())
