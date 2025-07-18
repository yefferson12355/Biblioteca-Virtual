# app.py (Versión Final y Corregida)

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'una_puno_fis_secreto'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Lógica de la Base de Datos ---
def get_db_connection():
    conn = sqlite3.connect('biblioteca.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- Rutas de la Aplicación ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/python')
def python_page():
    conn = get_db_connection()
    # Usamos los nombres de columna correctos en la consulta
    libros = conn.execute("SELECT titulo, autor, descripcion, ruta_archivo FROM libros WHERE categoria = 'Python' ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('python.html', libros=libros, categoria='Python')

@app.route('/java')
def java_page():
    conn = get_db_connection()
    libros = conn.execute("SELECT titulo, autor, descripcion, ruta_archivo FROM libros WHERE categoria = 'Java' ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('java.html', libros=libros, categoria='Java')

@app.route('/cpp')
def cpp_page():
    conn = get_db_connection()
    libros = conn.execute("SELECT titulo, autor, descripcion, ruta_archivo FROM libros WHERE categoria = 'C++' ORDER BY id DESC").fetchall()
    conn.close()
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
        
        conn = get_db_connection()
        conn.execute('INSERT INTO libros (titulo, autor, descripcion, categoria, ruta_archivo) VALUES (?, ?, ?, ?, ?)',
                     (titulo, autor, descripcion, categoria, filename))
        conn.commit()
        conn.close()
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