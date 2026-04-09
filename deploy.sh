# Script de despliegue para BeToDo

echo "=== DESPLIEGUE DE BETODO ==="

# Backend
echo "Configurando backend..."
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configurar .env (debes editarlo manualmente)
echo "Recuerda configurar el archivo .env en backend/ con tus credenciales reales"

# Frontend
echo "Construyendo frontend..."
cd ../frontend
npm install
npm run build

echo "=== DESPLIEGUE COMPLETADO ==="
echo "Para ejecutar localmente:"
echo "  Backend: cd backend && python wsgi.py"
echo "  Frontend: Los archivos están en frontend/dist/ - sírvelos con un servidor web"