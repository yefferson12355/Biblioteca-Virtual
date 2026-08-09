from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os
import tempfile
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine, text

app = Flask(__name__)
app.secret_key = 'una_puno_fis_secreto'

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Si viene con mysql://, le agregamos +pymysql para que SQLAlchemy use el driver correcto
    if DATABASE_URL.startswith('mysql://'):
        DATABASE_URL = DATABASE_URL.replace('mysql://', 'mysql+pymysql://', 1)
    elif DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        
    engine = create_engine(DATABASE_URL, future=True)
    app.config['UPLOAD_FOLDER'] = os.path.join(tempfile.gettempdir(), 'uploads')
else:
    # Modo Local (SQLite)
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
    SQLITE_PATH = os.path.join(app.root_path, 'biblioteca.db')
    engine = create_engine(f"sqlite:///{SQLITE_PATH}", future=True)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Lógica de la Base de Datos ---

def init_db():
    with engine.begin() as conn:
        # Si es MySQL usa AUTO_INCREMENT y VARCHAR, si es SQLite usa AUTOINCREMENT y TEXT
        if engine.dialect.name == 'mysql':
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS libros (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    titulo VARCHAR(255) NOT NULL,
                    autor VARCHAR(255),
                    descripcion TEXT,
                    categoria VARCHAR(100) NOT NULL,
                    ruta_archivo VARCHAR(500) NOT NULL
                )
            '''))
        else:
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS libros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    autor TEXT,
                    descripcion TEXT,
                    categoria TEXT NOT NULL,
                    ruta_archivo TEXT NOT NULL
                )
            '''))

def fetch_libros(categoria):
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT titulo, autor, descripcion, ruta_archivo "
            "FROM libros WHERE categoria = :categoria ORDER BY id DESC"
        ), {"categoria": categoria})
        return [dict(row) for row in result.mappings().all()]

def insert_libro(titulo, autor, descripcion, categoria, filename):
    with engine.begin() as conn:
        conn.execute(text(
            "INSERT INTO libros (titulo, autor, descripcion, categoria, ruta_archivo) "
            "VALUES (:titulo, :autor, :descripcion, :categoria, :ruta_archivo)"
        ), {
            "titulo": titulo,
            "autor": autor,
            "descripcion": descripcion,
            "categoria": categoria,
            "ruta_archivo": filename
        })

# Inicializar la base de datos al arrancar
init_db()

# --- Rutas de la Aplicación ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/python')
def python_page():
    libros = fetch_libros('Python')
    return render_template('python.html', libros=libros, categoria='Python')

@app.route('/java')
def java_page():
    libros = fetch_libros('Java')
    return render_template('java.html', libros=libros, categoria='Java')

@app.route('/cpp')
def cpp_page():
    libros = fetch_libros('C++')
    return render_template('cpp.html', libros=libros, categoria='C++')

@app.route('/upload', methods=['POST'])
def upload_file():
    categoria = request.form['category']
    titulo = request.form['title']
    autor = request.form['author']
    descripcion = request.form['description']
    archivo = request.files['file']

    if archivo and archivo.filename != '':
        filename = secure_filename(archivo.filename)
        archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        insert_libro(titulo, autor, descripcion, categoria, filename)
        flash(f'¡Libro "{titulo}" subido con éxito!', 'success')
    else:
        flash('Error: No se seleccionó ningún archivo.', 'danger')
        
    return redirect(url_for(f'{categoria.lower()}_page'))

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- Ejecución ---
if __name__ == '__main__':
    app.run(debug=True)