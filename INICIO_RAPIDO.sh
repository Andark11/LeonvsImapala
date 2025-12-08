#!/bin/bash

# Script de inicio rápido para León vs Impala
# Ejecutar con: bash INICIO_RAPIDO.sh

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              LEÓN VS IMPALA - INICIO RÁPIDO                    ║"
echo "║          Sistema de Aprendizaje por Refuerzo                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d" " -f2 | cut -d"." -f1-2)
echo "✓ Python detectado: $PYTHON_VERSION"

# Verificar versión mínima
if [ "${PYTHON_VERSION//./}" -lt "38" ]; then
    echo "⚠️  Se requiere Python 3.8 o superior"
    echo "   Tu versión: $PYTHON_VERSION"
    exit 1
fi

echo "✓ Versión compatible"
echo ""

# Crear directorio de datos si no existe
if [ ! -d "datos" ]; then
    mkdir datos
    echo "✓ Creado directorio 'datos/'"
fi

# Menú de opciones
echo "Selecciona una opción:"
echo ""
echo "1. Ejecutar programa principal (menú interactivo)"
echo "2. Ejecutar tests unitarios"
echo "3. Entrenamiento rápido (100 episodios)"
echo "4. Visualización de ejemplo"
echo "5. Ver documentación"
echo ""
read -p "Opción (1-5): " opcion

case $opcion in
    1)
        echo ""
        echo "Iniciando programa principal..."
        python3 main.py
        ;;
    2)
        echo ""
        echo "Ejecutando tests..."
        python3 tests/test_basico.py
        ;;
    3)
        echo ""
        echo "Ejecutando entrenamiento rápido de 100 episodios..."
        python3 -c "
from learning.entrenamiento import Entrenador

print('Iniciando entrenamiento...\n')
entrenador = Entrenador()
reporte = entrenador.entrenar(100, verbose=True)

print('\n' + '='*70)
print('RESULTADOS')
print('='*70)
print(f'Episodios: {reporte[\"episodios\"]}')
print(f'Exitosas: {reporte[\"exitosas\"]}')
print(f'Tasa de éxito: {reporte[\"tasa_exito\"]}%')
print(f'Duración: {reporte[\"duracion_segundos\"]} segundos')
print(f'Estados aprendidos: {reporte[\"estadisticas_bc\"][\"estados_unicos\"]}')
"
        ;;
    4)
        echo ""
        echo "Ejecutando visualización de ejemplo..."
        python3 -c "
from ui.paso_a_paso import PasoAPasoUI

ui = PasoAPasoUI()
print('Visualización automática de cacería (posición inicial: 1)')
print('El león toma decisiones aleatorias\n')
ui.visualizar_con_delay(1, 0.5)
"
        ;;
    5)
        echo ""
        if [ -f "RESUMEN_PROYECTO.md" ]; then
            cat RESUMEN_PROYECTO.md | less
        else
            cat README.md | less
        fi
        ;;
    *)
        echo "❌ Opción inválida"
        exit 1
        ;;
esac

echo ""
echo "✓ Proceso completado"
