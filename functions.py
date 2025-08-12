import cv2 as cv
import numpy as np
import math

def CalculeAngles(p1,p2,p3):
    """
    Calcula el angulo entre tres puntos.

    Args:
        p1 (tuple): Coordenadas del primer punto (x, y).
        p2 (tuple): Coordenadas del segundo punto (x, y).
        p3 (tuple): Coordenadas del tercer punto (x, y).

    Returns:
        dict: Diccionario con los angulos y vectores calculados.
            - 'angle': angulo entre los vectores p1->p2 y p2->p3 en grados.
            - 'angle_v1': angulo del vector p1->p2 respecto al eje x en grados.
            - 'angle_v2': angulo del vector p2->p3 respecto al eje x en grados.
            - 'vector1': Vector de p1 a p2 (dx, dy).
            - 'vector2': Vector de p2 a p3 (dx, dy).
            - 'p1', 'p2', 'p3': Puntos originales.

    Raises:
        ValueError: Si ocurre un error en el calculo del angulo.
        ZeroDivisionError: Si los vectores tienen longitud cero.
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

def Draw(img, p1, c, p2, radius=50, color=(255, 255, 255), thickness=2, opuesto=False):
    """
    Dibuja lineas y un arco entre tres puntos, representando el angulo formado.

    Args:
        img (np.ndarray): Imagen sobre la que se dibuja.
        p1 (tuple): Coordenadas del primer punto (x, y).
        c (tuple): Coordenadas del punto central (x, y).
        p2 (tuple): Coordenadas del tercer punto (x, y).
        radius (int, optional): Radio del arco. Por defecto 50.
        color (tuple, optional): Color del arco. Por defecto (0, 255, 0).
        thickness (int, optional): Grosor del arco. Por defecto 2.
        opuesto (bool, optional): Si es True, dibuja el angulo opuesto. Por defecto False.

    Returns:
        tuple: Imagen con los elementos dibujados y el angulo calculado.
    """

    #Dibujamos las lineas entre los puntos
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

    # Parametros de la elipse
    center = c  # Centro de la elipse
    
    # Normalizar los ángulos para asegurar que estén en el rango [0, 360)
    angle_v1_norm = angle_v1 % 360
    angle_v2_norm = angle_v2 % 360

    # Calcular la diferencia angular más corta
    diff = abs(angle_v2_norm - angle_v1_norm)

    if opuesto:
        # Si queremos el ángulo opuesto, invertimos la lógica
        if diff > 180:
            # Dibujar el arco corto
            start_angle = min(angle_v1_norm, angle_v2_norm)
            end_angle = max(angle_v1_norm, angle_v2_norm)
        else:
            # Dibujar el arco largo (complementario)
            if angle_v1_norm > angle_v2_norm:
                start_angle = angle_v2_norm
                end_angle = angle_v1_norm + 360
            else:
                start_angle = angle_v1_norm
                end_angle = angle_v2_norm + 360
    else:
        # Lógica normal: dibujar el arco más corto
        if diff > 180:
            # Si la diferencia es mayor a 180°, el arco corto va en la otra dirección
            if angle_v1_norm > angle_v2_norm:
                start_angle = angle_v1_norm
                end_angle = angle_v2_norm + 360
            else:
                start_angle = angle_v2_norm
                end_angle = angle_v1_norm + 360
        else:
            # Arco normal: del ángulo menor al mayor
            start_angle = min(angle_v1_norm, angle_v2_norm)
            end_angle = max(angle_v1_norm, angle_v2_norm)

    # Dibujar la elipse
    cv.ellipse(img, center, (radius, radius), 0, start_angle, end_angle, color, thickness)

    return img, angle


def AnalizarFrame(img, model):
    """
    Analiza el frame para detectar poses y dibujar angulos.

    Args:
        img (np.ndarray): Imagen a analizar.
        model: Modelo de deteccion de poses.

    Returns:
        tuple: Imagen con los angulos dibujados y diccionario de angulos calculados.

    Raises:
        Exception: Si no se detectan keypoints en la imagen.

    """

    # Detect the pose
    results = model(img, verbose=False)
    if not results or not results[0].keypoints:
        raise Exception("No keypoints detected in the image.")

    #Obtenemos la lista de puntos
    keypoints = results[0].keypoints[0].xyn
    keypoints_list = keypoints[0].tolist()

    #Obtenemos los puntos para cada articulacion TODO: Poner las id correctas de cada punto
    keypoint_dic = {
        "puntapie": keypoints_list[0],
        "tobillo": keypoints_list[1],
        "rodilla": keypoints_list[2],
        "cadera": keypoints_list[3],
        "hombro": keypoints_list[4],
        "codo": keypoints_list[5],
        "muneca": keypoints_list[6],
        "dedo": keypoints_list[6],
        "cabeza": keypoints_list[7]
    }

    #TODO: Borrar puntos menos el de caderaX
    keypoint_dic["puntapie"] = (
        (keypoint_dic["tobillo"][0] + 0.05),
        (keypoint_dic["tobillo"][1])
    )

    #Anadimos el CaderaX
    keypoint_dic["caderaX"] = (
        (keypoint_dic["cadera"][0] + 0.05),
        (keypoint_dic["cadera"][1])
    )

    keypoint_dic["dedo"] = (
        (keypoint_dic["dedo"][0]+ 0.05),
        (keypoint_dic["dedo"][1])
    )

    #Dibujamos los puntos clave
    for _, keypoint in enumerate(keypoint_dic.items()):
        name = keypoint[0]
        x = int(keypoint[1][0] * img.shape[1])
        y = int(keypoint[1][1] * img.shape[0])
        keypoint_dic[name] = (x, y)

        cv.circle(img, (x, y), 5, (0, 255, 0), -1)

    #Calculamos los angulos y dibujamos las lineas y angulos
    img , angulo_cuello = Draw(img, keypoint_dic["cabeza"] ,keypoint_dic["hombro"], keypoint_dic["cadera"], opuesto=True, color=(0, 255, 0))
    img , angulo_cadera = Draw(img, keypoint_dic["caderaX"] ,keypoint_dic["cadera"], keypoint_dic["hombro"], color=(255, 0, 0))
    img , angulo_hombro = Draw(img,keypoint_dic["cadera"] ,keypoint_dic["hombro"], keypoint_dic["codo"],color=(0, 0, 255))
    img , angulo_codo = Draw(img, keypoint_dic["hombro"] ,keypoint_dic["codo"], keypoint_dic["muneca"], color=(255, 255, 0))
    img , angulo_muneca = Draw(img, keypoint_dic["codo"] ,keypoint_dic["muneca"], keypoint_dic["dedo"], color=(255, 0, 255))
    img , angulo_rodilla = Draw(img, keypoint_dic["cadera"] ,keypoint_dic["rodilla"], keypoint_dic["tobillo"], color=(0, 255, 255))
    img, angulo_tobillo = Draw(img, keypoint_dic["puntapie"] ,keypoint_dic["tobillo"], keypoint_dic["rodilla"], color=(128, 128, 128))

    #Guardamos los angulos en un diccionario
    angulos = {
        "Pelvis": angulo_cadera,
        "Cuello": angulo_cuello,
        "Cadera": angulo_cadera,
        "Rodilla": angulo_rodilla,
        "Tobillo": angulo_tobillo,
        "Hombro": angulo_hombro,
        "Codo": angulo_codo,
        "Muneca": angulo_muneca
    }

    return img, angulos