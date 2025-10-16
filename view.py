# view.py
import cv2
import numpy as np
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QMessageBox, QFrame
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, Signal

class DetectorView(QMainWindow):
    """
    Vista: Define y controla todos los widgets de la interfaz.
    No contiene lógica de aplicación, solo emite señales de interacción.
    """
    # Señales que el Controlador escuchará
    analyze_button_clicked = Signal()
    camera_button_clicked = Signal()
    save_button_clicked = Signal()
    classifier_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Detector con Haar Cascades (MVC)")
        self.setGeometry(100, 100, 900, 600)
        self.setFixedSize(900, 600)
        self._setup_ui()

    def _setup_ui(self):
        """Construye la interfaz de usuario a partir de widgets."""
        # --- Controles (Izquierda) ---
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(10)

        controls_layout.addWidget(QLabel("<b>1. Seleccionar Clasificador:</b>"))
        self.cascade_combo = QComboBox()
        controls_layout.addWidget(self.cascade_combo)
        
        line1 = QFrame(); line1.setFrameShape(QFrame.HLine)
        controls_layout.addWidget(line1)

        controls_layout.addWidget(QLabel("<b>Modo: Análisis de Imagen</b>"))
        self.image_combo = QComboBox()
        controls_layout.addWidget(self.image_combo)
        self.analyze_button = QPushButton("Analizar Imagen")
        controls_layout.addWidget(self.analyze_button)
        self.save_button = QPushButton("Guardar Resultado")
        self.save_button.setEnabled(False)
        controls_layout.addWidget(self.save_button)
        
        line2 = QFrame(); line2.setFrameShape(QFrame.HLine)
        controls_layout.addWidget(line2)

        controls_layout.addWidget(QLabel("<b>Seleccionar Cámara:</b>"))
        self.camera_combo = QComboBox() # El nuevo menú
        controls_layout.addWidget(self.camera_combo)
        # -----------------------------------------------------------

        self.camera_button = QPushButton("Iniciar Cámara")

        controls_layout.addWidget(QLabel("<b>Modo: Detección en Vivo</b>"))
        self.camera_button = QPushButton("Iniciar Cámara")
        self.camera_button.setStyleSheet("background-color: #007BFF; color: white; padding: 10px;")
        controls_layout.addWidget(self.camera_button)
        controls_layout.addStretch()
        
        controls_widget = QWidget()
        controls_widget.setLayout(controls_layout)
        controls_widget.setFixedWidth(250)

        # --- Visor de Imagen (Derecha) ---
        self.image_label = QLabel("Seleccione un modo de operación")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")

        # --- Layout Principal ---
        main_layout = QHBoxLayout()
        main_layout.addWidget(controls_widget)
        main_layout.addWidget(self.image_label)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Conectar señales internas de widgets a las señales de la clase
        self.analyze_button.clicked.connect(self.analyze_button_clicked.emit)
        self.camera_button.clicked.connect(self.camera_button_clicked.emit)
        self.save_button.clicked.connect(self.save_button_clicked.emit)
        self.cascade_combo.currentTextChanged.connect(self.classifier_changed.emit)

    # --- Métodos que el Controlador puede llamar para actualizar la UI ---
    def populate_combos(self, cascades, images, cameras): # Añadir 'cameras'
        self.cascade_combo.addItems(cascades)
        self.image_combo.addItems(images)
        
        # Poblar el nuevo menú de cámaras
        if not cameras:
            self.camera_combo.addItem("No se encontraron cámaras")
            self.camera_combo.setEnabled(False)
            self.camera_button.setEnabled(False)
        else:
            for index in cameras:
                # Guardamos el índice numérico como dato asociado al texto
                self.camera_combo.addItem(f"Cámara {index}", index)

    def display_image(self, cv_image: np.ndarray):
        height, width, channel = cv_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB).data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def set_camera_button_state(self, is_active: bool):
        if is_active:
            self.camera_button.setText("Detener Cámara")
            self.camera_button.setStyleSheet("background-color: #DC3545; color: white; padding: 10px;")
        else:
            self.camera_button.setText("Iniciar Cámara")
            self.camera_button.setStyleSheet("background-color: #007BFF; color: white; padding: 10px;")
            self.image_label.setText("Cámara detenida. Seleccione un modo.")

    def set_image_mode_enabled(self, enabled: bool):
        self.image_combo.setEnabled(enabled)
        self.analyze_button.setEnabled(enabled)
        # El botón de guardar se maneja por separado

    def set_save_button_enabled(self, enabled: bool):
        self.save_button.setEnabled(enabled)

    def show_message(self, title, text, level="info"):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        if level == "info": msg_box.setIcon(QMessageBox.Information)
        elif level == "warning": msg_box.setIcon(QMessageBox.Warning)
        elif level == "critical": msg_box.setIcon(QMessageBox.Critical)
        msg_box.exec()