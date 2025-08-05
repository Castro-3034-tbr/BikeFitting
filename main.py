# import matplotlib.pyplot as plt
import angles
import cv2 as cv
from ultralytics import YOLO

import math
import numpy as np

def CalculeAngles(p1,p2,p3):
    """
    Calculate the angle between three points.
    INPUT:
    p1, p2, p3: Tuples representing the coordinates of the points (x, y).
    OUTPUT:
    angles: A dictionary containing the calculated angles and vectors.
    The dictionary contains:
        - 'angle': The angle between the vectors p1->p2 and p2->p3 in degrees.
        - 'angle_v1': The angle of vector p1->p2 with respect to the x-axis in degrees.
        - 'angle_v2': The angle of vector p2->p3 with respect to the x-axis in degrees.
        - 'vector1': The vector from p1 to p2 as a tuple (dx, dy).
        - 'vector2': The vector from p2 to p3 as a tuple (dx, dy).
    """
    
    #Calculate the vectors
    v1 = (p2[0] - p1[0], p2[1] - p1[1])
    v2 = (p3[0] - p2[0], p3[1] - p2[1])
    
    #Calculamos el angulo del vector con el eje x
    angle_v1 = math.atan2(v1[1], v1[0])% 360
    angle_v2 = math.atan2(v2[1], v2[0])% 360

    #Calculamos el angulo entre los dos vectores
    try: 
        angle = math.acos((v1[0] * v2[0] + v1[1] * v2[1]) / 
                        (math.sqrt(v1[0]**2 + v1[1]**2) * math.sqrt(v2[0]**2 + v2[1]**2)))
        
        angle = math.degrees(angle)
        angle = round(angle, 2)
    except ValueError:
        angle = None
    except ZeroDivisionError:
        angle = None

    #Devolvemos toda la informacion
    angulos = {
        'angle': angle,
        'angle_v1': angle_v1,
        'angle_v2': angle_v2,
        'vector1': v1,
        'vector2': v2, 
        'p1': p1,
        'p2': p2,
        'p3': p3
    }

    return angulos

def Draw(img, p1,c,p2, radius=50, color=(0, 255, 0), thickness=2, opuesto=False):
    """
    Draws a line between three points and an arc representing the angle between them.
    INPUT:
    img: The image on which to draw.
    p1, c, p2: Tuples representing the coordinates of the points (x, y).
    radius: The radius of the arc.
    color: The color of the arc and text.
    thickness: The thickness of the arc and text.
    OUTPUT:
    img: The image with the drawn elements.
    """
    
    #Dibujamos los puntos
    cv.circle(img, p1, radius=5, color=(255, 255, 255), thickness=-1)  # Rojo
    cv.circle(img, c, radius=5, color=(255, 255, 255), thickness=-1)  # Verde
    cv.circle(img, p2, radius=5, color=(255, 255, 255), thickness=-1)  # Azul

    #Dibujamos las líneas entre los puntos
    cv.line(img, p1, c, (255, 255, 255), 2)  
    cv.line(img, c, p2, (255, 255, 255), 2)  
    
    #Calculamos los vectores
    vector1 = np.array(p1) - np.array(c)
    vector2 = np.array(p2) - np.array(c)

    #Calculamos los angulos entre el vector y el eje x
    angle_v1 = np.degrees(np.arctan2(vector1[1], vector1[0])) % 360
    angle_v2 = np.degrees(np.arctan2(vector2[1], vector2[0])) % 360
    
    #Calculamos el angulo entre los dos vectores
    try:
        angle = np.degrees(np.arccos(np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))))
        angle = round(angle, 2)
    except ValueError:
        angle = None 
    except ZeroDivisionError:
        angle = None

    if radius != 50:
        #Calculamos el angulo central
        angulo_central = (angle_v1 + angle_v2) / 2
        
        #Calculamos la posición del texto debido que hay varios angulos concentricos
        x_text = int(c[0] + np.cos(np.radians(angulo_central)) * radius)
        y_text = int(c[1] + np.sin(np.radians(angulo_central)) * radius)
        if radius == 25:
            color = (0, 255, 0)  # Cambiamos el color del texto a verde
        elif radius == 75:
            color = (0, 0, 255)  # Cambiamos el color del texto a azul
        else:
            color = (255, 255, 255)  # Cambiamos el color del texto a blanco

    else:
        #Calculamos la posición del texto
        x_text = c[0] + 10
        y_text = c[1] 
        color = (255, 255, 255)  # Cambiamos el color del texto a blanco
    

    # Parámetros de la elipse
    center = c                  # Centro de la elipse
    start_angle = angle_v1       # Ángulo inicial del arco
    end_angle = angle_v2         # Ángulo final del arco

    # Dibujar la elipse
    cv.ellipse(img, center, (radius, radius), 0, start_angle, end_angle, color, thickness)
    cv.putText(img, f" {angle} deg", (x_text, y_text), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    return img, angle

def DrawAngles(img, angulos):
    """
    Draws angles in the image to visualize all the angles calculated.
    """
    
    #Creamos un cuadrado blanco en la esquina superior izquierda
    imgsize = img.shape
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

def AnalizarFrame(img):
    """
    Analyze the frame to detect poses and draw angles.
    INPUT:
    img: The image to analyze.
    OUTPUT:
    img: The image with drawn angles.
    """

    global model
    
    # Detect the pose
    results = model(img)
    if not results or not results[0].keypoints:
        raise Exception("No keypoints detected in the image.")
    print("Pose detection completed successfully.")
    
    #Obtenemos los puntos de la pose
    keypoints = results[0].keypoints[0].xyn
    keypoints_list = keypoints[0].tolist()
    
    #Convert normalized keypoints to pixel coordinates
    size = img.shape
    keypoints_list = [(int(kp[0] * size[1]), int(kp[1] * size[0])) for kp in keypoints_list]
    
    #Organimaos los puntos
    ankles = (keypoints_list[0], keypoints_list[8])
    knees = (keypoints_list[1], keypoints_list[7])
    hip = keypoints_list[2]
    shoulders = keypoints_list[3]
    elbow = keypoints_list[4]
    wrist = keypoints_list[5]
    head = keypoints_list[6]

    # Draw angles on the image
    img , angle1 = Draw(img, ankles[0], knees[0], hip)
    img , angle2 = Draw(img, ankles[1], knees[1], hip)
    img , angle3 = Draw(img, knees[0], hip, shoulders, radius=25)
    img , angle4 = Draw(img, knees[1], hip, shoulders, radius=75)
    img , angle5 = Draw(img, hip, shoulders, elbow, radius=75)
    img , angle6 = Draw(img, shoulders, elbow, wrist)
    img , angle7 = Draw(img, head, shoulders, hip, radius=25)   
    
    #Guardamos los angulos en un diccionario
    angulos = {"rodilla1": angle1, "rodilla2": angle2, "pierna1": angle3, "pierna2": angle4,"brazo": angle5, "codo": angle6, "cabeza": angle7}

    return img, angulos 

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

        #Dibujamos los angulos
        frame = DrawAngles(frame, angulos)

        #Guardamos el frame en el video
        out.write(frame)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv.destroyAllWindows()








