import sys
import os
import numpy as np
import pyqtgraph as pg

# Configuracion para mejorar compatibilidad con OpenGL en Linux
os.environ['QT_QPA_PLATFORM'] = 'xcb'  # Forzar X11 en lugar de Wayland
os.environ['PYOPENGL_PLATFORM'] = 'glx'

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QTableWidget, QTableWidgetItem, QMessageBox, QPushButton,
    QLabel, QGridLayout, QStackedWidget, QSizePolicy, QDialog, QComboBox,
)
from PyQt5.QtCore import QTimer, Qt
import pyqtgraph.opengl as gl
from PyQt5.QtWidgets import QHeaderView, QAction, QActionGroup, QMenu
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtGui import QPalette, QColor,QPixmap

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import random

#region: Main Window 
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
        conf_cam_menu.triggered.connect(self.open_configcam_window)
        config_menu.addAction(conf_cam_menu)

        # Accion salir
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Repo
        repo_action = QAction("Repositorio", self)
        repo_action.triggered.connect(lambda: QMessageBox.information(self, "Repositorio",
                                                                        "Visita nuestro repositorio en GitHub:\n\n"
                                                                        "https://github.com/tu-repo"))
        help_menu.addAction(repo_action)

        # Accion acerca de
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
        self.vista_3d = gl.GLViewWidget()  # Aqui pondras tu vista 3D real (por ahora placeholder)
        self.vista_3d.setStyleSheet("background-color: lightgray;")

        # Variables para controlar la inicializacion del 3D
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
                [2.5, 0, 5.5],        # 11: Hombro R
                [2.5, 0, 2.5],        # 12: Codo R
                [2.5, 0, 0],          # 13: Muneca R
                [2.5, 1, 0],          # 14: Mano R

                # Brazo izquierdo
                [-2.5, 0, 5.5],       # 15: Hombro L
                [-2.5, 0, 2.5],       # 16: Codo L
                [-2.5, 0, 0],         # 17: Muneca L
                [-2.5, 1, 0],       # 18: Mano L
            ], dtype=np.float32)

        self.joint_points = np.array([
                self.skeleton_points[0],  # 0: Pelvis
                self.skeleton_points[1],  # 1: Cuello
                self.skeleton_points[3],  # 2: Cadera R
                self.skeleton_points[4],  # 3: Rodilla R
                self.skeleton_points[5],  # 4: Tobillo R
                self.skeleton_points[7],  # 5: Cadera L
                self.skeleton_points[8],  # 6: Rodilla L
                self.skeleton_points[9],  # 7: Tobillo L
                self.skeleton_points[11], # 8: Hombro R
                self.skeleton_points[12], # 9: Codo R
                self.skeleton_points[13], # 10: Muneca R
                self.skeleton_points[15], # 11: Hombro L
                self.skeleton_points[16], # 12: Codo L
                self.skeleton_points[17], # 13: Muneca L
            ])

        self.angles_joints = {
            "Pelvis": [0, 0, 0],
            "Cuello": [0, 0, 0],
            "Cadera R": [0, 0, 0],
            "Rodilla R": [0, 0, 0],
            "Tobillo R": [0, 0, 0],
            "Cadera L": [0, 0, 0],
            "Rodilla L": [0, 0, 0],
            "Tobillo L": [0, 0, 0],
            "Hombro R": [0, 0, 0],
            "Codo R": [0, 0, 0],
            "Muneca R": [0, 0, 0],
            "Hombro L": [0, 0, 0],
            "Codo L": [0, 0, 0],
            "Muneca L": [0, 0, 0],
        }

            # Definir conexiones entre puntos (start_index, end_index, joint_index, link_index)
        self.connections = [
            # Columna vertebral
            (0, 1, 0, 0), (1, 2, 1, 1),
            # Pierna derecha
            (0, 3, None, None), (3, 4, 2, 2), (4, 5, 3, 3), (5, 6, 4, 4),
            # Pierna izquierda
            (0, 7, None, None), (7, 8, 5, 2), (8, 9, 6, 3), (9, 10, 7, 4),
            # Brazo derecho
            (1, 11, None, None), (11, 12, 8, 5), (12, 13, 9, 6), (13, 14, 10, 7),
            # Brazo izquierdo
            (1, 15, None, None), (15, 16, 11, 5), (16, 17, 12, 6), (17, 18, 13, 7),
        ]

        self.link_dimensions = np.array([
            #Dimension de cada una de los eslabones del exoesqueleto
            5.5,  #0: Tronco
            2.5,  #1: Cuello
            4.5,  #2: Muslo
            4.5,  #3: Pierna
            1.4,  #4: Pie
            3.0,  #5: Brazo
            2.5,  #6: Antebrazo
            1.0,  #7: Mano
        ])
        self.gl_initialized = False


        #Creamos las variables de guardado de valores
        self.valores_grafica_L = [[[],[]],[[],[]]]
        self.valores_grafica_R = [[[],[]],[[],[]]]

        # Panel 2D (cuadricula de las 4 camaras)
        self.vista_2d = QWidget()
        grid = QGridLayout(self.vista_2d)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(2)

        # Crear 4 etiquetas de camara dinamicas
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
        boton_info.clicked.connect(self.open_analisis_window)
        right_layout.addWidget(boton_info)

        # Señal para cerrar seguro
        self.app_quit_action = QAction("Salir", self)
        self.app_quit_action.triggered.connect(self.safe_quit)
        file_menu.addAction(self.app_quit_action)

        #Anadimos el panel derecho al layout principal
        main_layout.addWidget(right_panel, stretch=1)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        #Cremos las variables de las paguinas necesarias
        self.config_cam_window = ConfigCamWindow(self)
        self.analisis_window = AnalisisWindow(self)

    def ObtainCamAvailable(self):
        """Obtener las camaras disponibles y agregarlas al menu de configuracion. """

        #Obtenemos las camaras disponibles
        cameras = QCameraInfo.availableCameras()
        self.list_cam = [cam.description() for cam in cameras]
        if not self.list_cam:
            self.list_cam.append("No hay camaras disponibles")
            return

    def cambiar_vista(self, vista):
        """Funcion para cambiar la vista de visualizacion.
        INPUTS:
        vista: La vista a la que cambiar (2D o 3D)
        """
        if not self.camaras_configuradas:
            # Si no estan configuradas las camaras, forzar panel blanco
            self.stacked_widget.setCurrentIndex(0)

            # Mostrar mensaje de advertencia
            QMessageBox.warning(self, "Advertencia", "Por favor, configure las camaras antes de cambiar la vista. Minimo es necesario configurar la camara derecha y la izquierda.")

            return

        if vista == "3D":
            # Asegurar que el 3D este inicializado antes de mostrar
            self.stacked_widget.setCurrentIndex(1)
            QTimer.singleShot(1000, self.initialize_3d_when_ready)
        elif vista == "2D":
            self.stacked_widget.setCurrentIndex(2)

    def update_angles(self):
        """Funcion que usamos para actualizar los angulos de las articulaciones dentro de la tabla"""
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

            # Anadir grilla de referencia
            grid = gl.GLGridItem()
            grid.setSize(10, 10)
            grid.setSpacing(1, 1)
            self.vista_3d.addItem(grid)
            self.exoesqueleto_items.append(grid)

            # Configurar la vista 3D
            self.vista_3d.setCameraPosition(distance=20, elevation=20, azimuth=45)
            self.gl_initialized = True

        except Exception as e:
            print(f"Error configurando exoesqueleto 3D: {e}")
            # Fallback: solo mostrar grilla basica
            try:
                grid = gl.GLGridItem()
                self.vista_3d.addItem(grid)
            except:
                pass

    def update_skeleton(self):
        """Crea un exoesqueleto básico y robusto con validaciones de depuración."""
        pass


    def calcular_punto_3d(self, origen, longitud, theta):
        """Calcula un punto 3D a partir de un origen, longitud y angulos theta y phi.
        INPUTS:
        origen: El punto de origen (x, y, z)
        longitud: La longitud del segmento
        theta: El angulo en el plano XY
        OUTPUTS:
        Un punto 3D (x, y, z) como un array de numpy.
        """
        x = origen[0]
        y = origen[1] + longitud * np.cos(theta)
        z = origen[2] + longitud * np.sin(theta)
        return np.array([x, y, z], dtype=np.float32)

    def update_points(self):
        """Actualizamos los puntos de exoesqueleto segun los angulos de cada una de las articulaciones."""

        #Calculamos el punto para cada articulacion ( Vamos a probar con la cadera derecha, rodilla derecha y tobillo derecho )
        for i, conect in enumerate(self.connections):
            start_idx, end_idx, joint_idx, link_idx = conect
            if joint_idx is None or link_idx is None:
                continue
            #Obtenemos la informacion
            start_point = self.skeleton_points[start_idx]
            clave=list(self.angles_joints.keys())[joint_idx]
            angle = self.angles_joints[clave][0]
            angle = np.radians(angle)  # Convertir a radianes
            longitud = self.link_dimensions[link_idx]

            #calculamos el nuevo punto
            new_point = self.calcular_punto_3d(start_point, longitud, angle)

            if joint_idx in [2,3,4,5,6,7]:
                # Si es una articulacion de la pierna, invertimos el eje z
                new_point[2] = -new_point[2]

            self.skeleton_points[end_idx] = new_point
            self.joint_points[joint_idx] = new_point

    def initialize_3d_when_ready(self):
        """Inicializa los elementos 3D cuando el widget este listo."""
        if not self.gl_initialized:
            try:
                self.config_exoesqueleto()
            except Exception as e:
                print(f"Error en inicializacion 3D: {e}")

    def open_configcam_window(self):
        """Abre la ventana de configuracion de camaras."""
        self.config_cam_window = ConfigCamWindow(self)
        #Abrimos la ventana de configuracion de camaras
        self.config_cam_window.show()

    def open_analisis_window(self):
        """Abre la ventana de analisis de datos."""
        self.analisis_window = AnalisisWindow(self)
        #Abrimos la ventana de analisis de datos
        self.analisis_window.show()

#region: Config Cam Window
class ConfigCamWindow(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window  # acceso a la ventana principal
        self.setWindowTitle("Configuracion de Camaras")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Titulo arriba
        title = QLabel("Selecciona la camara correspondiente para cada vista")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # Contenedor central con imagen + combos
        center_layout = QGridLayout()
        layout.addLayout(center_layout)

        # Imagen central
        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap("./ImagenPrueba.jpg").scaled(300, 300, Qt.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(self.image_label, 1, 1)

        # Vistas y combos
        self.combo_boxes = {}
        self.add_view_combo(center_layout, "Frontal", 0, 1)
        self.add_view_combo(center_layout, "Izquierda", 1, 0)
        self.add_view_combo(center_layout, "Derecha", 1, 2)
        self.add_view_combo(center_layout, "Trasera", 2, 1)


    def add_view_combo(self, layout, name, row, col):
        """Crea una etiqueta + combo para una vista
        INPUTS:
        layout: El layout en el que añadir el combo
        name: El nombre de la vista
        row: La fila en la que colocar el combo
        col: La columna en la que colocar el combo
        """
        #Creamos la etiqueta
        vbox = QVBoxLayout()
        label = QLabel(name)
        label.setAlignment(Qt.AlignCenter)

        #Creamos el combo
        combo = QComboBox()
        combo.addItem("Sin asignar ")  # opcion en blanco
        combo.addItems(self.main_window.list_cam)  # Usar las camaras disponibles
        combo.currentIndexChanged.connect(self.update_combo_options)

        # Anadimos al layout
        vbox.addWidget(label)
        vbox.addWidget(combo)

    # Creamos un contenedor para el layout vertical
        container = QWidget()
        container.setLayout(vbox)
        container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)  # evita que se desplace mucho verticalmente

        # Anadimos el contenedor al layout principal
        layout.addWidget(container, row, col, alignment=Qt.AlignCenter)

        # Guardamos el combo en un diccionario para actualizaciones posteriores
        self.combo_boxes[name] = combo

    def update_combo_options(self):
        """Cuando cambia una seleccion, actualizamos el resto de combos."""

        selected = set()
        for name, combo in self.combo_boxes.items():
            text = combo.currentText()
            if text and text != "Sin asignar" and text != "":  # ignoramos si esta vacio
                selected.add(text)

        # Actualizamos combos
        for name, combo in self.combo_boxes.items():
            # Obtener el texto actual del combo
            current = combo.currentText()
            # Evitar senales para evitar bucles infinitos
            combo.blockSignals(True)

            # Limpiar el combo y anadir la opcion en blanco
            combo.clear()
            combo.addItem("Sin asignar")  # opcion en blanco

            # Mostrar solo las camaras no seleccionadas o la actual
            options = [cam for cam in self.main_window.list_cam if cam == current or cam not in selected]
            combo.addItems(options)

            # Si la opcion actual esta en las opciones disponibles, la seleccionamos
            if current in options or current == "Sin asignar":
                combo.setCurrentText(current)

            combo.blockSignals(False)

        #Comprobamos si la configuracion es la minima necesaria
        self.check_config()

    def check_config(self):
        """Verifica que tenemos la configuracion necesaria de camaras para iniciar el analisis."""

        #Obtenemos el valor de los boxes izquierdos y derechos
        left_value = self.combo_boxes["Izquierda"].currentText()
        right_value = self.combo_boxes["Derecha"].currentText()

    #Comprobamos que no esten vacios
        if left_value != "Sin asignar" or right_value != "Sin asignar" or left_value != "" or right_value != "":
            #Si tenemos configuracion minima, habilitamos el boton de analisis
            self.main_window.camaras_configuradas = True


#region: Analisis window
class AnalisisWindow(QDialog):
    """Ventana de analisis de datos biomecanicos."""
    def __init__(self, main_window=None):
        super().__init__(main_window)
        self.main_window = main_window
        self.setWindowTitle("Analisis de Datos")
        self.setGeometry(100, 100, 1800, 1800)

        # Layout principal vertical
        main_vlayout = QVBoxLayout(self)

    # ===== Grid superior unico 7x4 =====
        self.grid_superior = QGridLayout()
        main_vlayout.addLayout(self.grid_superior)

        self.optimal_ranges = [
        ("Pelvis", [[0, 360], [0, 360]]),
        ("Cuello", [[0, 360], [0, 360]]),
        ("Cadera R", [[0, 360], [0, 360]]),
        ("Rodilla R", [[0, 360], [0, 360]]),
        ("Tobillo R", [[0, 360], [0, 360]]),
        ("Cadera L", [[0, 360], [0, 360]]),
        ("Rodilla L", [[0, 360], [0, 360]]),
        ("Tobillo L", [[0, 360], [0, 360]]),
        ("Hombro R", [[0, 360], [0, 360]]),
        ("Codo R", [[0, 360], [0, 360]]),
        ("Muneca R", [[0, 360], [0, 360]]),
        ("Hombro L", [[0, 360], [0, 360]]),
        ("Codo L", [[0, 360], [0, 360]]),
        ("Muneca L", [[0, 360], [0, 360]])
        ]


        #Dividimos el rango en dos
        mitad1 = self.optimal_ranges[:len(self.optimal_ranges)//2]
        mitad2 = self.optimal_ranges[len(self.optimal_ranges)//2:]

        #Creamos los conjuntos de graficas
        self.fig,axes = plt.subplots(
            nrows=max(len(mitad1), len(mitad2)),
            ncols=4,
            figsize=(12, len(mitad1) * 0.6),
            dpi=120
        )

        #Dibujamos los rangos
        self.line_refs = {}

        for row, data in enumerate(mitad1):
            name, (range1, range2) = data
            self.line_refs[(name, 0)] = self.draw_range_bar(axes[row, 0], f"Min: {name}", range1)
            self.line_refs[(name, 1)] = self.draw_range_bar(axes[row, 1], f"Max: {name}", range2)

        for row, data in enumerate(mitad2):
            name, (range1, range2) = data
            self.line_refs[(name, 0, 'R')] = self.draw_range_bar(axes[row, 2], f"Min: {name}", range1)
            self.line_refs[(name, 1, 'R')] = self.draw_range_bar(axes[row, 3], f"Max: {name}", range2)

        plt.tight_layout()

    #Anadimos la grafica al layout
        self.canvas = FigureCanvas(self.fig)
        main_vlayout.addWidget(self.canvas)

        # ===== Parte inferior: dos casillas =====
        bottom_layout = QGridLayout()
        main_vlayout.addLayout(bottom_layout)

        # Creamos una grafica
        self.grafica_L = pg.PlotWidget(title="Trayectoria Derecha")
        self.grafica_L.setFixedHeight(int(self.height() / 3))
        self.grafica_L.setAspectLocked(True)
        bottom_layout.addWidget(self.grafica_L, 0, 0)

        self.grafica_R = pg.PlotWidget(title="Trayectoria Izquierda")
        self.grafica_R.setFixedHeight(int(self.height() / 3))
        self.grafica_R.setAspectLocked(True)
        bottom_layout.addWidget(self.grafica_R, 0, 1)

        #Seteamos los limites TODO: Cambiar los rangos por los necesarios
        self.grafica_L.setLimits(xMin=0, xMax=100, yMin=0, yMax=100)
        self.grafica_R.setLimits(xMin=0, xMax=100, yMin=0, yMax=100)

        # Boton abajo
        boton = QPushButton("Reiniciar")
        main_vlayout.addWidget(boton)
        boton.clicked.connect(self.reiniciar_datos)

        #Creamos un reloj de actualizacion
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_trayectorias)
        self.timer.timeout.connect(self.update_bars)
        self.timer.start(1000)

    def reiniciar_datos(self):
        """Funcion que usamos para reiniciar todos los valores"""

        #Reiniciamos los maximos y minimos de los angulos
        #TODO:

        #Reiniciamos las trayectorias
        self.main_window.valores_grafica_L = [[[],[]],[[],[]]]
        self.main_window.valores_grafica_R = [[[],[]],[[],[]]]

    def update_trayectorias(self):
        """Actualiza las trayectorias de los graficos."""
         Removed 3D skeleton generation due to error. Implementation

        #Obtenemos los valores
        valores_L = self.main_window.valores_grafica_L
        valores_R = self.main_window.valores_grafica_R

        #Actualizmos la trayectoria derecha
        self.grafica_R.clear()
        self.grafica_R.plot(valores_R[0][0], valores_R[0][1], pen="r", name="Rodilla")
        self.grafica_R.plot(valores_R[1][0], valores_R[1][1], pen="g", name="Tobillo")
        self.grafica_R.addLegend()

        #Actualizamos la trayectoria izquierda
        self.grafica_L.clear()
        self.grafica_L.plot(valores_L[0][0], valores_L[0][1], pen="r", name="Rodilla")
        self.grafica_L.plot(valores_L[1][0], valores_L[1][1], pen="g", name="Tobillo")
        self.grafica_L.addLegend()


    def draw_range_bar(self, ax, name, range_values):
        """Dibuja una barra de rango en el grafico.
        INPUTS:
        ax: El eje en el que dibujar la barra
        name: El nombre de la barra
        range_values: Los valores de rango (inicio, fin)
        OUTPUTS:
        Una línea vertical que representa el rango en el gráfico.
        """
        start, end = range_values
        mid = (start + end) / 2
        values = np.linspace(start, end, 300)
        colors = []
        for val in values:
            dist = abs(val - mid) / ((end - start) / 2)
            green = max(0, 1 - dist)
            red = 1 - green
            colors.append((red, green, 0))
        ax.imshow([colors], extent=[start, end, 0, 1], aspect='auto')
        ax.set_yticks([])
        ax.set_xticks([start, mid, end])
        ax.set_xticklabels([f"{start}°", f"{mid:.1f}°", f"{end}°"], fontsize=7)
        ax.set_xlim(start, end)
        ax.set_title(name, fontsize=8)
        return ax.axvline(start - 1, color='black', linewidth=2)

    def update_bars(self):
        """Funcion que usamos para actualizar todos los valores"""
        # Evitar dibujar si la ventana no está visible
        if not self.isVisible():
            return

        # Actualizamos los valores de las barras de rango
        for key,line in self.line_refs.items():

            #Lado Izquierdo
            if len(key) == 2:
                name, col = key
                start, end = self.optimal_ranges[[n for n, _ in self.optimal_ranges].index(name)][1][col]

            #Lado Derecho
            else:
                name, col, _ = key
                start, end = self.optimal_ranges[[n for n, _ in self.optimal_ranges].index(name)][1][col]

            #Obtenemos el nuevo valor de angulo
            if col == 0:  # Minimo
                new_value = self.main_window.angles_joints[name][0] #TODO: Cambiar por 1 cuando este implementado
            else:  # Maximo
                new_value = self.main_window.angles_joints[name][0] #TODO: Cambiar por 2 cuando este implementado

            line.set_xdata([new_value])
        self.fig.canvas.draw_idle()


def update_trayectoria_test(window: BiomecanicaUI):
    """Funcion que usamos para calcular la trayectoria de prueba
    TODO: Esta es una funcion de prueba en la original no tiene que funcionar

    INPUTS:
    window: La ventana principal de la aplicacion
    """

    # Limpiamos las trayectorias anteriores
    window.valores_grafica_L = [[[], []], [[], []]]
    window.valores_grafica_R = [[[], []], [[], []]]

    #Obtenemos un radio aleatorio para cada una de las graficas
    radio1 = np.random.uniform(1, 10)
    radio2 = np.random.uniform(1, 10)
    radio3 = np.random.uniform(1, 10)
    radio4 = np.random.uniform(1, 10)

    # Generamos nuevos datos de prueba
    for i in range(0,360,15):
        i = np.radians(i)  # Convertir a radianes

        # Creamos una elipse con centro en (2, 4)
        window.valores_grafica_L[0][0].append(radio1*np.cos(i) + 20)
        window.valores_grafica_L[0][1].append(radio1*np.sin(i) + 40)

        window.valores_grafica_L[1][0].append(radio2*np.cos(i) + 20)
        window.valores_grafica_L[1][1].append(radio2*np.sin(i) + 60)

        # Datos para la grafica derecha
        window.valores_grafica_R[0][0].append(radio3*np.cos(i) + 20)
        window.valores_grafica_R[0][1].append(radio3*np.sin(i) + 40)

        window.valores_grafica_R[1][0].append(radio4*np.cos(i) + 20)
        window.valores_grafica_R[1][1].append(radio4*np.sin(i) + 60)

    # Actualizamos las graficas si la ventana de analisis esta abierta
    if not window.analisis_window is None and window.analisis_window.isVisible():
        window.analisis_window.update_trayectorias()


def update_test_angles(window: BiomecanicaUI):
    """Funcion que usamos para probar la actualizacion de angulos
    TODO: Esta es una funcion de prueba en la original no tiene que funcionar

    INPUTS:
    window: La ventana principal de la aplicacion

    """

    # Actualizamos los angulos de las articulaciones con valores aleatorios entre 30 y 160 grados
    for joint in window.angles_joints:
        new_angle = np.random.uniform(30, 160)
        window.angles_joints[joint][0] = new_angle

    window.update_angles()
    window.update_points()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BiomecanicaUI()
    window.show()

    timer = QTimer()
    timer.timeout.connect(lambda: update_test_angles(window))
    timer.timeout.connect(lambda: update_trayectoria_test(window))
    timer.start(1000)

    sys.exit(app.exec_())
