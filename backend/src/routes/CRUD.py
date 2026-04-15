from flask import Blueprint, jsonify, request
from src.extensions import conexion, crear_token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from src import loggers
from uuid import uuid4
from datetime import datetime, timedelta
import re
import bleach
import smtplib
from email.message import EmailMessage
import os

_email_regex = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def sanitize_text(text: str) -> str:
    """Elimina TODO el HTML/JS para prevenir XSS."""
    if text is None: return ""
    return bleach.clean(text, tags=[], attributes={}, strip=True)

def is_valid_email(email: str) -> bool:
    return bool(_email_regex.match(email))

def is_strong_password(password: str) -> bool:
    """Mínimo 8 caracteres, al menos una mayúscula, minúscula, número y símbolo."""
    if len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)
    return has_upper and has_lower and has_digit and has_symbol

# Login throttling: 10 intentos fallidos antes de bloquear 5 minutos
LOGIN_ATTEMPTS = {}
MAX_LOGIN_ATTEMPTS = 10
LOCKOUT_SECONDS = 5 * 60

def enviar_email_recuperacion(email_destino: str, token: str):
    """Envía el email desde el backend en lugar de usar EmailJS en el frontend."""
    # Configura tus credenciales reales en tu archivo .env
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER", "tu_correo@gmail.com")
    smtp_pass = os.getenv("SMTP_PASS", "tu_password_de_aplicacion")

    enlace = f"https://be-to-do.vercel.app/reset-password?token={token}"
    
    msg = EmailMessage()
    msg['Subject'] = 'Recuperación de Contraseña'
    msg['From'] = smtp_user
    msg['To'] = email_destino
    msg.set_content(f"Hola,\n\nPara restablecer tu contraseña, haz clic en el siguiente enlace:\n{enlace}\n\nEste enlace expira en 1 hora.")

    try:
        # Si no tienes configurado el SMTP, se imprimirá en consola (modo desarrollo)
        print(f"--- SIMULACIÓN DE ENVÍO DE EMAIL ---\nEnlace: {enlace}\n------------------------------------")
        

        with smtplib.SMTP(smtp_server, smtp_port) as server:
             server.starttls()
             server.login(smtp_user, smtp_pass)
             server.send_message(msg)
    except Exception as e:
        print(f"Error enviando email: {e}")

AUTH = Blueprint("auth", __name__, url_prefix="/auth")
fileLog = loggers.my_logger("log_file", "WARNING", False, "MyLog.log")

@AUTH.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data: return jsonify({'error':'Datos inválidos'}), 400

    email = sanitize_text(data.get("email", "")).strip().lower()
    userName = sanitize_text(data.get("name", "Anónimo")).strip()
    password = data.get("password", "")
    passwordCheck = data.get("password_check", "") # Evitamos sanitizar contraseñas para no dañar caracteres especiales

    if not is_valid_email(email): return jsonify({'error': 'Email no válido'}), 400
    if len(email) > 254 or len(userName) > 50: return jsonify({'error': 'Campo demasiado largo'}), 400
    if not is_strong_password(password): return jsonify({"error":"La contraseña debe tener al menos 8 caracteres, con mayúsculas, minúsculas, números y símbolos"}), 400
    if passwordCheck != password: return jsonify({"error": "Las contraseñas deben coincidir"}), 400

    try:
        with conexion.connection.cursor() as cursor:
            cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone(): return jsonify({'error': 'El email ya está registrado'}), 409

            passwordHash = generate_password_hash(password)
            cursor.execute("INSERT INTO usuarios (email, password, username) VALUES (%s, %s, %s)", (email, passwordHash, userName))
            conexion.connection.commit()
            
            user_id = cursor.lastrowid
            token = crear_token(str(user_id))

        return jsonify({'message': 'Usuario registrado', 'token': token, 'user': userName}), 201
    except Exception as e:
        fileLog.error(f"Error en register: {str(e)}")
        print("🚨 ERROR REAL EN REGISTER:", e)
        return jsonify({'error': 'Error interno'}), 500

@AUTH.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data: return jsonify({"error": "JSON inválido"}), 400

    email = sanitize_text(data.get("email", "")).strip().lower()
    password = data.get("password", "")

    if not password: return jsonify({"error": "Contraseña requerida"}), 400

    now = datetime.now()
    attempt = LOGIN_ATTEMPTS.get(email, {"count": 0, "locked_until": None})
    locked_until = attempt.get("locked_until")

    if locked_until and now < locked_until:
        wait_seconds = int((locked_until - now).total_seconds())
        return jsonify({"error": f"Demasiados intentos. Espera {wait_seconds} segundos."}), 429

    if locked_until and now >= locked_until:
        attempt = {"count": 0, "locked_until": None}

    try:
        with conexion.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()

            if not user:
                attempt["count"] = attempt.get("count", 0) + 1
                if attempt["count"] >= MAX_LOGIN_ATTEMPTS:
                    attempt["locked_until"] = now + timedelta(seconds=LOCKOUT_SECONDS)
                    attempt["count"] = 0
                LOGIN_ATTEMPTS[email] = attempt
                return jsonify({"error": "Credenciales incorrectas"}), 401

            # Soporte dual: ya sea que la base de datos devuelva Diccionarios o Tuplas (id, email, password, username)
            user_id = user["id"] if isinstance(user, dict) else user[0]
            user_pass = user["password"] if isinstance(user, dict) else user[2]
            user_name = user["username"] if isinstance(user, dict) else user[3]

            if not check_password_hash(user_pass, password):
                attempt["count"] = attempt.get("count", 0) + 1
                if attempt["count"] >= MAX_LOGIN_ATTEMPTS:
                    attempt["locked_until"] = now + timedelta(seconds=LOCKOUT_SECONDS)
                    attempt["count"] = 0
                LOGIN_ATTEMPTS[email] = attempt
                return jsonify({"error": "Credenciales incorrectas"}), 401

            LOGIN_ATTEMPTS.pop(email, None)
            token = crear_token(str(user_id))

        return jsonify({"token": token, "user": user_name}), 200
    except Exception as e:
        fileLog.error(f"Error en login: {str(e)}")
        return jsonify({'error': 'Error interno'}), 500

@AUTH.route("/tareas", methods=["POST"])
@jwt_required()
def postTareas():
    try:
        # 1. Movido dentro del try por seguridad
        userId = int(get_jwt_identity())  
        
        # 2. Agregamos 'or {}' para evitar que 'data' sea None si el frontend no envía el Content-Type adecuado
        data = request.get_json() or {}
        
        # 3. Validación manual por si envían un JSON vacío
        if not data: 
            return jsonify({"error": "No se enviaron datos"}), 400

        titulo = sanitize_text(data.get("titulo", "")).strip()
        descripcion = sanitize_text(data.get("descripcion", "")).strip()
        estado = sanitize_text(data.get("estado", "pendiente")).strip().lower()
        
        if estado not in ("pendiente","en_marcha","completada"): 
            estado = "pendiente"

        if not titulo: 
            return jsonify({"error": "Título requerido"}), 400

        with conexion.connection.cursor() as cursor:
            cursor.execute("INSERT INTO tareas (id_usuario, titulo, descripcion, estado) VALUES (%s, %s, %s, %s)", 
                           (userId, titulo, descripcion, estado))
            conexion.connection.commit()
            
        return jsonify({"status": "ok"}), 201
        
    except Exception as e:
        # Ahora sí atrapará TODOS los errores correctamente
        fileLog.error(f"Error en postTareas: {str(e)}")
        print("Error real en postTareas:", e) # <-- Esto saldrá en tus logs de Render
        return jsonify({"error": "Error interno"}), 500

@AUTH.route("/tareas", methods=["GET"])
@jwt_required()
def getTareas():
    userId = int(get_jwt_identity())  # Convertir a int
    try:
        with conexion.connection.cursor() as cursor:
            cursor.execute("SELECT id_tarea, titulo, descripcion, estado FROM tareas WHERE id_usuario = %s ORDER BY id_tarea DESC LIMIT 50", (userId,))
            tareas_raw = cursor.fetchall()
            tareas = []
            for t in tareas_raw:
                if isinstance(t, dict):
                    if 'id_tarea' in t: t['id'] = t.pop('id_tarea')
                    tareas.append(t)
                else:
                    tareas.append({"id": t[0], "titulo": t[1], "descripcion": t[2], "estado": t[3]})
        return jsonify({"ok": True, "tareas": tareas}), 200
    except Exception as e:
        fileLog.error(f"Error en getTareas: {str(e)}")
        print("Error en getTareas:", e)
        return jsonify({"error": "Error interno"}), 500

@AUTH.route("/tareas/<int:tarea_id>", methods=["PUT"])
@jwt_required()
def updateTarea(tarea_id):
    userId = int(get_jwt_identity())  # Convertir a int
    try:
        data = request.get_json() or {}
        titulo_nuevo = sanitize_text(data["titulo"]) if "titulo" in data else None
        descripcion_nueva = sanitize_text(data["descripcion"]) if "descripcion" in data else None
        estado_nuevo = sanitize_text(data["estado"]).strip().lower() if "estado" in data else None

        with conexion.connection.cursor() as cursor:
            cursor.execute("SELECT id_usuario FROM tareas WHERE id_tarea = %s", (tarea_id,))
            tarea = cursor.fetchone()

            if not tarea: return jsonify({"error": "Tarea no encontrada"}), 404
            
            tarea_id_usuario = tarea["id_usuario"] if isinstance(tarea, dict) else tarea[0]
            if str(tarea_id_usuario) != str(userId): return jsonify({"error": "No autorizado"}), 403

            updates, params = [], []
            if titulo_nuevo is not None: updates.append("titulo = %s"); params.append(titulo_nuevo.strip())
            if descripcion_nueva is not None: updates.append("descripcion = %s"); params.append(descripcion_nueva.strip())
            if estado_nuevo is not None: updates.append("estado = %s"); params.append(estado_nuevo)

            if not updates: return jsonify({"error": "No hay campos para actualizar"}), 400
            params.append(tarea_id)
            cursor.execute(f"UPDATE tareas SET {', '.join(updates)} WHERE id_tarea = %s", tuple(params))
            conexion.connection.commit()

        return jsonify({"status": "ok", "message": "Tarea actualizada"}), 200
    except Exception as e:
        fileLog.error(f"Error en updateTarea: {str(e)}")
        print("Error en updateTarea:", e)
        return jsonify({"error": "Error interno"}), 500

@AUTH.route("/tareas/<int:tarea_id>", methods=["DELETE"])
@jwt_required()
def deleteTarea(tarea_id):
    userId = int(get_jwt_identity())  # Convertir a int
    try:
        with conexion.connection.cursor() as cursor:
            cursor.execute("SELECT id_usuario FROM tareas WHERE id_tarea = %s", (tarea_id,))
            tarea = cursor.fetchone()
            if not tarea: return jsonify({"error": "Tarea no encontrada"}), 404
            
            tarea_id_usuario = tarea["id_usuario"] if isinstance(tarea, dict) else tarea[0]
            if str(tarea_id_usuario) != str(userId): return jsonify({"error": "No autorizado"}), 403

            cursor.execute("DELETE FROM tareas WHERE id_tarea = %s", (tarea_id,))
            conexion.connection.commit()
        return jsonify({"status": "ok", "message": "Tarea eliminada"}), 200
    except Exception as e:
        fileLog.error(f"Error en deleteTarea: {str(e)}")
        print("Error en deleteTarea:", e)
        return jsonify({"error": "Error interno"}), 500

@AUTH.route("/tareas", methods=["DELETE"])
@jwt_required()
def deleteTodasTareas():
    userId = int(get_jwt_identity())  # Convertir a int
    try:
        with conexion.connection.cursor() as cursor:
            cursor.execute("DELETE FROM tareas WHERE id_usuario = %s", (userId,))
            conexion.connection.commit()
        return jsonify({"status": "ok", "message": "Todas las tareas eliminadas"}), 200
    except Exception as e:
        fileLog.error(f"Error en deleteTodasTareas: {str(e)}")
        print("Error en deleteTodasTareas:", e)
        return jsonify({"error": "Error interno"}), 500

@AUTH.route("/request-password-reset", methods=["POST"])
def request_password_reset():
    data = request.get_json()
    email = sanitize_text(data.get("email", "")).strip().lower()
    
    try:
        with conexion.connection.cursor() as cursor:
            cursor.execute("SELECT id, email FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()
            if not user: return jsonify({"message": "Si existe la cuenta, se ha enviado un correo"}), 200

            user_id = user['id'] if isinstance(user, dict) else user[0]
            user_email = user['email'] if isinstance(user, dict) else user[1]

            cursor.execute('''CREATE TABLE IF NOT EXISTS password_resets (
                id INT AUTO_INCREMENT PRIMARY KEY, user_id INT NOT NULL, token VARCHAR(128) NOT NULL,
                expires DATETIME NOT NULL, used TINYINT(1) DEFAULT 0)''')

            reset_token = uuid4().hex
            expires = datetime.utcnow() + timedelta(hours=1)
            cursor.execute("INSERT INTO password_resets (user_id, token, expires) VALUES (%s, %s, %s)", (user_id, reset_token, expires))
            conexion.connection.commit()

            enviar_email_recuperacion(user_email, reset_token)

        # EL TOKEN YA NO SE ENVÍA AL FRONTEND
        return jsonify({"message": "Si existe la cuenta, se ha enviado un correo"}), 200
    except Exception as e:
        return jsonify({"error": "Error interno"}), 500

@AUTH.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    token = sanitize_text(data.get("token"))
    new_password = data.get("password")

    if not is_strong_password(new_password): return jsonify({"error": "La contraseña debe tener al menos 8 caracteres, con mayúsculas, minúsculas, números y símbolos"}), 400

    try:
        with conexion.connection.cursor() as cursor:
            cursor.execute("SELECT id, user_id, expires, used FROM password_resets WHERE token = %s", (token,))
            record = cursor.fetchone()

            if not record:
                return jsonify({"error": "Token inválido o expirado"}), 400

            record_id = record['id'] if isinstance(record, dict) else record[0]
            record_user_id = record['user_id'] if isinstance(record, dict) else record[1]
            record_expires = record['expires'] if isinstance(record, dict) else record[2]
            record_used = record['used'] if isinstance(record, dict) else record[3]

            if record_used or record_expires < datetime.utcnow():
                return jsonify({"error": "Token inválido o expirado"}), 400

            passwordHash = generate_password_hash(new_password)
            cursor.execute("UPDATE usuarios SET password = %s WHERE id = %s", (passwordHash, record_user_id))
            cursor.execute("UPDATE password_resets SET used = 1 WHERE id = %s", (record_id,))
            conexion.connection.commit()

        return jsonify({"message": "Contraseña actualizada"}), 200
    except Exception:
        return jsonify({"error": "Error interno"}), 500

@AUTH.route("/contact", methods=["POST"])
def contact():
    """Endpoint para enviar el formulario de contacto al correo del administrador."""
    data = request.get_json()
    if not data: return jsonify({"error": "Datos inválidos"}), 400

    nombre = sanitize_text(data.get("nombre", "Usuario"))
    email_remitente = sanitize_text(data.get("email", ""))
    mensaje = sanitize_text(data.get("mensaje", ""))

    if not is_valid_email(email_remitente) or not mensaje:
        return jsonify({"error": "Email y mensaje son obligatorios"}), 400

    destino = "titobek21@gmail.com"
    
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_pass = os.getenv("SMTP_PASS", "")

    try:
        msg = EmailMessage()
        msg['Subject'] = f'Nuevo mensaje de contacto de BeToDo de: {nombre}'
        msg['From'] = smtp_user if smtp_user else "betodo@ejemplo.com"
        msg['To'] = destino
        msg.set_content(f"Has recibido un nuevo mensaje desde tu aplicación BeToDo.\n\nNombre: {nombre}\nEmail: {email_remitente}\n\nMensaje:\n{mensaje}")

        # Para que el correo salga de verdad a tu bandeja, debes configurar SMTP_USER y SMTP_PASS en el .env
        if smtp_user and smtp_pass:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            return jsonify({"message": "Email enviado correctamente"}), 200
        else:
            # Evita que falle si estás en desarrollo sin credenciales SMTP puestas
            print(f"SIMULACIÓN DE CORREO A {destino}: \n{mensaje}")
            return jsonify({"message": "Email simulado con éxito (Falta configurar credenciales SMTP en backend)"}), 200

    except Exception as e:
        print(f"Error en endpoint contact: {e}")
        return jsonify({"error": "No se pudo enviar el mensaje"}), 500