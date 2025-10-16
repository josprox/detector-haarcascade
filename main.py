# main.py
import sys
from PySide6.QtWidgets import QApplication
from view import DetectorView
from model import DetectionModel
from controller import DetectorController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 1. Crear las instancias
    model = DetectionModel()
    view = DetectorView()
    
    # 2. Conectarlos a través del Controlador
    controller = DetectorController(model=model, view=view)
    
    # 3. Mostrar la vista y ejecutar la aplicación
    view.show()
    sys.exit(app.exec())