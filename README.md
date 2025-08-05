# BikeFitting 

> **ENGLISH SUMMARY**

This project aims to analyze the **biomechanics of a cyclist** using **computer vision**, a **webcam**, and a **YOLOv11 Pose model**. It calculates key joint angles from body landmarks detected during pedaling, enabling postural analysis, injury prevention, and performance optimization.  
Designed to evolve into a real-time, multi-camera 3D analysis system with intelligent tracking and feedback.

# 🚴 Análisis Biomecánico de Ciclistas mediante Visión Artificial

Este proyecto busca analizar la **biomecánica del ciclista** durante el pedaleo mediante técnicas de **visión artificial**, usando una **webcam** y un modelo de detección de poses basado en **YOLOv11**. A partir de los puntos clave del cuerpo, se calcula una serie de **ángulos articulares relevantes** para evaluar la postura, prevenir lesiones y optimizar el rendimiento.

## 🎯 Objetivo General

Diseñar e implementar una herramienta capaz de:
- Detectar automáticamente los movimientos clave del ciclista.
- Calcular ángulos biomecánicos relevantes.
- Ofrecer feedback visual y cuantitativo.
- Servir de base para análisis más avanzados en versiones futuras.

## 📌 Características Principales

- 🧠 Detección automática de keypoints anatómicos (hombros, cadera, rodillas, tobillos, etc.).
- 📐 Cálculo de ángulos articulares en tiempo real o por archivo.
- 🎯 Visualización gráfica de los ángulos sobre el vídeo o imagen.
- 💾 Exportación de resultados con anotaciones biomecánicas.
- 🧩 Estructura modular para futuras ampliaciones (multi-cámara, análisis temporal, comparaciones, etc.).


## ⚙️ Requisitos

- Python 3.8 o superior  
- OpenCV ≥ 4.5  
- Ultralytics YOLO ≥ 8.x  
- NumPy  

Instalación rápida:
```bash
pip install -r requirements.txt
````


## ▶️ Ejecución

1. Asegúrate de tener el modelo entrenado en `models/best_Pose.pt`.
2. Ejecuta el análisis:

```bash
python main.py
```

Soporta tanto imágenes como vídeos. El resultado se guarda con anotaciones visuales en el archivo de salida.

---

## 📊 Resultados Actuales

Actualmente, el sistema es capaz de:

- ✅ Detectar automáticamente los puntos clave del cuerpo a partir de vídeo o imagen.
- ✅ Calcular y visualizar ángulos articulares como rodilla-cadera-tobillo o brazo-hombro.
- ✅ Dibujar esqueleto, arcos, líneas de análisis y ángulos sobre la imagen original.
- ✅ Exportar resultados con superposición gráfica.
- ✅ Entrenar modelos propios con YOLOv11 Pose para adaptar a datasets específicos.

> 📌 *En su estado actual, el sistema está en fase funcional de prototipo. La precisión es suficiente para pruebas controladas, con margen de mejora en robustez y exactitud.*

## 🚧 Desarrollos Futuros

Este proyecto está diseñado para crecer hacia una solución más avanzada y profesional. Las próximas etapas previstas incluyen:

- **🎥 Entrada en tiempo real desde cámara**: reemplazo del procesamiento por archivo.
- **🖥️ Sistema multicámara**: para reconstrucción 3D mediante triangulación de keypoints.
- **📐 Calibración del entorno**: herramientas automáticas para corregir distancias y perspectiva.
- **📈 Seguimiento temporal y análisis dinámico**: representación de la evolución de ángulos por ciclo de pedaleo.
- **📤 Exportación de datos en CSV/PDF**: informes automáticos y exportación para análisis posteriores.
- **🔁 Modo comparación**: referencia contra una técnica ideal o patrón de pedaleo eficiente.
- **🎛️ Interfaz gráfica (GUI)**: control del flujo de análisis sin necesidad de código.
* **🤖 Filtro de Kalman para seguimiento continuo**:

  * Estimación de keypoints entre frames.
  * Reducción de ruido.
  * Mejora del rendimiento y robustez ante oclusiones.


## 🤝 Contribuciones

Este proyecto está en crecimiento. Las contribuciones son bienvenidas, ya sea mediante PRs, reportes de bugs o sugerencias de mejora.

## 📩 Contacto

Para dudas, propuestas de colaboración o comentarios técnicos:

📧 [danielcastrogomezzz@gmail.com](mailto:danielcastrogomezzz@gmail.com)
GitHub: [Castro-3034-tbr](https://github.com/Castro-3034-tbr)
