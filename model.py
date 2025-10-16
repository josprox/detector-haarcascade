# model.py
import os
import sys 
import cv2
import numpy as np
from PySide6.QtCore import QObject, Signal, QTimer

# --- Resolución dinámica de rutas para PyInstaller (Solución Universal) ---
if getattr(sys, 'frozen', False):
    # Si la aplicación está "congelada" por PyInstaller
    if hasattr(sys, '_MEIPASS'):
        # Modo --onefile: los datos están en una carpeta temporal
        base_path = sys._MEIPASS
    else:
        # Modo de carpeta: los datos están junto al ejecutable
        base_path = os.path.dirname(sys.executable)
else:
    # Si se ejecuta como un script normal .py
    base_path = os.path.dirname(os.path.abspath(__file__))


# --- Constantes con rutas dinámicas ---
HAARCASCADE_DIR = os.path.join(base_path, 'haarcascade')
IMAGES_DIR = os.path.join(base_path, 'imgPruebas')


class DetectionModel(QObject):
    """
    Modelo: Maneja toda la lógica de OpenCV y el estado de la aplicación.
    No conoce la existencia de la interfaz gráfica.
    """
    # Señales para notificar al Controlador sobre los cambios
    frame_updated = Signal(np.ndarray)
    detection_completed = Signal(int) # Emite el número de detecciones

    def __init__(self):
        super().__init__()
        self.classifier = None
        self.video_capture = None
        self.is_camera_active = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_frame)

    def get_available_cameras(self):
        """
        Escanea los índices de las cámaras para encontrar las que están conectadas.
        Devuelve una lista de índices válidos.
        """
        camera_indexes = []
        # Un límite razonable para no escanear infinitamente
        for i in range(10): 
            cap = cv2.VideoCapture(i, cv2.CAP_MSMF)
            if cap.isOpened():
                camera_indexes.append(i)
                cap.release()
        return camera_indexes

    def get_available_cascades(self):
        """Devuelve una lista de archivos .xml en el directorio de cascadas."""
        try:
            return [f for f in os.listdir(HAARCASCADE_DIR) if f.endswith('.xml')]
        except FileNotFoundError:
            # Añadimos un print para depuración
            print(f"Error: No se encontró el directorio de cascadas en: {HAARCASCADE_DIR}")
            return []

    def get_available_images(self):
        """Devuelve una lista de imágenes en el directorio de pruebas."""
        try:
            return [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        except FileNotFoundError:
            # Añadimos un print para depuración
            print(f"Error: No se encontró el directorio de imágenes en: {IMAGES_DIR}")
            return []

    def load_classifier(self, cascade_name):
        """Carga un clasificador Haar Cascade."""
        if not cascade_name: return False
        cascade_path = os.path.join(HAARCASCADE_DIR, cascade_name)
        self.classifier = cv2.CascadeClassifier(cascade_path)
        return not self.classifier.empty()

    def process_static_image(self, image_name):
        """Procesa una imagen estática y emite el resultado."""
        if self.classifier is None or not image_name: return

        image_path = os.path.join(IMAGES_DIR, image_name)
        image = cv2.imread(image_path)
        if image is None: return

        processed_image, detections = self._perform_detection(image)
        self.frame_updated.emit(processed_image)
        self.detection_completed.emit(len(detections))

    def start_camera(self, camera_index): # Ahora recibe el índice como argumento
        """Inicia la captura de video desde la cámara especificada."""
        if self.classifier is None: return False
        
        # Usa el índice que nos pasa el controlador
        self.video_capture = cv2.VideoCapture(camera_index, cv2.CAP_MSMF)
        if not self.video_capture.isOpened():
            self.video_capture = None
            return False

        self.is_camera_active = True
        self.timer.start(30) # ~33 FPS
        return True

    def stop_camera(self):
        """Detiene la captura de video."""
        self.is_camera_active = False
        self.timer.stop()
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
            
    def _update_frame(self):
        """Captura y procesa un fotograma de la cámara."""
        if not self.video_capture: return

        ret, frame = self.video_capture.read()
        if not ret:
            self.stop_camera()
            return
        
        processed_frame, _ = self._perform_detection(frame)
        self.frame_updated.emit(processed_frame)

    def _perform_detection(self, image):
        """Función central de detección para cualquier imagen (estática o de video)."""
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detections = self.classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(30, 30))

        for (x, y, w, h) in detections:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 125), 2)
            
        return image, detections

