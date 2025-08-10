import matplotlib.pyplot as plt
import numpy as np
import time
import random

# --- Datos ---
optimal_ranges = [
    ("Pelvis", [[25, 35], [145, 155]]),
    ("Cuello", [[25, 35], [145, 155]]),
    ("Cadera R", [[30, 40], [150, 160]]),
    ("Rodilla R", [[30, 40], [150, 160]]),
    ("Tobillo R", [[30, 40], [150, 160]]),
    ("Cadera L", [[30, 40], [150, 160]]),
    ("Rodilla L", [[30, 40], [150, 160]]),
    ("Tobillo L", [[30, 40], [150, 160]]),
    ("Hombro R", [[30, 40], [150, 160]]),
    ("Codo R", [[30, 40], [150, 160]]),
    ("Muñeca R", [[30, 40], [150, 160]]),
    ("Hombro L", [[30, 40], [150, 160]]),
    ("Codo L", [[30, 40], [150, 160]]),
    ("Muñeca L", [[30, 40], [150, 160]])
]

# Dividimos en dos columnas
mid = len(optimal_ranges) // 2
left_ranges = optimal_ranges[:mid]
right_ranges = optimal_ranges[mid:]

# --- Crear figura ---
fig, axes = plt.subplots(
    nrows=max(len(left_ranges), len(right_ranges)),
    ncols=4,
    figsize=(12, len(left_ranges) * 0.6),
    dpi=120
)

line_refs = {}

# --- Función para dibujar cada barra ---
def draw_range_bar(ax, name, angle_range):
    start, end = angle_range
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

# Dibujar rangos
for row, data in enumerate(left_ranges):
    name, (range1, range2) = data
    line_refs[(name, 0)] = draw_range_bar(axes[row, 0], f"Min: {name}", range1)
    line_refs[(name, 1)] = draw_range_bar(axes[row, 1], f"Max: {name}", range2)

for row, data in enumerate(right_ranges):
    name, (range1, range2) = data
    line_refs[(name, 0, 'R')] = draw_range_bar(axes[row, 2], f"Min: {name}", range1)
    line_refs[(name, 1, 'R')] = draw_range_bar(axes[row, 3], f"Max: {name}", range2)

plt.tight_layout()

# --- Función para actualizar ---
def update_all_values():
    for key, line in line_refs.items():
        if len(key) == 2:  # lado izquierdo
            name, col = key
            start, end = optimal_ranges[[n for n, _ in optimal_ranges].index(name)][1][col]
        else:  # lado derecho
            name, col, _ = key
            start, end = optimal_ranges[[n for n, _ in optimal_ranges].index(name)][1][col]
        new_value = random.uniform(start, end)
        line.set_xdata([new_value])
    fig.canvas.draw_idle()

# --- Modo interactivo ---
plt.ion()
# plt.show()

# Bucle de actualización cada 1s
while True:
    update_all_values()
    plt.pause(1)
