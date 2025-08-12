from ultralytics import YOLO

#importamos el modelo YOLO
model = YOLO('./models/yolo11n-pose.pt')
if not model:
    raise Exception("Failed to load the YOLO model.")
print("YOLO model loaded successfully.")

#Realizamos el entrenamiento
model.train(
    data='/home/castro/Musica/Biomecanica/data/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    device='0',
    name='yolo11n-pose',
    project='./runs/train',
    exist_ok=True,
    save=True,
    save_period=10,
)

