from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage
import cv2 as cv
from ultralytics import YOLO

import os

# Configuracion para mejorar compatibilidad con OpenGL en Linux
os.environ['QT_QPA_PLATFORM'] = 'xcb'  # Forzar X11 en lugar de Wayland
os.environ['PYOPENGL_PLATFORM'] = 'glx'
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "/usr/lib/qt/plugins/platforms"


from GUI import BiomecanicaUI
from functions import AnalizarFrame

def setup():
    """
    Funcion de configuracion de la aplicacion

    Funcion que usamos para configurar la aplicacion, cuando camaras configuradas pasa a valer True la primera vez
    """
    
    global MainWindow, camaras_obj
    
    #Cargamos todas las camaras
    camaras = MainWindow.list_cam

    for name in camaras:
        #Obtenemos el ID de la camara
        id = name.replace("Camera ", "")
        
        #Intentamos cargar la camara
        cap = cv.VideoCapture(int(id))
        if not cap.isOpened():
            print(f"Error al abrir la camara {name} con ID {id}.")
        else:
            camaras_obj[name] = cap

def BuclePrincipal():
    """Bucle principal de la aplicacion.

    Raises:
        Exception: Si ocurre un error en el bucle.
    """
    #Importamos las variables globales
    global app, MainWindow, model, configurado, camaras_obj
    
    if not MainWindow.camaras_configuradas:
        #Si las camaras no estan configuradas, salimos
        return

    if not configurado:
        # Si no esta configurado, hacemos la configuracion
        setup()
        configurado = True
    
    #Bucle de captura y procesamiento
    for name, cap in camaras_obj.items():
        ret, frame = cap.read()
        if not ret:
            print(f"Error al leer el frame de la camara {name}.")
            continue
        
        #Analizamos el frame
        frame, angulos = AnalizarFrame(frame, model)

        #Obtenemos la vista de la camara
        vista = [k for k in MainWindow.cam_vista if MainWindow.cam_vista[k] == name]
        if vista:
            vista = vista[0]
        else:
            vista = None

        if vista == "Derecha":
            # Procesar la vista derecha
            MainWindow.angles_joints["Pelvis"][0] = angulos["Pelvis"]
            MainWindow.angles_joints["Cuello"][0] = angulos["Cuello"]
            MainWindow.angles_joints["Cadera R"][0] = angulos["Cadera"]
            MainWindow.angles_joints["Rodilla R"][0] = angulos["Rodilla"]
            MainWindow.angles_joints["Tobillo R"][0] = angulos["Tobillo"]
            MainWindow.angles_joints["Hombro R"][0] = angulos["Hombro"]
            MainWindow.angles_joints["Codo R"][0] = angulos["Codo"]
            MainWindow.angles_joints["Muneca R"][0] = angulos["Muneca"]

        elif vista == "Izquierda":
            MainWindow.angles_joints["Pelvis"][0] = angulos["Pelvis"]
            MainWindow.angles_joints["Cuello"][0] = angulos["Cuello"]
            MainWindow.angles_joints["Cadera L"][0] = angulos["Cadera"]
            MainWindow.angles_joints["Rodilla L"][0] = angulos["Rodilla"]
            MainWindow.angles_joints["Tobillo L"][0] = angulos["Tobillo"]
            MainWindow.angles_joints["Hombro L"][0] = angulos["Hombro"]
            MainWindow.angles_joints["Codo L"][0] = angulos["Codo"]
            MainWindow.angles_joints["Muneca L"][0] = angulos["Muneca"]

        #Actualizamos la vista 3D
        MainWindow.update_angles()

        if frame is not None:
            # OpenCV usa BGR, QImage espera RGB
            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            qimg = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            MainWindow.updateImagen(name, qimg)

#Cargamos el modelo
model = YOLO('./models/yolo11n-pose.pt')
if not model:
    raise Exception("Error al cargar el modelo.")
print("Modelo cargado correctamente.")

#Definimos las variables globales de control
configurado = False
camaras_obj= {}

#Iniciamos la interfaz grafica
app = QApplication([])
MainWindow = BiomecanicaUI()
MainWindow.show()

#Creamos un bucle de ejecucion
timer = QTimer()
timer.timeout.connect(BuclePrincipal)
timer.start(100)  # Ejecutar cada 100 ms

app.exec_()
