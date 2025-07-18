# init_db.py
import sqlite3

# Conecta (o crea si no existe) el archivo de la base de datos
conn = sqlite3.connect('biblioteca.db')

print("Base de datos conectada...")

# DROP TABLE asegura que empecemos con una tabla limpia cada vez que se ejecuta
conn.execute('DROP TABLE IF EXISTS libros;')
print("Tabla 'libros' vieja eliminada (si existía).")

# Crea la tabla 'libros' con la estructura final
conn.execute('''
    CREATE TABLE libros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT,
        descripcion TEXT,
        categoria TEXT NOT NULL,
        ruta_archivo TEXT NOT NULL
    )
''')

print("Tabla 'libros' creada exitosamente en biblioteca.db")

# Guarda los cambios y cierra la conexión
conn.commit()
conn.close()