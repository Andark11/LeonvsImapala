"""
León vs Impala - Sistema de Aprendizaje por Refuerzo
Punto de entrada principal del programa
"""

import sys
import os

# Agregar el directorio actual al path de Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.entrenamiento_ui import EntrenamientoUI
from ui.paso_a_paso import PasoAPasoUI
from storage.carga import cargar_conocimiento


def menu_principal():
    """Menú principal del programa"""
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                    LEÓN VS IMPALA                              ║
    ║           Sistema de Aprendizaje por Refuerzo                  ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    while True:
        print("\n" + "=" * 70)
        print("MENÚ PRINCIPAL")
        print("=" * 70)
        print("1. Sistema de Entrenamiento")
        print("2. Visualización Paso a Paso")
        print("3. Visualización con León Entrenado")
        print("4. Acerca del Proyecto")
        print("5. Salir")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == '1':
            modo_entrenamiento()
        
        elif opcion == '2':
            modo_visualizacion()
        
        elif opcion == '3':
            modo_visualizacion_entrenado()
        
        elif opcion == '4':
            mostrar_acerca_de()
        
        elif opcion == '5':
            print("\n¡Gracias por usar León vs Impala!")
            print("Desarrollado como proyecto final de Sistemas Inteligentes\n")
            break
        
        else:
            print("\n❌ Opción inválida")


def modo_entrenamiento():
    """Modo de entrenamiento automático"""
    ui = EntrenamientoUI()
    ui.menu_principal()


def modo_visualizacion():
    """Modo de visualización paso a paso sin entrenamiento"""
    print("\n" + "=" * 70)
    print("MODO VISUALIZACIÓN - SIN ENTRENAMIENTO")
    print("=" * 70)
    print("El león tomará decisiones aleatorias")
    
    ui = PasoAPasoUI()
    
    try:
        posicion = int(input("\nPosición inicial del león (1-8, Enter=1): ").strip() or "1")
        if not 1 <= posicion <= 8:
            posicion = 1
    except:
        posicion = 1
    
    print("\nTipo de visualización:")
    print("1. Paso a paso (manual)")
    print("2. Automática (con delay)")
    
    tipo = input("Selecciona (1/2, Enter=1): ").strip() or "1"
    
    try:
        if tipo == '2':
            delay = float(input("Delay entre turnos en segundos (Enter=1.0): ").strip() or "1.0")
            ui.visualizar_con_delay(posicion, delay)
        else:
            ui.visualizar_caceria(posicion)
    except KeyboardInterrupt:
        print("\n\nVisualización interrumpida")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def modo_visualizacion_entrenado():
    """Modo de visualización con león entrenado"""
    print("\n" + "=" * 70)
    print("MODO VISUALIZACIÓN - CON LEÓN ENTRENADO")
    print("=" * 70)
    
    from storage.guardado import listar_guardados
    
    guardados = listar_guardados("datos")
    
    if not guardados:
        print("\n❌ No hay entrenamientos guardados")
        print("Primero debes entrenar al león usando la opción 1 del menú principal")
        return
    
    print("\nEntrenamientos disponibles:")
    for i, guardado in enumerate(guardados, 1):
        print(f"{i}. {guardado['archivo']} - Tasa de éxito: {guardado['tasa_exito']}%")
    
    try:
        seleccion = int(input("\nSelecciona un entrenamiento (número): ")) - 1
        if not 0 <= seleccion < len(guardados):
            print("❌ Selección inválida")
            return
        
        guardado = guardados[seleccion]
        
        # Cargar conocimiento
        print(f"\nCargando {guardado['archivo']}...")
        bc = cargar_conocimiento(guardado['ruta'])
        
        if not bc:
            print("❌ Error al cargar el conocimiento")
            return
        
        print(f"✓ Conocimiento cargado exitosamente")
        print(f"  Estados únicos: {guardado['estados']}")
        print(f"  Tasa de éxito: {guardado['tasa_exito']}%")
        
        # Crear UI con conocimiento
        ui = PasoAPasoUI(base_conocimientos=bc)
        
        posicion = int(input("\nPosición inicial del león (1-8, Enter=1): ").strip() or "1")
        if not 1 <= posicion <= 8:
            posicion = 1
        
        print("\nTipo de visualización:")
        print("1. Paso a paso (manual)")
        print("2. Automática (con delay)")
        
        tipo = input("Selecciona (1/2, Enter=1): ").strip() or "1"
        
        if tipo == '2':
            delay = float(input("Delay entre turnos en segundos (Enter=1.0): ").strip() or "1.0")
            ui.visualizar_con_delay(posicion, delay)
        else:
            ui.visualizar_caceria(posicion)
    
    except KeyboardInterrupt:
        print("\n\nVisualización interrumpida")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def mostrar_acerca_de():
    """Muestra información del proyecto"""
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                  ACERCA DE LEÓN VS IMPALA                      ║
    ╚════════════════════════════════════════════════════════════════╝
    
    DESCRIPCIÓN:
    Sistema de aprendizaje automático donde un león joven aprende a 
    cazar un impala en un abrevadero mediante aprendizaje por refuerzo.
    
    CARACTERÍSTICAS:
    • Aprendizaje basado en Q-Learning
    • Entrenamiento automático de miles de episodios
    • Generalización de conocimiento
    • Visualización paso a paso
    • Persistencia de conocimiento aprendido
    
    COMPONENTES:
    • Entorno: Abrevadero con 8 posiciones
    • Agentes: León (aprende) e Impala (presa)
    • Aprendizaje: Algoritmo Q-Learning
    • Base de conocimientos: Estados → Acciones → Resultados
    
    REGLAS DEL JUEGO:
    1. El impala actúa primero (ver, beber, huir)
    2. El león reacciona (avanzar, esconderse, atacar)
    3. El impala huye si detecta al león o si está muy cerca
    4. El león gana si alcanza al impala
    5. El león pierde si el impala escapa
    
    VELOCIDADES:
    • León avanzando: 1 cuadro/turno
    • León atacando: 2 cuadros/turno
    • Impala huyendo: 1, 2, 3, 4... cuadros/turno (acelera)
    
    DESARROLLO:
    Arquitectura modular en Python con separación de responsabilidades:
    - environment.py: Mapa y geometría
    - agents/: Comportamiento de león e impala
    - simulation/: Lógica de cacería
    - knowledge/: Base de conocimientos y generalización
    - learning/: Q-Learning y entrenamiento
    - ui/: Interfaces de usuario
    - storage/: Persistencia
    
    TECNOLOGÍAS:
    • Python 3.8+
    • Q-Learning (Reinforcement Learning)
    • Arquitectura modular y orientada a objetos
    
    PROYECTO FINAL - SISTEMAS INTELIGENTES
    """)
    
    input("\nPresiona Enter para continuar...")


def verificar_directorios():
    """Verifica y crea directorios necesarios"""
    directorios = ['datos', 'tests']
    for directorio in directorios:
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f"✓ Creado directorio: {directorio}")


if __name__ == "__main__":
    try:
        # Verificar directorios necesarios
        verificar_directorios()
        
        # Iniciar menú principal
        menu_principal()
    
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
