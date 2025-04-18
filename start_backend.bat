@echo off

cd email-assistant-backend
echo Activando el entorno virtual de Python...
call venv\Scripts\activate

echo Instalando dependencias del backend...
pip install -r requirements.txt

echo Iniciando el servidor de desarrollo del backend...
uvicorn main:app --reload

echo El servidor se ha detenido. Desactivando el entorno virtual...
call venv\Scripts\deactivate.bat
cd ..