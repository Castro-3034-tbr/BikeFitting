# 🚴 Biomecanica de Ciclistas basada en Vision Artificial

Este proyecto tiene como objetivo analizar la **biomecanica de un ciclista** en tiempo real utilizando **vision artificial**, una **webcam** y un modelo de **deteccion de poses YOLOv11**. Se calcula una serie de angulos articulares clave a partir de los puntos corporales detectados, con fines de analisis postural, optimizacion del rendimiento y prevencion de lesiones.


## 📌 Objetivo

Desarrollar una herramienta capaz de capturar y analizar los movimientos clave de un ciclista durante el pedaleo para:

- Evaluar la postura y simetria corporal.
- Medir angulos articulares relevantes en miembros superiores e inferiores.
- Identificar posibles desalineaciones o sobrecargas.
- Proporcionar feedback visual y cuantitativo sobre la tecnica de pedaleo.


## 📖 Tabla de Contenidos
- [🚴 Biomecanica de Ciclistas basada en Vision Artificial](#-biomecanica-de-ciclistas-basada-en-vision-artificial)
  - [📌 Objetivo](#-objetivo)
  - [📖 Tabla de Contenidos](#-tabla-de-contenidos)
  - [🧰 Tecnologias utilizadas](#-tecnologias-utilizadas)
  - [📦 Estructura de Carpetas](#-estructura-de-carpetas)
  - [⚙️ Requisitos](#️-requisitos)
  - [📥​ Instalacion](#-instalacion)
  - [▶️​ Ejecucion](#️-ejecucion)
  - [🧠 Explicacion del Codigo](#-explicacion-del-codigo)
  - [📊 Resultados Actuales](#-resultados-actuales)
  - [Interfaz Grafica](#interfaz-grafica)
    - [1. Ventana Principal](#1-ventana-principal)
      - [1. Diseno de interfaz](#1-diseno-de-interfaz)
      - [Vistas](#vistas)
    - [2. Pagina de Analisis](#2-pagina-de-analisis)
    - [3. Pagina de Exportacion (Generacion de PDF)](#3-pagina-de-exportacion-generacion-de-pdf)
    - [4. Pagina de Configuracion de camaras](#4-pagina-de-configuracion-de-camaras)
  - [📩 Contacto](#-contacto)

## 🧰 Tecnologias utilizadas

- **Python 3.X**: Lenguaje principal.
- **OpenCV**: Procesamiento y visualizacion de video.
- **Ultralytics YOLOv11**: Modelo de deteccion de poses.
- **NumPy**: Calculos numericos y vectores.
- **math**: Calculo de angulos en coordenadas polares.
- **Ultralytics SDK**: Para entrenamiento y pruebas.

## 📦 Estructura de Carpetas
```
Biomecanica/
├── pdf/                    # Carpeta donde se almacenan los documentos PDF generados
├── .images/                # Carpeta donde se almacenan las imagenes generadas
├── .images_readme/         # Carpeta donde se almacenan las imagenes para el README
│   ├── ImagenCofCam.jpg
│   └── logo.png
├── models/                # Carpeta que contiene el modelo YOLOv11
├── test/                  # Carpeta para pruebas
├── data/                  # Funciones utilitarias para el analisis
├── GUI.py                  # Interfaz grafica de usuario
├── ExportPDF.py            # Funciones para exportar a PDF
├── main.py                # Archivo principal que ejecuta el analisis
├── train.py               # Script para entrenar el modelo YOLOv11
├── requirements.txt       # Archivo de dependencias del proyecto
└── README.md               # Documentacion del proyecto
```

## ⚙️ Requisitos
- Python 3.8 o superior
- NumPy
- PyQt5
- PyQtGraph
- Matplotlib
- ReportLab
- Pillow
- OpenCV ≥ 4.5
- Ultralytics ≥ 8.x

Instala todo con:
```bash
pip install -r requirements.txt
```

## 📥​ Instalacion
1. Clona el repositorio:
   ```bash
   git clone https://github.com/Castro-3034-tbr/Biomecanica.git
   cd Biomecanica
   ```
2. Coloca el modelo entrenado YOLOv11 en models/best_Pose.pt.

   📌 Puedes entrenar el modelo tu mismo siguiendo los pasos de la siguiente seccion o solicitar el modelo entrenado.



## ▶️​ Ejecucion
Para analizar una imagen o un video, ejecuta el siguiente comando:
```bash
python main.py
```

## 🧠 Explicacion del Codigo
`main.py` – Analisis biomecanico a partir de video o imagen

Este script es el nucleo funcional del sistema. Se encarga de:
1. **Cargar el modelo YOLOv11 Pose** desde `models/best_Pose.pt`.
2. **Leer el archivo de entrada** (imagen o video) especificado en `input_file`.
3. **Detectar keypoints** usando el modelo YOLOv11.
4. **Calcular angulos articulares** entre los puntos relevantes del cuerpo (rodillas, cadera, brazos, cabeza).
5. **Visualizar los angulos** en la imagen/video, dibujando lineas y arcos con OpenCV.
6. **Guardar los resultados** en un nuevo archivo de salida (`output_pose.jpg` o `output_pose_video.avi`).

Componentes principales:
- `CalculeAngles()`: calcula angulos entre tres puntos usando trigonometria.
- `Draw()`: dibuja los puntos, lineas y arcos que representan los angulos en pantalla.
- `AnalizarFrame()`: gestiona el analisis completo de un frame (deteccion + dibujo).
- `DrawAngles()`: renderiza los angulos calculados en una zona visible del frame.

Soporte para modo imagen y modo video, con generacion de salida para ambos.

`train_model.py` – Entrenamiento del modelo YOLOv11 Pose
Este script permite entrenar un modelo personalizado de deteccion de poses con YOLOv11.

**Flujo del entrenamiento:**
1. **Carga del modelo base** (`yolo11n-pose.pt`) desde la carpeta `models/`.
2. **Lectura del archivo de configuracion** data.yaml, que contiene:
   - Rutas a imagenes de entrenamiento y validacion.
   - Clases y formato del dataset (en este caso, keypoints).

3. **Ejecucion del proceso de entrenamiento** con los siguientes parametros:
   - epochs: numero total de epocas (por defecto 100).
   - imgsz: resolucion de entrada (640).
   - batch: tamano del batch.
   - device: GPU utilizada.
   - save_period: frecuencia con la que se guarda un checkpoint del modelo.

4. **Generacion de los pesos entrenados** dentro de `./runs/train/yolo11n-pose/.`

Este archivo utiliza la API de Ultralytics, por lo que se requiere tener instalada la version oficial del paquete ultralytics.

## 📊 Resultados Actuales
El sistema actual permite analizar biomecanicamente el pedaleo de un ciclista utilizando vision artificial con un modelo de pose basado en YOLOv11. Como se encuentra en una fase de prototipado los resultados no son de alta calidad. A continuacion se detallan las funcionalidades implementadas:

✅ Entrenamiento basico del modelo YOLOv11 Pose con un dataset de keypoints.

✅ Deteccion de keypoints anatomicos en ciclistas (hombros, cadera, rodillas, tobillos, etc.) a partir de imagenes o videos previamente grabados.

✅ Visualizacion sobrepuesta de los puntos clave, conexiones esqueleticas y elementos geometricos auxiliares como lineas o elipses.

✅ Calculo automatico de angulos articulares (por ejemplo, angulo rodilla-cadera-tobillo) con visualizacion directa sobre la imagen.

✅ Representacion grafica del angulo en pantalla y exportacion en formato visual del frame con anotaciones biomecanicas.


En resumen, se ha establecido un sistema base solido y funcional, sobre el cual se construira un conjunto de herramientas de analisis avanzado en las siguientes etapas del proyecto.

![Resultados](./ImagesReadme/ResultadoProto.jpg)

## Interfaz Grafica

### 1. Ventana Principal

La ventana principal actua como el nucleo de la aplicacion, proporcionando un acceso centralizado a todas las funciones del sistema de analisis biomecanico.
Desde aqui, el usuario puede navegar a las diferentes secciones, configurar el entorno de analisis, iniciar sesiones de captura y generar informes PDF.
![Imagen de la Ventana Principal](.images_readme/principal_window.png)

#### 1. Diseno de interfaz

- Basada en PyQt5 con una disposicion QVBoxLayout y QGridLayout para estructurar los componentes.

- Barra de herramientas y menus superiores para acceso rapido a funciones criticas. Divididos en cuatro menus diferentes:
  1. **Archivo**: Opciones para guardar y exportar datos mediante PDF y boton para salir.
  2. **Visualizacion**: Cambia entre los diferentes modos de visualizacion de datos entre Vista 2D y 3D. Para el cambio de vista es necesario configurar dos camaras, para ambos laterales.
  3. **Configuracion**: Ajustes de camaras. Cuenta con la lista de camaras disponibles y la ejecucion del menu de configuracion de camaras.
  4. **Ayuda**: Acceso al repositorio de GitHub del proyecto y contacto.

- La **vista principal** se muestra en la izquierda las vistas configurables y en la derecha se muestra una tabla los angulos. Se muestra el angulo local, el valor maximo del angulo y el valor minimo del angulo.

#### Vistas
- **Vista 2D**: Representacion sobre las imagen capturada por la imagen, la informacion de los angulos

![Imagen de la Vista 2D](.images_readme/vista_2d_window.png)

- **Vista 3D**: Representacion tridimensional de la posicion actual. (Se encuentra en desarrollo debido a errores de visualizacion)
![Imagen de la Vista 3D](.images_readme/vista_3d_window.png)

### 2. Pagina de Analisis

La pagina de analisis es el entorno principal para visualizar y procesar los datos biomecanicos.

- **Visualizacion grafica en tiempo real** mediante *PyQtGraph*.
- **Secciones divididas**:  
  - Graficas comparativa de los angulos de cada articulacion respecto el rango de angulos optimo.
  - Trayectoria de los puntos clave de la rodilla y el tobillo.
- Controles para **reiniciar** los datos actuales.
  
![Imagen de la Pagina de Analisis](.images_readme/analisis_window.png)

### 3. Pagina de Exportacion (Generacion de PDF)

En esta seccion el usuario puede **generar un informe en formato PDF** con los resultados del analisis.

- Boton principal para **exportar resultados**.
- Generacion de documento PDF con:
  - Tabla de angulos maximos y minimos
  - Graficas comparativa de los angulos de cada articulacion respecto el rango de angulos optimo.
  - Grafica de las trayectoria de los puntos clave del tobillo y de la rodilla

- Flujo optimizado para que el usuario no necesite guardar las graficas manualmente; estas se extraen directamente.

![Imagen de la Pagina de Exportacion](.images_readme/export_window.png)

### 4. Pagina de Configuracion de camaras

Permite ajustar la posicion de las camaras respecto al sujeto:

![Imagen de la Pagina de Configuracion de Camaras](.images_readme/config_cam_window.png)


## 📩 Contacto

Para dudas, propuestas de colaboracion o comentarios tecnicos:

📧 [danielcastrogomezzz@gmail.com](mailto:danielcastrogomezzz@gmail.com)
GitHub: [Castro-3034-tbr](https://github.com/Castro-3034-tbr)
