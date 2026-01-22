#!/bin/bash

echo "🚀 Desplegando tu app de fitness a GitHub Pages..."

# Configurar git si no está configurado
if ! git config --global user.name; then
    echo "Por favor, configura tu nombre de usuario:"
    echo "git config --global user.name 'Tu Nombre'"
    echo "git config --global user.email 'tu-email@example.com'"
    exit 1
fi

# Inicializar repositorio
git init
git add .
git commit -m "Initial commit: Fitness App with PWA support"

# Agregar remote (reemplaza con tu usuario)
echo "Reemplaza 'TU_USERNAME' con tu usuario de GitHub:"
echo "git remote add origin https://github.com/TU_USERNAME/fitness-app-personal.git"

# Push a main
echo "git branch -M main"
echo "git push -u origin main"

echo "✅ Una vez subido, ve a tu repo → Settings → Pages → Source: Deploy from a branch → Main/root"

# Activar GitHub Pages con GitHub CLI si está disponible
if command -v gh &> /dev/null; then
    echo "🎯 Activando GitHub Pages con GitHub CLI..."
    gh repo create fitness-app-personal --public --push --source=.
    gh api repos/:owner/fitness-app-personal/pages -X POST -f source[branch]=main
    echo "🌐 Tu app estará disponible en: https://TU_USERNAME.github.io/fitness-app-personal/"
fi