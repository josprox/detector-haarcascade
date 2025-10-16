# Detector de Objetos con Haar Cascades

Una aplicación de escritorio construida con Python y PySide6 que permite detectar objetos (como rostros, ojos, sonrisas) en imágenes estáticas y en video en tiempo real utilizando clasificadores Haar Cascade de OpenCV.

<center>
<img src="./img/logo.png">
</center>

## 📜 Descripción

Esta herramienta ofrece una interfaz gráfica de usuario (GUI) intuitiva para experimentar con diferentes modelos de detección Haar Cascade. Los usuarios pueden seleccionar dinámicamente tanto el modelo clasificador como la fuente (una imagen de un directorio local o la cámara web en vivo) para realizar el análisis. Los resultados se pueden guardar con un nombre de archivo descriptivo generado automáticamente.

El proyecto está estructurado siguiendo el patrón de diseño **Modelo-Vista-Controlador (MVC)**, lo que separa la lógica de la aplicación (backend) de la interfaz de usuario (frontend), haciéndolo más mantenible, escalable y organizado.

-----

## ✨ Características

  * **Interfaz Gráfica Intuitiva**: Fácil de usar gracias a su diseño basado en PySide6.
  * **Selección Dinámica de Clasificadores**: Carga automáticamente todos los modelos Haar Cascade (`.xml`) que se encuentren en la carpeta `haarcascade`.
  * **Doble Modo de Análisis**:
    1.  **Modo Imagen**: Analiza archivos de imagen (`.jpg`, `.png`) de un directorio local.
    2.  **Modo Cámara en Vivo**: Activa la cámara web para detección en tiempo real.
  * **Actualización en Vivo**: Permite cambiar el clasificador al vuelo mientras la cámara está activa.
  * **Guardado de Resultados**: Guarda las imágenes procesadas en la carpeta `Resultados` con un nombre descriptivo que incluye la fecha y el clasificador utilizado.
  * **Código Modular (MVC)**: Código limpio y separado para facilitar futuras mejoras.

-----

## 🏗️ Estructura del Proyecto

El código está organizado bajo el patrón **Modelo-Vista-Controlador**:

  * **`main.py`**: El punto de entrada de la aplicación. Se encarga de crear e inicializar las instancias del Modelo, la Vista y el Controlador.
  * **`model.py` (Modelo)**: Contiene toda la lógica de backend. Gestiona la interacción con OpenCV, la carga de clasificadores, el procesamiento de imágenes, y el manejo de la cámara. No tiene conocimiento de la interfaz gráfica.
  * **`view.py` (Vista)**: Define la estructura y apariencia de la interfaz gráfica (frontend). Es responsable de mostrar los widgets y emitir señales cuando el usuario interactúa, pero no contiene lógica de procesamiento.
  * **`controller.py` (Controlador)**: Actúa como el intermediario entre el Modelo y la Vista. Escucha las acciones del usuario desde la Vista, las traduce en comandos para el Modelo y actualiza la Vista con los datos resultantes.

-----

## 🛠️ Instalación y Puesta en Marcha

Sigue estos pasos para poner en funcionamiento el proyecto en tu máquina local.

### 1\. Prerrequisitos

Asegúrate de tener instalado lo siguiente:

  * [Python 3.8](https://www.python.org/downloads/) o superior
  * `pip` (el gestor de paquetes de Python)
  * [Git](https://git-scm.com/downloads)

### 2\. Configuración del Proyecto

**A. Clona o descarga este repositorio**

```bash
git clone <URL-del-repositorio>
cd <nombre-del-repositorio>
```

**B. Crea un entorno virtual (recomendado)**
Esto aísla las dependencias de tu proyecto.

```bash
python -m venv venv
```

Actívalo:

  * En Windows (cmd): `venv\Scripts\activate`
  * En macOS/Linux: `source venv/bin/activate`

**C. Instala las librerías necesarias**
Crea un archivo llamado `requirements.txt` en la raíz de tu proyecto y pega el siguiente contenido:

```txt
# requirements.txt
PySide6
opencv-python
numpy
```

Luego, instala todo con un solo comando:

```bash
pip install -r requirements.txt
```

**D. Descarga los Clasificadores Haar Cascade**
Los archivos `.xml` son necesarios para la detección. Puedes descargarlos todos directamente desde el repositorio de OpenCV usando Git:

```bash
# Crea una carpeta para los clasificadores si no existe
mkdir haarcascade

# Entra en la carpeta
cd haarcascade

# Descarga únicamente la carpeta de clasificadores de OpenCV
git init
git remote add -f origin https://github.com/opencv/opencv.git
git config core.sparsecheckout true
echo "data/haarcascades" >> .git/info/sparse-checkout
git pull origin master

# Mueve los archivos .xml a la raíz de la carpeta 'haarcascade' para simplificar
mv data/haarcascades/*.xml .
rm -rf data .git # Limpia los archivos innecesarios de Git
cd .. # Regresa a la raíz del proyecto
```

### 3\. Prepara las Carpetas

Asegúrate de que tu proyecto tenga la siguiente estructura de carpetas en su raíz:

```
/REC_FAC
|-- /haarcascade/           <-- Aquí van los archivos .xml
|-- /imgPruebas/            <-- Coloca aquí tus imágenes de prueba
|-- /Resultados/            <-- Se creará automáticamente para guardar las imágenes
|-- main.py
|-- model.py
|-- view.py
|-- controller.py
|-- requirements.txt
```

-----

## 🚀 Uso

Una vez que hayas completado la instalación, ejecuta la aplicación desde la terminal:

```bash
python main.py
```

Se abrirá la ventana de la aplicación, ¡y ya está lista para usarse\!