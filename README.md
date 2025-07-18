# 📚 Biblioteca de Programación - FIS UNA PUNO

Este proyecto es una aplicación web simple y funcional desarrollada con **Flask** que sirve como una **biblioteca colaborativa de recursos de programación**.  
Los usuarios pueden navegar por recursos organizados por lenguaje (Python, Java, C++) y contribuir subiendo sus propios archivos.

---

## ➤ Características

- **Visualización por Categorías:** Recursos organizados en secciones dedicadas para *Python, Java y C++*.
- **Subida de Archivos:** Un formulario intuitivo en una ventana modal permite a los usuarios subir nuevos libros o documentos a la categoría correspondiente.
- **Listado Dinámico:** Los recursos subidos aparecen inmediatamente en la tabla sin necesidad de reiniciar el servidor.
- **Descarga de Archivos:** Cada recurso listado tiene un enlace directo para su descarga.
- **Diseño Responsivo:** La interfaz, construida con **Bootstrap 5**, se adapta a cualquier tamaño de pantalla, desde computadoras de escritorio hasta teléfonos móviles.

---

## ➤ Tecnologías Utilizadas

### 🔧 Backend

- **Python 3**
- **Flask:** Framework web para la gestión de rutas y lógica del servidor.
- **Jinja2:** Motor de plantillas para renderizar HTML dinámico.

### 💾 Base de Datos

- **SQLite:** Base de datos relacional ligera para almacenar la metadata de los libros.

### 🎨 Frontend

- **HTML5**
- **CSS3**
- **Bootstrap 5:** Para el diseño y los componentes de la interfaz.
- **Font Awesome:** Para los íconos.

---

## 🚀 Instalación y Ejecución Local

Sigue estos pasos para poner en marcha el proyecto en tu máquina local.

### ✅ Prerrequisitos

Tener **Python 3** instalado en tu sistema. Puedes verificarlo con el siguiente comando:

```bash

= OJO ESTE PROYECTO SOLO FUNCIONA A NIVEL LOCAL ,POR AHORA .
python --version
📥 1. Clonar el Repositorio
bash

git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
🧪 2. Crear un Entorno Virtual
Es una buena práctica crear un entorno virtual para aislar las dependencias del proyecto.

bash

# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS / Linux
python3 -m venv venv
source venv/bin/activate
Verás (venv) al principio de la línea de tu terminal, indicando que el entorno está activo.

📦 3. Instalar las Dependencias
bash

pip install Flask
🛠 4. Inicializar la Base de Datos
Ejecuta el script init_db.py para crear el archivo biblioteca.db y la tabla libros.
Este paso solo es necesario la primera vez.

bash

python init_db.py
Deberías ver mensajes en la terminal confirmando que la base de datos y la tabla se crearon.

▶️ 5. Ejecutar la Aplicación
bash

python app.py
La terminal te mostrará un mensaje como este:

csharp

 * Running on http://127.0.0.1:5000
🌐 ¡Probar el Proyecto!
Abre tu navegador web y ve a la dirección:

cpp

http://127.0.0.1:5000
¡Ya deberías ver la página principal de la biblioteca!

📂 Estructura del Proyecto
bash

/
├── app.py              # Lógica principal de Flask.
├── init_db.py          # Script de inicialización de la BD.
├── biblioteca.db       # Archivo de la base de datos.
│
├── /static/            # Archivos estáticos (CSS, JS, imágenes).
├── /templates/         # Plantillas HTML.
└── /uploads/           # Carpeta donde se guardan los archivos subidos.
🔧 Posibles Mejoras a Futuro
🔐 Sistema de Autenticación: Para controlar quién puede subir archivos.

🔍 Función de Búsqueda: Para encontrar recursos fácilmente.

🗑️ Eliminación de Archivos: Para que un administrador pueda moderar el contenido.

📄 Paginación: Para manejar un gran número de recursos de manera eficiente.

🙌 Créditos  : Yefferson miranda Josec
Este proyecto fue desarrollado como parte del curso de programación de la
Facultad de Ingeniería de Sistemas - Universidad Nacional del Altiplano, Puno.









Preguntar a ChatGPT
