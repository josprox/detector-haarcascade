# -*- coding: utf-8 -*-
"""
Detector de Ojos en una Imagen Estática.

Este script carga una imagen, detecta los ojos utilizando un clasificador
Haar Cascade de OpenCV y dibuja un rectángulo alrededor de cada ojo encontrado.
Finalmente, muestra el resultado y lo guarda en un nuevo archivo.
"""

import cv2
import sys
import os

# --- Configuración ---
# Centralizar las variables facilita las modificaciones.
IMAGE_PATH = 'rostros.jpg'
OUTPUT_IMAGE_PATH = 'resultado_ojos.jpg'
CASCADE_CLASSIFIER = cv2.data.haarcascades + 'haarcascade_eye.xml'

# Parámetros visuales y de detección
RECTANGLE_COLOR = (255, 100, 100)  # Color BGR (Azul, Verde, Rojo)
RECTANGLE_THICKNESS = 2
SCALE_FACTOR = 1.3  # Parámetro para `detectMultiScale`
MIN_NEIGHBORS = 5   # Parámetro para `detectMultiScale`


def main():
    """Función principal que ejecuta todo el proceso."""
    
    # 1. Validar que los archivos necesarios existen
    if not os.path.exists(IMAGE_PATH):
        print(f"Error: No se encontró la imagen en la ruta: '{IMAGE_PATH}'")
        sys.exit(1) # Termina el script si no encuentra la imagen

    # 2. Cargar el clasificador de ojos
    eye_cascade = cv2.CascadeClassifier(CASCADE_CLASSIFIER)
    if eye_cascade.empty():
        print(f"Error: No se pudo cargar el archivo clasificador de Haar Cascade.")
        sys.exit(1)

    # 3. Cargar y procesar la imagen
    image = cv2.imread(IMAGE_PATH)
    if image is None:
        print(f"Error: OpenCV no pudo leer la imagen. Verifica que el archivo no esté dañado.")
        sys.exit(1)
    
    # La detección es más efectiva en escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 4. Realizar la detección de ojos
    # Nota: El nombre de la variable 'face_cascade' en tu código original era confuso,
    # ya que estabas cargando el detector de OJOS. Lo he corregido a 'eye_cascade'.
    eyes = eye_cascade.detectMultiScale(
        gray_image,
        scaleFactor=SCALE_FACTOR,
        minNeighbors=MIN_NEIGHBORS
    )

    print(f"¡Detección completada! Se encontraron {len(eyes)} ojo(s).")

    # 5. Dibujar los resultados en la imagen original
    for (x, y, w, h) in eyes:
        cv2.rectangle(image, (x, y), (x + w, y + h), RECTANGLE_COLOR, RECTANGLE_THICKNESS)

    # 6. Mostrar y guardar la imagen resultante
    cv2.imshow('Detección de Ojos', image)
    cv2.imwrite(OUTPUT_IMAGE_PATH, image)
    print(f"El resultado se ha guardado como '{OUTPUT_IMAGE_PATH}'")

    # Esperar a que el usuario presione una tecla para cerrar la ventana
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Punto de entrada estándar para scripts de Python
if __name__ == '__main__':
    main()