import sys
import os
import numpy as np

# Configuración para mejorar compatibilidad con OpenGL en Linux
os.environ['QT_QPA_PLATFORM'] = 'xcb'  # Forzar X11 en lugar de Wayland
os.environ['PYOPENGL_PLATFORM'] = 'glx'

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QTableWidget, QTableWidgetItem, QMessageBox, QPushButton,
    QLabel, QGridLayout, QStackedWidget, QSizePolicy
)
from PyQt5.QtCore import QTimer, Qt
import pyqtgraph.opengl as gl
from PyQt5.QtWidgets import QHeaderView, QAction, QActionGroup, QMenu
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtGui import QPalette, QColor,QPixmap


class BiomecanicaUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analisis Biomecanico 3D")
        self.setGeometry(100, 100, 1800, 900)

        # --- Barra de menu ---
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Archivo")
        visualization_menu = menubar.addMenu("Visualizacion")
        config_menu = menubar.addMenu("Configuracion")
        help_menu = menubar.addMenu("Ayuda")

        #Exportar datos
        export_action = QAction("Exportar Datos", self)
        file_menu.addAction(export_action)

        # Seleccion de vista
        visualization_group = QActionGroup(self)
        visualization_group.setExclusive(True)
        view_2d_action = QAction("Vista Imagen", self, checkable=True)
        view_3d_action = QAction("Vista 3D", self, checkable=True)
        visualization_group.addAction(view_2d_action)
        visualization_group.addAction(view_3d_action)
        visualization_menu.addAction(view_2d_action)
        visualization_menu.addAction(view_3d_action)

        #TODO: Implementar la acciones de cambio de vista
        self.camaras_configuradas = True #TODO: Cambiar esto cuando se implementen la configuracion de camaras
        view_2d_action.triggered.connect(lambda: self.cambiar_vista("2D"))
        view_3d_action.triggered.connect(lambda: self.cambiar_vista("3D"))

        #Menu de configuracion
        self.list_cam = ["Cam 1", "Cam 2", "Cam 3", "Cam 4"]
        # self.ObtainCamAvailable() TODO:

        #Visualizar camaras disponibles
        cam_menu = QMenu("Camaras Disponibles", self)
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
        conf_cam_menu = QAction("Configuracion de Camaras", self)
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
                                                                        "Aplicacion de Bikefitting basada en vision artificial.\n\n"
                                                                        "Desarrollada por: Castro-3034-tbr\n\n"
                                                                        "Version 1.0\n\n"))
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

        #Panel 3D
        self.vista_3d = gl.GLViewWidget()  # Aquí ponerás tu vista 3D real (por ahora placeholder)
        self.vista_3d.setStyleSheet("background-color: lightgray;")

        # Variables para controlar la inicialización del 3D
        self.exoesqueleto_items = []
        self.skeleton_points = np.array([
                # Torso central
                [0, 0, 0],          # 0: Pelvis
                [0, 0, 5.5],        # 1: Cuello
                [0, 0, 8],          # 2: Cabeza

                # Pierna derecha
                [1, 0, 0],          # 3: Cadera R
                [1, 0, -4.5],       # 4: Rodilla R
                [1, 0, -9],         # 5: Tobillo R
                [1, 1, -9],         # 6: Pie R

                # Pierna izquierda
                [-1, 0, 0],         # 7: Cadera L
                [-1, 0, -4.5],      # 8: Rodilla L
                [-1, 0, -9],        # 9: Tobillo L
                [-1, 1, -9],        # 10: Pie L

                # Brazo derecho
                [2, 0, 5.5],        # 11: Hombro R
                [3, 0, 2.5],        # 12: Codo R
                [4, 0, 0],          # 13: Muñeca R
                [4, 1, 0],          # 14: Mano R

                # Brazo izquierdo
                [-2, 0, 5.5],       # 15: Hombro L
                [-3, 0, 2.5],       # 16: Codo L
                [-4, 0, 0],         # 17: Muñeca L
                [-4, 1, 0],       # 18: Mano L
            ], dtype=np.float32)
        self.gl_initialized = False

        # Panel 2D (cuadrícula de las 4 cámaras)
        self.vista_2d = QWidget()
        grid = QGridLayout(self.vista_2d)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(2)

        # Crear 4 etiquetas de cámara dinámicas
        self.cam_labels = []
        for i, vista in enumerate(self.list_cam):
            lbl = QLabel(vista)
            lbl.setStyleSheet("background-color: black; color: white; border: 1px solid gray;")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.cam_labels.append(lbl)
            grid.addWidget(lbl, i // 2, i % 2)

        #Stacked widget para cambiar entre vistas
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.blank_panel)  # Panel en blanco
        self.stacked_widget.addWidget(self.vista_3d)  # Panel 3D
        self.stacked_widget.addWidget(self.vista_2d)  # Panel 2D

        main_layout.addWidget(self.stacked_widget, stretch=3)
        self.stacked_widget.setCurrentIndex(0)  # Empezar con el panel en blanco

        # Panel derecho (tabla y botones)
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Articulacion", "Angulo (°)", "Maximo (°)", "Minimo (°)"])
        self.table.setStyleSheet(
            "QTableWidget { background-color: #f0f0f0; font-size: 14px; } "
            "QHeaderView::section { background-color: #d0d0d0; font-weight: bold; padding: 4px; border: 1px solid #a0a0a0; }"
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumWidth(400)

        self.angles_joints = {
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

        self.table.setRowCount(len(self.angles_joints))
        for row, joint in enumerate(self.angles_joints):
            self.table.setItem(row, 0, QTableWidgetItem(joint))

        self.table.setMinimumHeight(400)
        self.table.resizeRowsToContents()

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        right_layout.addWidget(self.table)

        #Boton de analisis
        boton_info = QPushButton("Analisis")
        #boton_info.clicked.connect() TODO: Implementar la accion del boton de analisis
        right_layout.addWidget(boton_info)

        #Añadimos el panel derecho al layout principal
        main_layout.addWidget(right_panel, stretch=1)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Inicializar 3D despues de que todo este configurado
        self.init_3d_timer = QTimer()
        self.init_3d_timer.setSingleShot(True)
        self.init_3d_timer.timeout.connect(self.initialize_3d_when_ready)
        self.init_3d_timer.start(100)  # Esperar 100ms

    def ObtainCamAvailable(self):
        """Obtener las camaras disponibles y agregarlas al menu de configuracion."""

        #Obtenemos las camaras disponibles
        cameras = QCameraInfo.availableCameras()
        self.list_cam = [cam.description() for cam in cameras]
        if not self.list_cam:
            self.list_cam.append("No hay camaras disponibles")
            return

    def cambiar_vista(self, vista):
        """Funcion para cambiar la vista de visualizacion."""
        if not self.camaras_configuradas:
            # Si no estan configuradas las camaras, forzar panel blanco
            self.stacked_widget.setCurrentIndex(0)
            return

        if vista == "3D":
            # Asegurar que el 3D este inicializado antes de mostrar
            if not self.gl_initialized:
                self.initialize_3d_when_ready()
            self.stacked_widget.setCurrentIndex(1)
        elif vista == "2D":
            self.stacked_widget.setCurrentIndex(2)

    def update_angles(self):
        for joint, angle in self.angles_joints.items():
            actual = angle[0]
            max_val = angle[1]
            min_val = angle[2]

            row = list(self.angles_joints.keys()).index(joint)
            self.table.setItem(row, 1, QTableWidgetItem(f"{actual:.2f}"))

            if actual > max_val:
                self.angles_joints[joint][1] = actual
            if actual < min_val or min_val == 0:
                self.angles_joints[joint][2] = actual

            self.table.setItem(row, 2, QTableWidgetItem(f"{self.angles_joints[joint][1]:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{self.angles_joints[joint][2]:.2f}"))

        self.table.resizeRowsToContents()

    def config_exoesqueleto(self):
        """Funcion que se usa para configurar el exoesqueleto de forma segura."""
        try:
            # Limpiar elementos anteriores si existen
            if hasattr(self, 'exoesqueleto_items'):
                for item in self.exoesqueleto_items:
                    if item is not None:
                        self.vista_3d.removeItem(item)

            self.exoesqueleto_items = []

            # Añadir grilla de referencia
            grid = gl.GLGridItem()
            grid.setSize(10, 10)
            grid.setSpacing(1, 1)
            self.vista_3d.addItem(grid)
            self.exoesqueleto_items.append(grid)

            # Configurar la vista 3D
            self.vista_3d.setCameraPosition(distance=20, elevation=20, azimuth=45)

            # Crear exoesqueleto básico
            self.create_basic_skeleton()

            self.gl_initialized = True

        except Exception as e:
            print(f"Error configurando exoesqueleto 3D: {e}")
            # Fallback: solo mostrar grilla básica
            try:
                grid = gl.GLGridItem()
                self.vista_3d.addItem(grid)
            except:
                pass

    def create_basic_skeleton(self):
        """Crea un exoesqueleto basico y robusto."""
        try:
            # Definir puntos del exoesqueleto (escalados para mejor visualizacion)

            joint_points = np.array([
                self.skeleton_points[1],  # Cuello
                self.skeleton_points[3],  # Cadera R
                self.skeleton_points[4],  # Rodilla R
                self.skeleton_points[5],  # Tobillo R
                self.skeleton_points[7],  # Cadera L
                self.skeleton_points[8],  # Rodilla L
                self.skeleton_points[9],  # Tobillo L
                self.skeleton_points[11], # Hombro R
                self.skeleton_points[12], # Codo R
                self.skeleton_points[13], # Muñeca R
                self.skeleton_points[15], # Hombro L
                self.skeleton_points[16], # Codo L
                self.skeleton_points[17], # Muñeca L
            ])

            # Definir conexiones entre puntos
            connections = [

                # Columna vertebral
                (0, 1), (1, 2),

                # Conexiones a extremidades
                (0, 3), (0, 7),    # Pelvis a caderas
                (1, 11), (1, 15),  # Cuello a hombros

                # Pierna derecha
                (0, 3), (3, 4), (4, 5), (5, 6),

                # Pierna izquierda
                (0, 7), (7, 8), (8, 9), (9, 10),

                # Brazo derecho
                (1, 11), (11, 12), (12, 13), (13, 14),

                # Brazo izquierdo
                (1, 15), (15, 16), (16, 17), (17, 18),
            ]

            # Crear puntos articulares
            scatter = gl.GLScatterPlotItem(
                pos=joint_points,
                size=1,
                color=(1, 0, 0, 0.8),  # Rojo semi-transparente
                pxMode=False
            )
            self.vista_3d.addItem(scatter)
            self.exoesqueleto_items.append(scatter)

            # Crear lineas de conexion
            for start_idx, end_idx in connections:
                try:
                    line_points = np.array([
                        self.skeleton_points[start_idx],
                        self.skeleton_points[end_idx]
                    ])

                    line = gl.GLLinePlotItem(
                        pos=line_points,
                        color=(0.8, 0.8, 0.8, 1.0),  # Gris
                        width=2,
                        antialias=True
                    )
                    self.vista_3d.addItem(line)
                    self.exoesqueleto_items.append(line)
                except Exception as e:
                    print(f"Error creando linea {start_idx}-{end_idx}: {e}")
                    continue

        except Exception as e:
            print(f"Error creando exoesqueleto basico: {e}")

    def actualizar_points(self, angles):
        """Actualizamos los puntos de exoesqueleto segun los angulos de cada una de las articulaciones."""
        pass

    def initialize_3d_when_ready(self):
        """Inicializa los elementos 3D cuando el widget este listo."""
        if not self.gl_initialized:
            try:
                self.config_exoesqueleto()
            except Exception as e:
                print(f"Error en inicializacion 3D: {e}")

def update_test_angles(window: BiomecanicaUI):
    """Funcion que usamos para probar la actualizacion de angulos"""

    # Actualizamos los angulos de las articulaciones con valores aleatorios entre 30 y 160 grados
    for joint in window.angles_joints:
        new_angle = np.random.uniform(30, 160)
        window.angles_joints[joint][0] = new_angle

    window.update_angles()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BiomecanicaUI()
    window.show()

    timer = QTimer()
    timer.timeout.connect(lambda: update_test_angles(window))
    timer.start(1000)

    sys.exit(app.exec_())
