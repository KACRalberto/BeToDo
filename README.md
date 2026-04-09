# BeToDo - Gestión de Tareas

Aplicación full-stack para gestión de tareas personales con autenticación JWT.

## 🚀 Despliegue a Producción

### 1. Configuración del Backend

1. Crea el archivo `backend/.env` con tus credenciales reales:
   ```
   MYSQL_USER=tu_usuario
   MYSQL_PASSWORD=tu_contraseña
   MYSQL_HOST=tu_host_mysql
   MYSQL_DB=gestor_tareas
   JWT_SECRET_KEY=clave_segura_muy_larga_aqui
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=tu_email@gmail.com
   SMTP_PASS=tu_app_password
   ```

2. Instala dependencias:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### 2. Configuración del Frontend

1. Construye para producción:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

### 3. Opciones de Despliegue

#### Opción A: Heroku (Recomendado para principiantes)
1. Crea una app en Heroku
2. Conecta tu repositorio Git
3. Asegúrate de que `Procfile`, `runtime.txt` y `requirements.txt` estén en la raíz
4. Despliega automáticamente

#### Opción B: VPS (DigitalOcean, AWS, etc.)
1. Instala Nginx y configura como proxy reverso
2. Usa Gunicorn para el backend: `gunicorn --bind 0.0.0.0:8000 wsgi:app`
3. Sirve el frontend desde `/var/www/html` o similar

#### Opción C: Railway o Render
- Sube el código, configura variables de entorno
- Despliegue automático

### 4. Base de Datos
- Crea la base de datos MySQL en tu proveedor (PlanetScale, AWS RDS, etc.)
- Ejecuta las migraciones si es necesario

### 5. Dominio y SSL
- Configura un dominio
- Habilita HTTPS con Let's Encrypt

## 🔧 Desarrollo Local

```bash
# Backend
cd backend
python -m venv venv
pip install -r requirements.txt
python src/app.py

# Frontend
cd frontend
npm install
npm run dev
```

## 📋 Checklist de Producción

- [ ] Cambiar JWT_SECRET_KEY por una clave segura
- [ ] Configurar base de datos MySQL real
- [ ] Configurar envío de emails
- [ ] Habilitar HTTPS
- [ ] Configurar CORS para tu dominio
- [ ] Probar todas las funcionalidades
- [ ] Configurar logs en producción