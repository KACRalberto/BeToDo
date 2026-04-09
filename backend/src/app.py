from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from src.extensions import conexion, jwt
from src.routes.CRUD import AUTH
import os
from datetime import timedelta

load_dotenv()

app = Flask(__name__)

# ========== CONFIGURACIÓN DE CORS ==========
CORS(
    app, 
    origins=["https://be-to-do.vercel.app"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Content-Type"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    supports_credentials=True
)

# ========== CONFIGURACIÓN DE LA BD ==========
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_ADDON_URI"] = os.getenv("MYSQL_ADDON_URI")

# ========== CONFIGURACIÓN DE JWT ==========
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_TOKEN_ACCESS_EXPIRES"] = timedelta(hours=24)

jwt.init_app(app)
conexion.init_app(app)

app.register_blueprint(AUTH)

@app.errorhandler(404)
def handle_404(e):
    return jsonify({"error": "Recurso no encontrado"}), 404

@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'"
    return response

@app.route("/peticion")
def uptime():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

if __name__ == "__main__":
    app.run(debug=True)