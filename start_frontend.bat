@echo off

cd email-assistant

echo Instalando dependencias del frontend...
call npm install

echo Iniciando el servidor de desarrollo del frontend...
call npm run dev