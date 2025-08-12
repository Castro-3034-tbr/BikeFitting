#!/bin/bash

# #Ejecutamos el codigo de python y blender
# blender ./RenderMinas.blend -b -P ./CreateDataset.py

# #Dividimos las imagenes en train y validacion
# bash Divisiondata.sh
# echo "Archivos divididos en train y validacion"

#Entrenamiento del modelo m
python3 YOLO.py  --model yolo11l-pose.pt --data ./data/data_config.yaml --patience 200 --epochs 200 --batch 2
