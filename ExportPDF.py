from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import numpy as np
import matplotlib.pyplot as plt
import pyqtgraph as pg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime

class AnalisisWindow():
    """Ventana de analisis de datos biomecanicos."""
    def __init__(self, ):

        # Rango optimo de movimiento
        self.optimal_ranges = [
        ("Pelvis", [[0, 360], [0, 360]]),
        ("Cuello", [[0, 360], [0, 360]]),
        ("Cadera R", [[0, 360], [0, 360]]),
        ("Rodilla R", [[0, 360], [0, 360]]),
        ("Tobillo R", [[0, 360], [0, 360]]),
        ("Cadera L", [[0, 360], [0, 360]]),
        ("Rodilla L", [[0, 360], [0, 360]]),
        ("Tobillo L", [[0, 360], [0, 360]]),
        ("Hombro R", [[0, 360], [0, 360]]),
        ("Codo R", [[0, 360], [0, 360]]),
        ("Muneca R", [[0, 360], [0, 360]]),
        ("Hombro L", [[0, 360], [0, 360]]),
        ("Codo L", [[0, 360], [0, 360]]),
        ("Muneca L", [[0, 360], [0, 360]])
        ]

        #Dividimos el rango en dos
        mitad1 = self.optimal_ranges[:len(self.optimal_ranges)//2]
        mitad2 = self.optimal_ranges[len(self.optimal_ranges)//2:]

        #Creamos los conjuntos de graficas
        self.fig,axes = plt.subplots(
            nrows=max(len(mitad1), len(mitad2)),
            ncols=4,
            figsize=(12, len(mitad1) * 0.6),
            dpi=120
        )

        #Dibujamos los rangos
        self.line_refs = {}

        for row, data in enumerate(mitad1):
            name, (range1, range2) = data
            self.line_refs[(name, 0)] = self.draw_range_bar(axes[row, 0], f"Min: {name}", range1)
            self.line_refs[(name, 1)] = self.draw_range_bar(axes[row, 1], f"Max: {name}", range2)

        for row, data in enumerate(mitad2):
            name, (range1, range2) = data
            self.line_refs[(name, 0, 'R')] = self.draw_range_bar(axes[row, 2], f"Min: {name}", range1)
            self.line_refs[(name, 1, 'R')] = self.draw_range_bar(axes[row, 3], f"Max: {name}", range2)

        plt.tight_layout()

    #Anadimos la grafica al layout
        self.canvas = FigureCanvas(self.fig)

        # ===== Parte inferior: dos casillas =====
        self.height = 200
        # Creamos una grafica
        self.grafica_L = pg.PlotWidget(title="Trayectoria Derecha")
        self.grafica_L.setFixedHeight(self.height)
        self.grafica_L.setAspectLocked(True)


        self.grafica_R = pg.PlotWidget(title="Trayectoria Izquierda")
        self.grafica_R.setFixedHeight(self.height)
        self.grafica_R.setAspectLocked(True)

        #Seteamos los limites TODO: Cambiar los rangos por los necesarios
        self.grafica_L.setLimits(xMin=0, xMax=100, yMin=0, yMax=100)
        self.grafica_R.setLimits(xMin=0, xMax=100, yMin=0, yMax=100)

    def update_trayectorias(self):
        """
        Actualiza las trayectorias de los graficos.

        El metodo actualiza las graficas de trayectoria derecha e izquierda usando los valores almacenados en la ventana principal.

        Returns:
            None
        """

        #Obtenemos los valores
        valores_L = self.main_window.valores_grafica_L
        valores_R = self.main_window.valores_grafica_R

        #Actualizmos la trayectoria derecha
        self.grafica_R.clear()
        self.grafica_R.plot(valores_R[0][0], valores_R[0][1], pen="r", name="Rodilla")
        self.grafica_R.plot(valores_R[1][0], valores_R[1][1], pen="g", name="Tobillo")
        self.grafica_R.addLegend()

        #Actualizamos la trayectoria izquierda
        self.grafica_L.clear()
        self.grafica_L.plot(valores_L[0][0], valores_L[0][1], pen="r", name="Rodilla")
        self.grafica_L.plot(valores_L[1][0], valores_L[1][1], pen="g", name="Tobillo")
        self.grafica_L.addLegend()


    def draw_range_bar(self, ax, name, range_values):
        """
        Dibuja una barra de rango en el grafico.

        El angulo se representa como una barra de color en el eje dado.

        Args:
            ax (matplotlib.axes.Axes): Eje en el que dibujar la barra.
            name (str): Nombre de la barra.
            range_values (list): Valores de rango (inicio, fin).

        Returns:
            matplotlib.lines.Line2D: Linea vertical que representa el rango en el grafico.
        """
        start, end = range_values
        mid = (start + end) / 2
        values = np.linspace(start, end, 300)
        colors = []
        for val in values:
            dist = abs(val - mid) / ((end - start) / 2)
            green = max(0, 1 - dist)
            red = 1 - green
            colors.append((red, green, 0))
        ax.imshow([colors], extent=[start, end, 0, 1], aspect='auto')
        ax.set_yticks([])
        ax.set_xticks([start, mid, end])
        ax.set_xticklabels([f"{start}°", f"{mid:.1f}°", f"{end}°"], fontsize=7)
        ax.set_xlim(start, end)
        ax.set_title(name, fontsize=8)
        return ax.axvline(start - 1, color='black', linewidth=2)

    def update_bars(self):
        """
        Actualiza todos los valores de las barras de rango.

        Returns:
            None
        """
        # Evitar dibujar si la ventana no esta visible
        if not self.isVisible():
            return

        # Actualizamos los valores de las barras de rango
        for key,line in self.line_refs.items():

            #Lado Izquierdo
            if len(key) == 2:
                name, col = key
                start, end = self.optimal_ranges[[n for n, _ in self.optimal_ranges].index(name)][1][col]

            #Lado Derecho
            else:
                name, col, _ = key
                start, end = self.optimal_ranges[[n for n, _ in self.optimal_ranges].index(name)][1][col]

            #Obtenemos el nuevo valor de angulo
            if col == 0:  # Minimo
                new_value = self.main_window.angles_joints[name][0] #TODO: Cambiar por 1 cuando este implementado
            else:  # Maximo
                new_value = self.main_window.angles_joints[name][0] #TODO: Cambiar por 2 cuando este implementado

            line.set_xdata([new_value])
        self.fig.canvas.draw_idle()

def crear_pdf(nombre, angulos):
    """
    Genera el PDF con los resultados biomecanicos y las graficas.

    Args:
        nombre (str): Nombre del usuario.
        angulos (dict): Diccionario con los angulos de las articulaciones.

    Returns:
        None

    Raises:
        FileNotFoundError: Si alguna imagen necesaria no se encuentra.

    Example:
        >>> crear_pdf('usuario', {'Rodilla': [30, 120]})
    """
    #Definimos el canvas para el PDF
    nombre_archivo = f"./pdf/informe_{nombre}.pdf"
    c = rl_canvas.Canvas(nombre_archivo, pagesize=A4)
    ancho, alto = A4
    margen = 25

    # --- Encabezado ---

    alto_encabezado = alto - margen

    # Imagen de la derecha
    ancho_img = 100
    alto_img = 50
    x = ancho - margen - ancho_img   
    y = alto - margen - alto_img      
    ruta_imagen = "./images/logo.png"  # Ruta de la imagen
    c.drawImage(ruta_imagen, x, y, width=ancho_img, height=alto_img, preserveAspectRatio=True)

    # Texto a la izquierda
    c.setFont("Helvetica-Bold", 20)
    texto_encabezado = f"Informe biomecanico de {nombre}"
    ancho_texto = c.stringWidth(texto_encabezado, "Helvetica-Bold", 20)
    x = margen + ancho_texto
    y = alto - margen - alto_img / 2 - 5
    c.drawRightString(x, y, texto_encabezado)
    
    # Linea divisoria gris
    y_linea = alto_encabezado - alto_img - 5
    c.setStrokeColor(colors.grey)
    c.setLineWidth(1)
    c.line(margen, y_linea, ancho - margen, y_linea)

    # --- Tabla de angulos ---
    
    #Transformamos los datos
    datos=[["Articulacion", "Angulo Minimo (º)","Angulo Maximo (º)"]]
    for articulacion, _ in angulos.items():
        datos.append([articulacion, round(angulos[0], 2), round(angulos[1], 2)])

    #Creamos la tabla
    tamano_columnas = [(ancho - 2 * margen) / len(datos[0])]*len(datos[0])
    tabla = Table(datos, colWidths=tamano_columnas)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    #Situamos la posicion de la tabla
    ancho_tabla, alto_tabla = tabla.wrap(ancho - 2 * margen, alto - 2 * margen)
    x_tabla = margen
    y_tabla = y_linea - 10 - alto_tabla
    tabla.drawOn(c, x_tabla, y_tabla)

    #---Graficas de rangos optimos ---
    #Insertamos la imagen
    ancho_img = ancho - 2 * margen
    alto_img = 200
    
    #Calculamos la posicion del grafico
    x_optimos = margen
    y_optimos = y_tabla - 10 - alto_img

    ruta_optimos = "./images/rangos_optimos.png"
    c.drawImage(ruta_optimos, x_optimos, y_optimos, width=ancho_img, height=alto_img, preserveAspectRatio=True)

    #--- Graficas de trayectorias ---
    
    #Ruta de las imagenes
    grafica_L_path = "./images/grafica_L.png"
    grafica_R_path = "./images/grafica_R.png"

    #Dividimos las graficas
    ancho_trayectoria = A4[0] / 2 - 2 * margen
    alto_trayectorias = 200
    
    x_L = margen
    x_R = ancho / 2 + margen
    y = y_optimos - alto_trayectorias - 10

    #Dividimos las graficas
    c.drawImage(grafica_L_path, x_L, y, width=ancho_trayectoria, height=alto_trayectorias, preserveAspectRatio=True)
    c.drawImage(grafica_R_path, x_R, y, width=ancho_trayectoria, height=alto_trayectorias, preserveAspectRatio=True)

    c.setFont("Helvetica", 10)
    c.drawString(margen, 10, "Informe generado por Castro_3034_tbr (" + str(datetime.now().date()) + ":" + str(datetime.now().time())+")")

    c.save()
