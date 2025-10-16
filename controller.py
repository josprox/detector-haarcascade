# controller.py
import os
from datetime import datetime

import cv2

# --- Constantes ---
OUTPUT_DIR = 'Resultados'

class DetectorController:
    """
    Controlador: Conecta la Vista (UI) con el Modelo (lógica).
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._processed_image = None
        self._connect_signals()
        
        # Poblar la UI con datos iniciales del modelo
        self.view.populate_combos(
            self.model.get_available_cascades(),
            self.model.get_available_images(),
            cameras=self.model.get_available_cameras()
        )

    def _connect_signals(self):
        """Conecta las señales de la Vista y el Modelo a los slots del Controlador."""
        # Señales de la Vista -> Slots del Controlador
        self.view.analyze_button_clicked.connect(self.analyze_image)
        self.view.camera_button_clicked.connect(self.toggle_camera)
        self.view.save_button_clicked.connect(self.save_result)
        self.view.classifier_changed.connect(self.classifier_changed)
        
        # Señales del Modelo -> Slots del Controlador
        self.model.frame_updated.connect(self.on_frame_updated)
        self.model.detection_completed.connect(self.on_detection_completed)

    # --- Slots para señales de la Vista ---
    def analyze_image(self):
        """Maneja el clic del botón 'Analizar Imagen'."""
        self.view.set_save_button_enabled(False) # Deshabilitar mientras procesa
        cascade_name = self.view.cascade_combo.currentText()
        if not self.model.load_classifier(cascade_name):
            self.view.show_message("Error", f"No se pudo cargar el clasificador: {cascade_name}", "critical")
            return
            
        image_name = self.view.image_combo.currentText()
        self.model.process_static_image(image_name)

    def toggle_camera(self):
        """Inicia o detiene la cámara."""
        if not self.model.is_camera_active:
            cascade_name = self.view.cascade_combo.currentText()
            # Obtiene el índice de la cámara seleccionada del menú
            camera_index = self.view.camera_combo.currentData()
            
            if camera_index is None:
                self.view.show_message("Error", "No hay cámaras disponibles.", "critical")
                return

            if self.model.load_classifier(cascade_name):
                # Pasa el índice de la cámara al modelo
                if self.model.start_camera(camera_index):
                    self.view.set_camera_button_state(True)
                    self.view.set_image_mode_enabled(False)
                else:
                    self.view.show_message("Error", f"No se pudo acceder a la Cámara {camera_index}.", "critical")
            else:
                self.view.show_message("Error", "Seleccione un clasificador válido primero.", "warning")
        else:
            self.model.stop_camera()
            self.view.set_camera_button_state(False)
            self.view.set_image_mode_enabled(True)

    def classifier_changed(self, cascade_name):
        """Recarga el clasificador si la cámara está activa."""
        if self.model.is_camera_active:
            print(f"Cambiando clasificador en vivo a: {cascade_name}")
            if not self.model.load_classifier(cascade_name):
                self.view.show_message("Error", f"No se pudo cargar: {cascade_name}", "critical")
                self.toggle_camera() # Detener cámara si el clasificador es inválido

    def save_result(self):
        """Guarda la última imagen procesada."""
        if self._processed_image is None: return

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        date_str = datetime.now().strftime('%d%m%y')
        base_img, _ = os.path.splitext(self.view.image_combo.currentText())
        base_cas, _ = os.path.splitext(self.view.cascade_combo.currentText())
        
        filename = f"{base_img}-{date_str}-{base_cas}.jpg"
        path = os.path.join(OUTPUT_DIR, filename)
        
        # OpenCV guarda en BGR, y nuestra imagen está en ese formato.
        cv2.imwrite(path, self._processed_image)
        self.view.show_message("Éxito", f"Imagen guardada en:\n{path}")


    # --- Slots para señales del Modelo ---
    def on_frame_updated(self, frame):
        """Actualiza la imagen en la vista cuando el modelo emite un nuevo frame."""
        self._processed_image = frame
        self.view.display_image(frame)

    def on_detection_completed(self, num_detections):
        """Se activa después del análisis de una imagen estática."""
        print(f"Análisis completado. Detecciones: {num_detections}")
        self.view.set_save_button_enabled(True)