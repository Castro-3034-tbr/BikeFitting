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

    def safe_quit(self):
        """Funcion para cerrar la aplicación de forma segura."""
        # Detener timers antes de cerrar
        if hasattr(self, 'init_3d_timer') and self.init_3d_timer.isActive():
            self.init_3d_timer.stop()
        if hasattr(self, 'analisis_window') and hasattr(self.analisis_window, 'timer'):
            self.analisis_window.timer.stop()
        self.close()

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

            # Crear exoesqueleto basico
            if self.vista_3d.isVisible():
                print("Actualizando exoesqueleto 3D...")
                self.update_skeleton_safe()
            else:
                print("Vista 3D no disponible arriba.")

            self.gl_initialized = True

        except Exception as e:
            print(f"Error configurando exoesqueleto 3D: {e}")
            # Fallback: solo mostrar grilla basica
            try:
                grid = gl.GLGridItem()
                self.vista_3d.addItem(grid)
            except:
                pass

    def update_skeleton_safe(self):
        self.vista_3d.makeCurrent()  # Activa el contexto de esta vista
        self.update_skeleton()
        self.vista_3d.doneCurrent()  # Libera el contexto
    
    def update_skeleton(self):
        """Crea un exoesqueleto básico y robusto con validaciones de depuración."""
        try:
            # --- Comprobaciones iniciales ---
            if not hasattr(self, 'vista_3d') or self.vista_3d is None:
                print("❌ No existe vista_3d")
                return
            if not self.vista_3d.isVisible():
                print("❌ vista_3d no está visible")
                return

            print(f"Vista disponible: {self.vista_3d is not None}, visible: {self.vista_3d.isVisible()}")

            # --- Borrar exoesqueleto anterior ---
            if hasattr(self, 'exoesqueleto_items'):
                for item in self.exoesqueleto_items:
                    try:
                        self.vista_3d.removeItem(item)
                    except Exception as e:
                        print(f"⚠️ Error eliminando item: {e}")
                self.exoesqueleto_items.clear()
            else:
                self.exoesqueleto_items = []

            # --- Validar datos de articulaciones ---
            if not hasattr(self, 'joint_points') or not isinstance(self.joint_points, np.ndarray):
                print("❌ joint_points no definido o no es np.ndarray")
                return
            if self.joint_points.ndim != 2 or self.joint_points.shape[1] != 3:
                print(f"❌ joint_points con forma inválida: {self.joint_points.shape}")
                return
            if np.any(np.isnan(self.joint_points)) or np.any(np.isinf(self.joint_points)):
                print("❌ joint_points contiene NaN o Inf")
                return

            # --- Crear puntos articulares ---
            scatter = gl.GLScatterPlotItem(
                pos=self.joint_points,
                size=1,
                color=(1, 0, 0, 0.8),  # Rojo semi-transparente
                pxMode=False
            )
            
            ctx = QtGui.QOpenGLContext.currentContext()
            print("Contexto activo:", ctx)
            print("Contexto esperado:", self.vista_3d.context())

            if ctx != self.vista_3d.context():
                print("⚠️ El contexto activo NO es el de la vista_3d. El dibujo no funcionará.")
            self.vista_3d.addItem(scatter)
            self.exoesqueleto_items.append(scatter)

            # --- Validar skeleton_points ---
            if not hasattr(self, 'skeleton_points') or not isinstance(self.skeleton_points, np.ndarray):
                print("❌ skeleton_points no definido o no es np.ndarray")
                return
            if self.skeleton_points.ndim != 2 or self.skeleton_points.shape[1] != 3:
                print(f"❌ skeleton_points con forma inválida: {self.skeleton_points.shape}")
                return
            if np.any(np.isnan(self.skeleton_points)) or np.any(np.isinf(self.skeleton_points)):
                print("❌ skeleton_points contiene NaN o Inf")
                return

            # --- Validar conexiones ---
            if not hasattr(self, 'connections') or not isinstance(self.connections, (list, tuple)):
                print("❌ connections no definido o no es lista/tupla")
                return

            for start_idx, end_idx, joint_idx, link_idx in self.connections:
                if (start_idx >= len(self.skeleton_points) or end_idx >= len(self.skeleton_points)
                    or start_idx < 0 or end_idx < 0):
                    print(f"⚠️ Índices fuera de rango: {start_idx}, {end_idx}")
                    continue

                try:
                    line_points = np.array([
                        self.skeleton_points[start_idx],
                        self.skeleton_points[end_idx]
                    ], dtype=float)

                    # Validar coordenadas de la línea
                    if np.any(np.isnan(line_points)) or np.any(np.isinf(line_points)):
                        print(f"⚠️ Línea {start_idx}-{end_idx} con valores inválidos")
                        continue

                    line = gl.GLLinePlotItem(
                        pos=line_points,
                        color=(0.8, 0.8, 0.8, 1.0),  # Gris
                        width=2,
                        antialias=True
                    )
                    self.vista_3d.addItem(line)
                    self.exoesqueleto_items.append(line)
                except Exception as e:
                    print(f"❌ Error creando línea {start_idx}-{end_idx}: {e}")
                    continue

            print(f"✅ Exoesqueleto creado con {len(self.exoesqueleto_items)} elementos.")

        except Exception as e:
            print(f"❌ Error en update_skeleton: {e}")


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

        #Comprobamos que la vista 3D esta visible
        if not self.vista_3d.isVisible():
            print("ABAJO: No esta visible la vista 3D")
            return

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

        # Actualizamos los puntos articulares
        self.update_skeleton_safe()

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