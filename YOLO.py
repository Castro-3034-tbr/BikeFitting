from argparse import ArgumentParser
from pathlib import Path
from ultralytics import YOLO
from ultralytics.utils.files import increment_path
import os
import logging
import time
import sys
import yaml


def find_cache_files(dir):
    """Funcion para encontrar y eliminar archivos de cache
    Input:
        dir: directorio donde buscar
    Output:
        cache_paths: lista de rutas de los archivos de cache
    """
    cache_paths = []

    # Recorremos el directorio y buscamos archivos de cache
    for dirpath, _, filenames in os.walk(dir):
        for file in filenames:

            if file.endswith(".cache"):
                full_path = os.path.join(dirpath, file)
                logger.info(f"A cache file has been found: {full_path}")
                try:
                    os.remove(full_path)
                    cache_paths.append(full_path)
                    logger.info("Cache removed successfully")
                except Exception as e:
                    logger.error(f"Failed to remove {full_path}: {e}")
    return cache_paths


# Leemos los argumentos
parser = ArgumentParser()
parser.add_argument(
    "--task",
    choices=["train", "val", "test", "detect"],
    nargs="+",
    default=["train"],
    help="Tarea a realizar",
)
parser.add_argument("--model", type=str, default="yolo11n.pt", help="Nombre del modelo")
parser.add_argument(
    "--augment", action="store_true", help="Usar augmentacion de ultralytics"
)
parser.add_argument("--weights", action="store_false", help="Usar pesos preentrenados")
parser.add_argument(
    "--data",
    type=str,
    default="./data/data_config.yaml",
    help="Ruta del config",
)
parser.add_argument("--epochs", type=int, default=100, help="Numero de epochs")
parser.add_argument("--batch", type=int, default=16, help="Batch size")
parser.add_argument("--imgsz", type=int, default=640, help="Tamaño de la imagen")
parser.add_argument("--device", type=str, default="cuda", help="Dispositivo a utilizar")

parser.add_argument("--save_period", type=int, default=10, help="Periodo de guardado")
parser.add_argument("--save", action="store_false", help="Guardar resultados")
parser.add_argument("--seed", type=int, default=1, help="Semilla")
parser.add_argument("--patience", type=int, default=10, help="Paciencia")
parser.add_argument("--workers", type=int, default=18, help="Numero de workers")
parser.add_argument("--mosaic", action="store_true", help="Usar mosaico")
parser.add_argument(
    "--conf", type=float, default=0.5, help="Confianza mínima para la detección"
)
parser.add_argument(
    "--output", type=str, default="output", help="Ruta del archivo de salida"
)

# Controlamos los argumentos
try:
    args = parser.parse_args()
except Exception as e:
    print(f"Error al parsar los argumentos: {e}")
    exit(1)

print("Argumentos ingresados:")
for arg in vars(args):
    print(f"  {arg}: {getattr(args, arg)}")

# Comprobamos la ruta de los datos
data_path = Path(args.data)


if not data_path.is_absolute():
    # Si no incluye carpeta 'DatasetTrain', la añadimos
    if data_path.parent.name != "DatasetTrain":
        data_path = Path("DatasetTrain") / data_path.name
    # Convertimos a absoluta respecto al directorio del script
    data_path = (Path(__file__).parent.resolve() / data_path).resolve()
else:
    # Es absoluta, solo resolvemos para normalizar
    data_path = data_path.resolve()

# Comprobamos si del modelo es correcto
if not args.model.endswith(".pt"):
    args.model += ".pt"

# Convertimos a Path
model_path = Path(args.model)

# Comprobamos si la ruta es absoluta
if not model_path.is_absolute():
    # Si no incluye carpeta 'models', la añadimos
    if model_path.parent.name != "models":
        model_path = Path("models") / model_path.name
    # Convertimos a absoluta respecto al directorio del script
    model_path = (Path(__file__).parent.resolve() / model_path).resolve()
else:
    # Es absoluta, solo resolvemos para normalizar
    model_path = model_path.resolve()

# Obtenemos el nombre del modelo
model_name = model_path.stem


# Obtenemos la ruta del proyecto
project_path = os.path.dirname(os.path.abspath(__file__))

output_path = os.path.join(project_path, "runs")
print("Ruta de salida: ", output_path)

time_now = time.localtime()
current_time = time.strftime("%m-%d_%H-%M-%S", time_now)

NameFile = "RUN_{}_{}".format(model_name, current_time)

output_path = os.path.join(output_path, NameFile)

if not os.path.exists(output_path):
    os.makedirs(output_path)
    print("Carpeta de salida creada: ", output_path)
else:
    print("La carpeta de salida ya existe: ", output_path)

# Creamos el logger
log_file = os.path.join(output_path, "log_RUN.log")
print(log_file)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, mode="w"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger()
print("Logger creado: ", log_file)


# Guardamos en el log los argumentos
logger.info(
    "Argumentos ingresados:\n\t task: {}\n\t model: {}\n\t augment: {}\n\t weights: {}\n\t data: {}\n\t epochs: {}\n\t batch: {}\n\t imgsz: {}\n\t device: {}\n\t save_period: {}\n\t save: {}\n\t seed: {}\n\t patience: {}\n\t workers: {}\n\t mosaic: {}\n\t conf: {}".format(
        args.task,
        args.model,
        args.augment,
        args.weights,
        args.data,
        args.epochs,
        args.batch,
        args.imgsz,
        args.device,
        args.save_period,
        args.save,
        args.seed,
        args.patience,
        args.workers,
        args.mosaic,
        args.conf,
    )
)


# Cargamos el modelo
try:
    if args.weights:
        logging.info(f"Modelo cargado: {model_path}, con pesos preentrenados")
    else:
        modeloName = args.model.replace(".pt", ".yaml")
        logging.info(f"Modelo cargado: {model_path}, sin pesos preentrenados")
    model = YOLO(model_path)
    model.info()

except Exception as e:
    logging.error(f"Error al cargar el modelo: {e}")
    exit(1)


# Buscamos y eliminamos archivos de cache
if args.task == "train":
    cache_paths = Path(args.data).resolve()
    print("Cache paths: ", cache_paths)

    cache_paths = find_cache_files(args.data)
    if len(cache_paths) > 0:
        logger.info(f"Cache files found and removed: {cache_paths}")
    else:
        logger.info("No cache files found")

for task in args.task:
    print("Tarea: ", task)
    # Comprobamos si la tarea es valida
    if task == "train":
        # Entrenamos el modelo
        logger.info("Comenzando el entrenamiento")

        try:
            if args.augment:
                print("Usando augmentación de ultralytics")
                model.train(
                    data=args.data,                         # Configuracion de los datos
                    epochs=args.epochs,                     # Numero de epochs
                    batch=args.batch,                       # Batch size
                    imgsz=args.imgsz,                       # Tamaño de la imagen
                    device=args.device,                     # Dispositivo a utilizar
                    save_period=args.save_period,           # Periodo de guardado
                    seed=args.seed,                         # Semilla
                    patience=args.patience,                 # Paciencia
                    workers=args.workers,                   # Numero de workers
                    mosaic=args.mosaic,                     # Usar mosaico
                    name=output_path+"/train",              # Ruta de guardado
                )
            else:
                print("No se usara augmentación de ultralytics")
                model.train(
                    data=args.data,                         # Configuracion de los datos
                    epochs=args.epochs,                     # Numero de epochs
                    batch=args.batch,                       # Batch size
                    imgsz=args.imgsz,                       # Tamaño de la imagen
                    device=args.device,                     # Dispositivo a utilizar
                    save_period=args.save_period,           # Periodo de guardado
                    seed=args.seed,                         # Semilla
                    patience=args.patience,                 # Paciencia
                    workers=args.workers,                   # Numero de workers
                    hsv_h=0,                                # HSV-Hue augmentation
                    hsv_s=0,                                # HSV-Saturation augmentation
                    hsv_v=0,                                # HSV-Value augmentation
                    degrees=0,                              # Image rotation
                    translate=0,                            # Image translation
                    scale=0,                                # Image scaling
                    shear=0,                                # Image shearing
                    perspective=0,                          # Perspective transformation
                    flipud=0,                               # Vertical flip
                    fliplr=0,                               # Horizontal flip
                    mosaic=0,                               # Mosaic augmentation
                    mixup=0,                                # Mixup augmentation
                    name=output_path+"/train",              # Ruta de guardado
                )

        except Exception as e:
            logger.error(f"Error en el entrenamiento: {e}")
            exit(1)
        logger.info("Entrenamiento finalizado")

        # Seleccionamos el mejor modelo
        model = YOLO(model.trainer.best)

    elif task == "val":
        # Validamos el modelo
        logger.info("Validando el modelo")

        model.val(
            data=args.data,                                 # Configuracion de los datos
            batch=args.batch,                               # Batch size
            imgsz=args.imgsz,                               # Tamaño de la imagen
            device=args.device,                             # Dispositivo a utilizar
            workers=args.workers,                           # Numero de workers
            name=output_path+"/validation",                 # Nombre de la carpeta de salida
        )

    elif task == "test":
        # Testeamos el modelo
        logger.info("Testeando el modelo")

        # Definimos la ruta de salida
        save_dir = increment_path("runs/test", exist_ok=True)

        model.val(
            data=args.data,                                 # Configuracion de los datos
            split="test",                                   # Usamos el split de test
        batch=args.batch,                                   # Batch size
        imgsz=args.imgsz,                                   # Tamaño de la imagen
            device=args.device,                             # Dispositivo a utilizar
            workers=args.workers,                           # Numero de workers
            name=output_path+"/test",                       # Nombre de la carpeta de salida
        )

    elif task == "detect":
        # Comprobamos si data es un .yaml
        if args.data.endswith(".yaml"):
            # Cogemos la ruta de detect de la configuracion
            with open(args.data, "r") as file:
                data = yaml.safe_load(file)
                data_path = data["detect"]

        # Predecimos la salida
        model.predict(
            source=data_path,                               # Ruta de la imagen
            conf=args.conf,                                 # Confianza mínima para la detección
            imgsz=args.imgsz,                               # Tamaño de la imagen
            device=args.device,                             # Dispositivo a utilizar
            save=args.save,                                 # Guardar resultados
            save_txt=args.save,                             # Guardar las etiquetas de las deteccion en txt
            save_conf=args.save,                            # Guardar confianza
            name=output_path+"/detect",                     # Nombre de la carpeta de salida
            exist_ok=True,                                  # Sobreescribir la carpeta de salida si existe
        )
