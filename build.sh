#!/bin/bash
# Script de build para Railway

echo "📦 Instalando dependencias de Python..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "✅ Dependencias instaladas correctamente"
