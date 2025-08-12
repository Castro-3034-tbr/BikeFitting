import math 
import cv2 as cv 
import numpy as np

def CalculeAngles(p1,p2,p3):
    """
    Calcula el ángulo entre tres puntos.

    Args:
        p1 (tuple): Coordenadas del primer punto (x, y).
        p2 (tuple): Coordenadas del segundo punto (x, y).
        p3 (tuple): Coordenadas del tercer punto (x, y).

    Returns:
        dict: Diccionario con los ángulos y vectores calculados.
            - 'angle': Ángulo entre los vectores p1->p2 y p2->p3 en grados.
            - 'angle_v1': Ángulo del vector p1->p2 respecto al eje x en grados.
            - 'angle_v2': Ángulo del vector p2->p3 respecto al eje x en grados.
            - 'vector1': Vector de p1 a p2 (dx, dy).
            - 'vector2': Vector de p2 a p3 (dx, dy).
            - 'p1', 'p2', 'p3': Puntos originales.

    Raises:
        ValueError: Si ocurre un error en el cálculo del ángulo.
        ZeroDivisionError: Si los vectores tienen longitud cero.

    Example:
        >>> CalculeAngles((0,0), (1,1), (2,2))
        {'angle': 0.0, ...}
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
    Dibuja líneas y un arco entre tres puntos, representando el ángulo formado.

    Args:
        img (np.ndarray): Imagen sobre la que se dibuja.
        p1 (tuple): Coordenadas del primer punto (x, y).
        c (tuple): Coordenadas del punto central (x, y).
        p2 (tuple): Coordenadas del tercer punto (x, y).
        radius (int, optional): Radio del arco. Por defecto 50.
        color (tuple, optional): Color del arco y texto. Por defecto (0, 255, 0).
        thickness (int, optional): Grosor del arco y texto. Por defecto 2.
        opuesto (bool, optional): Si es True, dibuja el ángulo opuesto. Por defecto False.

    Returns:
        tuple: Imagen con los elementos dibujados y el ángulo calculado.
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

    # #Calculamos los angulos entre el vector y el eje x
    # angle_v1 = np.degrees(np.arctan2(vector1[1], vector1[0])) % 360
    # angle_v2 = np.degrees(np.arctan2(vector2[1], vector2[0])) % 360
    
    #Calculamos el angulo entre los dos vectores
    try:
        angle = np.degrees(np.arccos(np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))))
        angle = round(angle, 2)
    except ValueError:
        angle = None 
    except ZeroDivisionError:
        angle = None

    # if radius != 50:
    #     #Calculamos el angulo central
    #     angulo_central = (angle_v1 + angle_v2) / 2
        
    #     #Calculamos la posición del texto debido que hay varios angulos concentricos
    #     x_text = int(c[0] + np.cos(np.radians(angulo_central)) * radius)
    #     y_text = int(c[1] + np.sin(np.radians(angulo_central)) * radius)
    #     if radius == 25:
    #         color = (0, 255, 0)  # Cambiamos el color del texto a verde
    #     elif radius == 75:
    #         color = (0, 0, 255)  # Cambiamos el color del texto a azul
    #     else:
    #         color = (255, 255, 255)  # Cambiamos el color del texto a blanco

    # else:
    #     #Calculamos la posición del texto
    #     x_text = c[0] + 10
    #     y_text = c[1] 
    #     color = (255, 255, 255)  # Cambiamos el color del texto a blanco
    

    # # Parámetros de la elipse
    # center = c                  # Centro de la elipse
    # start_angle = angle_v1       # Ángulo inicial del arco
    # end_angle = angle_v2         # Ángulo final del arco

    # # Dibujar la elipse
    # cv.ellipse(img, center, (radius, radius), 0, start_angle, end_angle, color, thickness)
    # cv.putText(img, f" {angle} deg", (x_text, y_text), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    return img, angle


def AnalizarFrame(img, model):
    """
    Analiza el frame para detectar poses y dibujar ángulos.

    Args:
        img (np.ndarray): Imagen a analizar.
        model: Modelo de detección de poses.

    Returns:
        tuple: Imagen con los ángulos dibujados y diccionario de ángulos calculados.

    Raises:
        Exception: Si no se detectan keypoints en la imagen.

    """
    
    # Detect the pose
    results = model(img, verbose=False)
    if not results or not results[0].keypoints:
        raise Exception("No keypoints detected in the image.")
    
    #Dibujamos los puntos clave
    for i, keypoint in enumerate(results[0].keypoints[0].xyn[0]):
        x = int(keypoint[0] * img.shape[1])
        y = int(keypoint[1] * img.shape[0])
        cv.circle(img, (x, y), 5, (0, 255, 0), -1)
        cv.putText(img, f"{i}", (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # #Obtenemos los puntos de la pose
    # keypoints = results[0].keypoints[0].xyn
    # keypoints_list = keypoints[0].tolist()
    
    # #Convert normalized keypoints to pixel coordinates
    # size = img.shape
    # keypoints_list = [(int(kp[0] * size[1]), int(kp[1] * size[0])) for kp in keypoints_list]
    
    # #Organimaos los puntos
    # ankles = (keypoints_list[0], keypoints_list[8])
    # knees = (keypoints_list[1], keypoints_list[7])
    # hip = keypoints_list[2]
    # shoulders = keypoints_list[3]
    # elbow = keypoints_list[4]
    # wrist = keypoints_list[5]
    # head = keypoints_list[6]

    # # Draw angles on the image
    # img , angle1 = Draw(img, ankles[0], knees[0], hip)
    # img , angle2 = Draw(img, ankles[1], knees[1], hip)
    # img , angle3 = Draw(img, knees[0], hip, shoulders, radius=25)
    # img , angle4 = Draw(img, knees[1], hip, shoulders, radius=75)
    # img , angle5 = Draw(img, hip, shoulders, elbow, radius=75)
    # img , angle6 = Draw(img, shoulders, elbow, wrist)
    # img , angle7 = Draw(img, head, shoulders, hip, radius=25)   

    #Obtennemos los angulos aleatorios para probar
    angle_pelvis = np.random.randint(0, 180)
    angle_cuello = np.random.randint(0, 180)
    angle_cadera = np.random.randint(0, 180)
    angle_hombro = np.random.randint(0, 180)
    angle_codo = np.random.randint(0, 180)
    angle_muneca = np.random.randint(0, 180)
    angle_rodilla = np.random.randint(0, 180)
    angle_tobillo = np.random.randint(0, 180)

    #Guardamos los angulos en un diccionario
    angulos = {
        "Pelvis": angle_pelvis,
        "Cuello": angle_cuello,
        "Cadera": angle_cadera,
        "Rodilla": angle_rodilla,
        "Tobillo": angle_tobillo,
        "Hombro": angle_hombro,
        "Codo": angle_codo,
        "Muneca": angle_muneca
    }
    
    return img, angulos