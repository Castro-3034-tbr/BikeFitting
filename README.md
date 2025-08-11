# 🚴 Biomecánica de Ciclistas basada en Visión Artificial

Este proyecto tiene como objetivo analizar la **biomecánica de un ciclista** en tiempo real utilizando **visión artificial**, una **webcam** y un modelo de **detección de poses YOLOv11**. Se calcula una serie de ángulos articulares clave a partir de los puntos corporales detectados, con fines de análisis postural, optimización del rendimiento y prevención de lesiones.


## 📌 Objetivo

Desarrollar una herramienta capaz de capturar y analizar los movimientos clave de un ciclista durante el pedaleo para:

- Evaluar la postura y simetría corporal.
- Medir ángulos articulares relevantes en miembros superiores e inferiores.
- Identificar posibles desalineaciones o sobrecargas.
- Proporcionar feedback visual y cuantitativo sobre la técnica de pedaleo.


## 📖 Tabla de Contenidos
- [🚴 Biomecánica de Ciclistas basada en Visión Artificial](#-biomecánica-de-ciclistas-basada-en-visión-artificial)
  - [📌 Objetivo](#-objetivo)
  - [📖 Tabla de Contenidos](#-tabla-de-contenidos)
  - [🧰 Tecnologías utilizadas](#-tecnologías-utilizadas)
  - [📦 Estructura de Carpetas](#-estructura-de-carpetas)
  - [⚙️ Requisitos](#️-requisitos)
  - [📥​ Instalacion](#-instalacion)
  - [▶️​ Ejecución](#️-ejecución)
  - [🧠 Explicación del Código](#-explicación-del-código)
  - [📊 Resultados Actuales](#-resultados-actuales)
  - [Interfaz Grafica](#interfaz-grafica)
    - [1. Ventana Principal](#1-ventana-principal)
      - [1. Diseño de interfaz](#1-diseño-de-interfaz)
      - [Vistas](#vistas)
    - [2. Página de Análisis](#2-página-de-análisis)
    - [3. Página de Exportación (Generación de PDF)](#3-página-de-exportación-generación-de-pdf)
    - [4. Página de Configuración de cámaras](#4-página-de-configuración-de-cámaras)
  - [📩 Contacto](#-contacto)

## 🧰 Tecnologías utilizadas

- **Python 3.X**: Lenguaje principal.
- **OpenCV**: Procesamiento y visualización de vídeo.
- **Ultralytics YOLOv11**: Modelo de detección de poses.
- **NumPy**: Cálculos numéricos y vectores.
- **math**: Cálculo de ángulos en coordenadas polares.
- **Ultralytics SDK**: Para entrenamiento y pruebas.

## 📦 Estructura de Carpetas
```
Biomecanica/
├── pdf/                    # Carpeta donde se almacenan los documentos PDF generados
├── .images/                # Carpeta donde se almacenan las imágenes generadas
├── .images_readme/         # Carpeta donde se almacenan las imágenes para el README
│   ├── ImagenCofCam.jpg
│   └── logo.png
├── models/                # Carpeta que contiene el modelo YOLOv11
├── test/                  # Carpeta para pruebas
├── data/                  # Funciones utilitarias para el análisis
├── GUI.py                  # Interfaz gráfica de usuario
├── ExportPDF.py            # Funciones para exportar a PDF
├── main.py                # Archivo principal que ejecuta el análisis
├── train.py               # Script para entrenar el modelo YOLOv11
├── requirements.txt       # Archivo de dependencias del proyecto
└── README.md               # Documentación del proyecto
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

   📌 Puedes entrenar el modelo tú mismo siguiendo los pasos de la siguiente sección o solicitar el modelo entrenado.



## ▶️​ Ejecución
Para analizar una imagen o un vídeo, ejecuta el siguiente comando:
```bash
python main.py
```

## 🧠 Explicación del Código
`main.py` – Análisis biomecánico a partir de vídeo o imagen

Este script es el núcleo funcional del sistema. Se encarga de:
1. **Cargar el modelo YOLOv11 Pose** desde `models/best_Pose.pt`.
2. **Leer el archivo de entrada** (imagen o vídeo) especificado en `input_file`.
3. **Detectar keypoints** usando el modelo YOLOv11.
4. **Calcular ángulos articulares** entre los puntos relevantes del cuerpo (rodillas, cadera, brazos, cabeza).
5. **Visualizar los ángulos** en la imagen/vídeo, dibujando líneas y arcos con OpenCV.
6. **Guardar los resultados** en un nuevo archivo de salida (`output_pose.jpg` o `output_pose_video.avi`).

Componentes principales:
- `CalculeAngles()`: calcula ángulos entre tres puntos usando trigonometría.
- `Draw()`: dibuja los puntos, líneas y arcos que representan los ángulos en pantalla.
- `AnalizarFrame()`: gestiona el análisis completo de un frame (detección + dibujo).
- `DrawAngles()`: renderiza los ángulos calculados en una zona visible del frame.

Soporte para modo imagen y modo vídeo, con generación de salida para ambos.

`train_model.py` – Entrenamiento del modelo YOLOv11 Pose
Este script permite entrenar un modelo personalizado de detección de poses con YOLOv11.

**Flujo del entrenamiento:**
1. **Carga del modelo base** (`yolo11n-pose.pt`) desde la carpeta `models/`.
2. **Lectura del archivo de configuración** data.yaml, que contiene:
   - Rutas a imágenes de entrenamiento y validación.
   - Clases y formato del dataset (en este caso, keypoints).

3. **Ejecución del proceso de entrenamiento** con los siguientes parámetros:
   - epochs: número total de épocas (por defecto 100).
   - imgsz: resolución de entrada (640).
   - batch: tamaño del batch.
   - device: GPU utilizada.
   - save_period: frecuencia con la que se guarda un checkpoint del modelo.

4. **Generación de los pesos entrenados** dentro de `./runs/train/yolo11n-pose/.`

Este archivo utiliza la API de Ultralytics, por lo que se requiere tener instalada la versión oficial del paquete ultralytics.

## 📊 Resultados Actuales
El sistema actual permite analizar biomecánicamente el pedaleo de un ciclista utilizando visión artificial con un modelo de pose basado en YOLOv11. Como se encuentra en una fase de prototipado los resultados no son de alta calidad. A continuación se detallan las funcionalidades implementadas:

✅ Entrenamiento basico del modelo YOLOv11 Pose con un dataset de keypoints.

✅ Detección de keypoints anatómicos en ciclistas (hombros, cadera, rodillas, tobillos, etc.) a partir de imágenes o vídeos previamente grabados.

✅ Visualización sobrepuesta de los puntos clave, conexiones esqueléticas y elementos geométricos auxiliares como líneas o elipses.

✅ Cálculo automático de ángulos articulares (por ejemplo, ángulo rodilla-cadera-tobillo) con visualización directa sobre la imagen.

✅ Representación gráfica del ángulo en pantalla y exportación en formato visual del frame con anotaciones biomecánicas.


En resumen, se ha establecido un sistema base sólido y funcional, sobre el cual se construirá un conjunto de herramientas de análisis avanzado en las siguientes etapas del proyecto.

![Resultados](./ImagesReadme/ResultadoProto.jpg)

## Interfaz Grafica

### 1. Ventana Principal

La ventana principal actúa como el núcleo de la aplicación, proporcionando un acceso centralizado a todas las funciones del sistema de análisis biomecánico.
Desde aquí, el usuario puede navegar a las diferentes secciones, configurar el entorno de análisis, iniciar sesiones de captura y generar informes PDF.
![Imagen de la Ventana Principal](.images_readme/principal_window.png)

#### 1. Diseño de interfaz

- Basada en PyQt5 con una disposición QVBoxLayout y QGridLayout para estructurar los componentes.

- Barra de herramientas y menús superiores para acceso rápido a funciones críticas. Divididos en cuatro menús diferentes:
  1. **Archivo**: Opciones para guardar y exportar datos mediante PDF y botón para salir.
  2. **Visualización**: Cambia entre los diferentes modos de visualización de datos entre Vista 2D y 3D. Para el cambio de vista es necesario configurar dos cámaras, para ambos laterales.
  3. **Configuración**: Ajustes de cámaras. Cuenta con la lista de camaras disponibles y la ejecucion del menu de configuracion de camaras.
  4. **Ayuda**: Acceso al repositorio de GitHub del proyecto y contacto.

- La **vista principal** se muestra en la izquierda las vistas configurables y en la derecha se muestra una tabla los angulos. Se muestra el angulo local, el valor maximo del angulo y el valor minimo del angulo.

#### Vistas
- **Vista 2D**: Representación sobre las imagen capturada por la imagen, la informacion de los angulos

![Imagen de la Vista 2D](.images_readme/vista_2d_window.png)

- **Vista 3D**: Representación tridimensional de la posición actual. (Se encuentra en desarrollo debido a errores de visualización)
![Imagen de la Vista 3D](.images_readme/vista_3d_window.png)

### 2. Página de Análisis

La página de análisis es el entorno principal para visualizar y procesar los datos biomecánicos.

- **Visualización gráfica en tiempo real** mediante *PyQtGraph*.
- **Secciones divididas**:  
  - Gráficas comparativa de los angulos de cada articulacion respecto el rango de angulos optimo.
  - Trayectoria de los puntos clave de la rodilla y el tobillo.
- Controles para **reiniciar** los datos actuales.
  
![Imagen de la Página de Análisis](.images_readme/analisis_window.png)

### 3. Página de Exportación (Generación de PDF)

En esta sección el usuario puede **generar un informe en formato PDF** con los resultados del análisis.

- Botón principal para **exportar resultados**.
- Generación de documento PDF con:
  - Tabla de angulos maximos y minimos
  - Gráficas comparativa de los angulos de cada articulacion respecto el rango de angulos optimo.
  - Grafica de las trayectoria de los puntos clave del tobillo y de la rodilla

- Flujo optimizado para que el usuario no necesite guardar las gráficas manualmente; estas se extraen directamente.

![Imagen de la Página de Exportación](.images_readme/export_window.png)

### 4. Página de Configuración de cámaras

Permite ajustar la posicion de las camaras respecto al sujeto:

![Imagen de la Página de Configuración de Cámaras](.images_readme/config_cam_window.png)


## 📩 Contacto

Para dudas, propuestas de colaboración o comentarios técnicos:

📧 [danielcastrogomezzz@gmail.com](mailto:danielcastrogomezzz@gmail.com)
GitHub: [Castro-3034-tbr](https://github.com/Castro-3034-tbr)
