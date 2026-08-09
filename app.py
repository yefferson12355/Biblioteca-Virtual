from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os
import tempfile
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine, text

app = Flask(__name__)
app.secret_key = 'una_puno_fis_secreto'

# 1. Obtener URL de Railway desde Vercel
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("CRÍTICO: No se encontró la variable DATABASE_URL en el entorno.")

# Ajustar prefijo para SQLAlchemy + PyMySQL
if DATABASE_URL.startswith('mysql://'):
    DATABASE_URL = DATABASE_URL.replace('mysql://', 'mysql+pymysql://', 1)

# Crear conexión persistente a MySQL
engine = create_engine(
    DATABASE_URL, 
    future=True, 
    pool_pre_ping=True, 
    pool_recycle=280
)

app.config['UPLOAD_FOLDER'] = os.path.join(tempfile.gettempdir(), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Consultas a la Base de Datos ---

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

# --- Rutas ---

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

if __name__ == '__main__':
    app.run(debug=True)