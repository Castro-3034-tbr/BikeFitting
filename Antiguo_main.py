# import matplotlib.pyplot as plt
import cv2 as cv
from ultralytics import YOLO

from functions import AnalizarFrame

def DrawAngles(img, angulos):
    """
    Dibuja los angulos calculados en la imagen para visualizacion.

    Args:
        img (np.ndarray): Imagen sobre la que se dibujan los angulos.
        angulos (dict): Diccionario con los angulos calculados.

    Returns:
        np.ndarray: Imagen con los angulos dibujados.
    """
    
    #Creamos un cuadrado blanco en la esquina superior izquierda
    cv.rectangle(img, (10, 10), (200, 220), (255, 255, 255), -1)

    #Dibujamos los angulos
    cv.putText(img, f"Rodilla 1: {angulos['rodilla1']:.2f} deg", (20, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv.putText(img, f"Rodilla 2: {angulos['rodilla2']:.2f} deg", (20, 50), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv.putText(img, f"Pierna 1: {angulos['pierna1']:.2f} deg", (20, 70), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv.putText(img, f"Pierna 2: {angulos['pierna2']:.2f} deg", (20, 90), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv.putText(img, f"Brazo: {angulos['brazo']:.2f} deg", (20, 110), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv.putText(img, f"Codo: {angulos['codo']:.2f} deg", (20, 130), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv.putText(img, f"Cabeza: {angulos['cabeza']:.2f} deg", (20, 150), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    return img

# Load the YOLO model
model = YOLO('./models/best_Pose.pt')
if not model:
    raise Exception("Failed to load the YOLO model.")
print("YOLO model loaded successfully.")

#Definimos el archivo de entrada
# input_file = './test/img2.jpg'
input_file = './test/test1.mkv'

#comprobamos si es una imagen o un video
if input_file.endswith('.jpg') or input_file.endswith('.png'):
    #Es una imagen
    img = cv.imread(input_file)
    if img is None:
        raise Exception("Failed to load image file.")
    print("Image file loaded successfully.")
    
    #Analizamos la imagen
    img, angulos = AnalizarFrame(img)
    #Dibujamos los angulos
    img = DrawAngles(img, angulos)
    
    #Guardamos la imagen con los puntos
    output_path = './test/output_pose.jpg'
    cv.imwrite(output_path, img)
    print(f"Output image saved to {output_path}.")

else:
    #Es un video
    cap = cv.VideoCapture(input_file)
    if not cap.isOpened():
        raise Exception("Failed to open video file.")
    print("Video file opened successfully.")

    #Creamos un video writer to save the output
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    output_path = './test/output_pose_video.avi'
    out = cv.VideoWriter(output_path, fourcc, 30.0, (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))
    
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        #Analizamos el frame
        frame, angulos = AnalizarFrame(frame)

        #Guardamos el frame en el video
        out.write(frame)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv.destroyAllWindows()








