# -*- coding: utf-8 -*-
"""
Detección de Rostros en Tiempo Real con OpenCV.

Este script utiliza la cámara web para capturar video, detecta rostros en
cada fotograma usando un clasificador Haar Cascade y muestra el resultado
con un rectángulo verde alrededor de cada rostro.

Presiona la tecla 'q' para salir.
"""

import cv2
import sys

# --- Constantes de Configuración ---
# Facilita cambiar parámetros sin tener que buscarlos en el código.
CASCADE_FILE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
CAMERA_DEVICE_INDEX = 0
RECTANGLE_COLOR = (0, 255, 125)  # Color BGR para el rectángulo
RECTANGLE_THICKNESS = 2

# Parámetros para el detector `detectMultiScale`
SCALE_FACTOR = 1.1      # Qué tanto se reduce la imagen en cada escala.
MIN_NEIGHBORS = 5       # Cuántos "vecinos" debe tener cada rectángulo candidato para retenerlo.
MIN_FACE_SIZE = (30, 30)  # El tamaño mínimo del objeto a detectar.


def run_face_detector():
    """
    Inicializa la cámara y ejecuta el bucle principal para la detección de rostros.
    """
    # 1. Cargar el clasificador Haar Cascade
    face_cascade = cv2.CascadeClassifier(CASCADE_FILE_PATH)
    if face_cascade.empty():
        print(f"Error crítico: No se pudo cargar el archivo del clasificador en: {CASCADE_FILE_PATH}")
        sys.exit(1)  # Termina el programa si no se puede cargar el archivo esencial.

    # 2. Iniciar la captura de video
    video_capture = cv2.VideoCapture(CAMERA_DEVICE_INDEX)
    if not video_capture.isOpened():
        print(f"Error crítico: No se pudo acceder a la cámara con índice {CAMERA_DEVICE_INDEX}.")
        sys.exit(1)

    print("Iniciando detector de rostros... Presiona 'q' para salir.")

    # 3. Bucle principal de procesamiento
    while True:
        # Capturar un fotograma de la cámara
        ret, frame = video_capture.read()
        if not ret:
            print("Advertencia: No se pudo obtener el fotograma. Saliendo...")
            break

        # Convertir a escala de grises (más eficiente para la detección)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar rostros en el fotograma
        faces = face_cascade.detectMultiScale(
            gray_frame,
            scaleFactor=SCALE_FACTOR,
            minNeighbors=MIN_NEIGHBORS,
            minSize=MIN_FACE_SIZE
        )

        # Dibujar un rectángulo en cada rostro detectado
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), RECTANGLE_COLOR, RECTANGLE_THICKNESS)

        # Mostrar el fotograma resultante
        cv2.imshow('Detector de Rostros', frame)

        # Condición de salida
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 4. Liberar recursos
    print("Cerrando aplicación y liberando recursos.")
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    run_face_detector()