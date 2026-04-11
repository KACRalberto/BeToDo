#!/usr/bin/env python3
"""
Script para inicializar/crear las tablas de la base de datos en producción.
Ejecutar una vez después del despliegue.
"""

import os
from dotenv import load_dotenv
from flask import Flask
from flask_mysqldb import MySQL

load_dotenv()

app = Flask(__name__)

# Configuración de la BD
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

def create_tables():
    with app.app_context():
        try:
            cursor = mysql.connection.cursor()

            # Crear tabla tareas si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tareas (
                    id_tarea INT PRIMARY KEY AUTO_INCREMENT,
                    id_usuario INT NOT NULL,
                    titulo VARCHAR(255) NOT NULL,
                    descripcion TEXT,
                    estado ENUM('pendiente', 'en_marcha', 'completada') DEFAULT 'pendiente',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
                )
            """)

            mysql.connection.commit()
            print("✅ Tabla 'tareas' creada o ya existe")

            # Verificar que la tabla existe
            cursor.execute("SHOW TABLES LIKE 'tareas'")
            if cursor.fetchone():
                print("✅ Verificación: tabla 'tareas' existe")
            else:
                print("❌ Error: tabla 'tareas' no se creó")

        except Exception as e:
            print(f"❌ Error al crear tablas: {e}")
        finally:
            cursor.close()

if __name__ == "__main__":
    create_tables()