"""
León vs Impala - Sistema de Aprendizaje por Refuerzo
Punto de entrada principal del programa
"""

import sys
import os
import json

# Agregar el directorio actual al path de Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.entrenamiento_ui import EntrenamientoUI
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
        print("2. Simulación Visual (Grid 19×19)")
        print("3. Acerca del Proyecto")
        print("4. Salir")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == '1':
            modo_entrenamiento()
        
        elif opcion == '2':
            modo_visualizacion_terminal_grid()
        
        elif opcion == '3':
            mostrar_acerca_de()
        
        elif opcion == '4':
            print("\n¡Gracias por usar León vs Impala!")
            print("Desarrollado como proyecto final de Sistemas Inteligentes\n")
            break
        
        else:
            print("\n❌ Opción inválida")


def modo_entrenamiento():
    """Modo de entrenamiento automático"""
    ui = EntrenamientoUI()
    ui.menu_principal()


def modo_visualizacion_terminal_grid():
    """Modo de visualización con grid 19×19 en terminal (ASCII)"""
    from ui.interfaz_terminal_grid import InterfazTerminalGrid
    from learning.q_learning import QLearning
    from learning.recompensas import SistemaRecompensas
    from knowledge.base_conocimientos import BaseConocimientos
    
    print("\n" + "=" * 70)
    print("MODO VISUALIZACIÓN - GRID 19×19 EN TERMINAL")
    print("="*70)
    print("\nEsta interfaz muestra el grid en la terminal usando ASCII:")
    print("  • Grid 19×19 completo en caracteres")
    print("  • Colores ANSI para mejor visualización")
    print("  • Sin dependencias de matplotlib")
    print("  • Visualización en tiempo real")
    
    # Detectar soporte de emojis
    usar_emojis = True
    try:
        print("\n🦁🦌 ¿Puedes ver estos emojis correctamente?")
        respuesta = input("(s/n, Enter=s): ").strip().lower()
        if respuesta == 'n':
            usar_emojis = False
            print("✓ Se usarán caracteres ASCII simples (L para león, I para impala)")
    except:
        usar_emojis = False
    
    print("\n¿Qué modo deseas usar?")
    print("  1. Manual (tú decides las acciones del león)")
    print("  2. Agente entrenado (Q-Learning decide automáticamente)")
    
    modo = input("\nElige opción (1-2, Enter=1): ").strip() or "1"
    usar_agente = (modo == '2')
    
    # Crear interfaz
    base_conocimientos = BaseConocimientos()
    agente_q = None
    
    if usar_agente:
        print("\n🧠 Cargando agente entrenado...")
        try:
            from storage.carga import cargar_conocimiento
            import os
            
            # Buscar archivos de conocimiento disponibles
            ruta_datos = "modelos"
            archivos = []
            if os.path.exists(ruta_datos):
                archivos = sorted([f for f in os.listdir(ruta_datos) if f.endswith("_conocimiento.json")])
            
            if archivos:
                print("\n📂 Bases de conocimiento disponibles:")
                for i, archivo in enumerate(archivos, 1):
                    # Obtener tamaño del archivo
                    ruta = os.path.join(ruta_datos, archivo)
                    tamaño_kb = os.path.getsize(ruta) / 1024
                    print(f"   {i}. {archivo} ({tamaño_kb:.1f} KB)")
                
                # Preguntar cuál usar
                seleccion = input(f"\n¿Cuál usar? (1-{len(archivos)}, Enter={len(archivos)}): ").strip()
                if seleccion == "":
                    indice = len(archivos) - 1  # Último (más reciente)
                else:
                    try:
                        indice = int(seleccion) - 1
                        indice = max(0, min(len(archivos) - 1, indice))
                    except:
                        indice = len(archivos) - 1
                
                archivo_seleccionado = archivos[indice]
                ruta_completa = os.path.join(ruta_datos, archivo_seleccionado)
                print(f"\n📥 Cargando: {archivo_seleccionado}")
                
                # Cargar también el archivo de configuración para verificar el RADIO
                archivo_config = archivo_seleccionado.replace("_conocimiento.json", "_config.json")
                ruta_config = os.path.join(ruta_datos, archivo_config)
                radio_entrenamiento = None
                if os.path.exists(ruta_config):
                    try:
                        with open(ruta_config, 'r') as f:
                            config_data = json.load(f)
                            if 'abrevadero' in config_data:
                                radio_entrenamiento = config_data['abrevadero'].get('RADIO')
                    except:
                        pass
                
                base_conocimientos = cargar_conocimiento(ruta_completa)
                if base_conocimientos:
                    print("✓ Base de conocimientos cargada")
                    
                    # Verificar compatibilidad de RADIO
                    from environment import Abrevadero
                    radio_actual = Abrevadero.RADIO
                    
                    if radio_entrenamiento:
                        print(f"   RADIO de entrenamiento: {radio_entrenamiento}")
                        print(f"   RADIO actual: {radio_actual}")
                        
                        if abs(radio_entrenamiento - radio_actual) > 0.1:
                            print("\n⚠️  ADVERTENCIA: El RADIO cambió")
                            print(f"   Este conocimiento fue entrenado con RADIO={radio_entrenamiento}")
                            print(f"   El RADIO actual es {radio_actual}")
                            print("   El agente puede tener peor rendimiento")
                            print("   Se recomienda re-entrenar con el nuevo RADIO")
                        else:
                            print("✓ El RADIO coincide con el del entrenamiento")
                    else:
                        print(f"\n⚠️  No se pudo determinar el RADIO de entrenamiento")
                        print(f"   (Probablemente entrenado con versión antigua)")
                        print(f"   RADIO actual: {radio_actual}")
                else:
                    print("⚠️  Error al cargar el archivo")
            else:
                print("⚠️  No se encontró conocimiento previo en 'datos/'")
                print("   Ejecuta primero la opción 1 (Entrenamiento)")
        except Exception as e:
            print(f"⚠️  Error al cargar: {e}")
            import traceback
            traceback.print_exc()
        
        sistema_recompensas = SistemaRecompensas()
        agente_q = QLearning(base_conocimientos, sistema_recompensas)
    
    interfaz = InterfazTerminalGrid(base_conocimientos, agente_q, usar_emojis)
    
    # Pedir posición inicial
    import random
    try:
        entrada = input("\n🦁 Posición inicial del león (1-8, Enter=aleatoria): ").strip()
        if entrada:
            posicion = int(entrada)
            posicion = max(1, min(8, posicion))
        else:
            posicion = random.randint(1, 8)
            print(f"   → Posición aleatoria seleccionada: {posicion}")
    except:
        posicion = random.randint(1, 8)
        print(f"   → Posición aleatoria seleccionada: {posicion}")
    
    # Delay para modo automático
    delay = 1.0
    if usar_agente:
        try:
            delay = float(input("⏱️  Delay entre turnos (segundos, Enter=1.0): ").strip() or "1.0")
        except:
            delay = 1.0
    
    # Visualizar
    try:
        interfaz.visualizar_caceria_interactiva(
            posicion_inicial=posicion,
            usar_agente_entrenado=usar_agente,
            delay=delay
        )
    except KeyboardInterrupt:
        print("\n\n👋 Visualización interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la visualización: {e}")
        import traceback
        traceback.print_exc()


def modo_visualizacion_grid():
    """Modo de visualización con grid 19×19 interactivo (matplotlib)"""
    try:
        from ui.interfaz_visual_grid import InterfazVisualGrid
        from learning.q_learning import QLearning
        from learning.recompensas import SistemaRecompensas
        from knowledge.base_conocimientos import BaseConocimientos
    except ImportError as e:
        print(f"\n❌ Error al importar módulos de visualización: {e}")
        print("Asegúrate de que matplotlib esté instalado: pip install matplotlib")
        return
    
    print("\n" + "=" * 70)
    print("MODO VISUALIZACIÓN - GRID 19×19")
    print("=" * 70)
    print("\nEsta interfaz muestra el mapa en un grid 19×19 con:")
    print("  • Posiciones del león y el impala")
    print("  • Cono de visión del impala")
    print("  • Trayectoria completa del león")
    print("  • Panel de información en tiempo real")
    
    print("\n¿Qué modo deseas usar?")
    print("  1. Manual (tú decides las acciones del león)")
    print("  2. Agente entrenado (Q-Learning decide automáticamente)")
    
    modo = input("\nElige opción (1-2, Enter=1): ").strip() or "1"
    usar_agente = (modo == '2')
    
    # Crear interfaz
    base_conocimientos = BaseConocimientos()
    agente_q = None
    
    if usar_agente:
        print("\n🧠 Cargando agente entrenado...")
        try:
            from storage.carga import cargar_conocimiento
            import os
            
            # Buscar archivos de conocimiento disponibles
            ruta_datos = "modelos"
            archivos = []
            if os.path.exists(ruta_datos):
                archivos = sorted([f for f in os.listdir(ruta_datos) if f.endswith("_conocimiento.json")])
            
            if archivos:
                print("\n📂 Bases de conocimiento disponibles:")
                for i, archivo in enumerate(archivos, 1):
                    # Obtener tamaño del archivo
                    ruta = os.path.join(ruta_datos, archivo)
                    tamaño_kb = os.path.getsize(ruta) / 1024
                    print(f"   {i}. {archivo} ({tamaño_kb:.1f} KB)")
                
                # Preguntar cuál usar
                seleccion = input(f"\n¿Cuál usar? (1-{len(archivos)}, Enter={len(archivos)}): ").strip()
                if seleccion == "":
                    indice = len(archivos) - 1  # Último (más reciente)
                else:
                    try:
                        indice = int(seleccion) - 1
                        indice = max(0, min(len(archivos) - 1, indice))
                    except:
                        indice = len(archivos) - 1
                
                archivo_seleccionado = archivos[indice]
                ruta_completa = os.path.join(ruta_datos, archivo_seleccionado)
                print(f"\n📥 Cargando: {archivo_seleccionado}")
                
                # Cargar también el archivo de configuración para verificar el RADIO
                archivo_config = archivo_seleccionado.replace("_conocimiento.json", "_config.json")
                ruta_config = os.path.join(ruta_datos, archivo_config)
                radio_entrenamiento = None
                if os.path.exists(ruta_config):
                    try:
                        with open(ruta_config, 'r') as f:
                            config_data = json.load(f)
                            if 'abrevadero' in config_data:
                                radio_entrenamiento = config_data['abrevadero'].get('RADIO')
                    except:
                        pass
                
                base_conocimientos = cargar_conocimiento(ruta_completa)
                if base_conocimientos:
                    print("✓ Base de conocimientos cargada")
                    
                    # Verificar compatibilidad de RADIO
                    from environment import Abrevadero
                    radio_actual = Abrevadero.RADIO
                    
                    if radio_entrenamiento:
                        print(f"   RADIO de entrenamiento: {radio_entrenamiento}")
                        print(f"   RADIO actual: {radio_actual}")
                        
                        if abs(radio_entrenamiento - radio_actual) > 0.1:
                            print("\n⚠️  ADVERTENCIA: El RADIO cambió")
                            print(f"   Este conocimiento fue entrenado con RADIO={radio_entrenamiento}")
                            print(f"   El RADIO actual es {radio_actual}")
                            print("   El agente puede tener peor rendimiento")
                            print("   Se recomienda re-entrenar con el nuevo RADIO")
                        else:
                            print("✓ El RADIO coincide con el del entrenamiento")
                    else:
                        print(f"\n⚠️  No se pudo determinar el RADIO de entrenamiento")
                        print(f"   (Probablemente entrenado con versión antigua)")
                        print(f"   RADIO actual: {radio_actual}")
                    
                    sistema_recompensas = SistemaRecompensas()
                    agente_q = QLearning(base_conocimientos, sistema_recompensas)
                else:
                    print("⚠️  Error al cargar el archivo")
                    print("Se usará un agente sin entrenamiento")
                    sistema_recompensas = SistemaRecompensas()
                    agente_q = QLearning(base_conocimientos, sistema_recompensas)
            else:
                print("⚠️  No se encontró conocimiento previo en 'datos/'")
                print("   Ejecuta primero la opción 1 (Entrenamiento)")
                print("Se usará un agente sin entrenamiento")
                sistema_recompensas = SistemaRecompensas()
                agente_q = QLearning(base_conocimientos, sistema_recompensas)
        except Exception as e:
            print(f"⚠️  Error al cargar: {e}")
            print("Se usará un agente sin entrenamiento")
            import traceback
            traceback.print_exc()
    
    interfaz = InterfazVisualGrid(base_conocimientos, agente_q)
    
    # Pedir posición inicial
    import random
    try:
        entrada = input("\n🦁 Posición inicial del león (1-8, Enter=aleatoria): ").strip()
        if entrada:
            posicion = int(entrada)
            posicion = max(1, min(8, posicion))
        else:
            posicion = random.randint(1, 8)
            print(f"   → Posición aleatoria seleccionada: {posicion}")
    except:
        posicion = random.randint(1, 8)
        print(f"   → Posición aleatoria seleccionada: {posicion}")
    
    # Visualizar
    try:
        interfaz.visualizar_caceria_interactiva(
            posicion_inicial=posicion,
            usar_agente_entrenado=usar_agente
        )
    except KeyboardInterrupt:
        print("\n\n👋 Visualización interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la visualización: {e}")
        import traceback
        traceback.print_exc()


def modo_visualizacion():
    """Modo de visualización paso a paso sin entrenamiento"""
    print("\n" + "=" * 70)
    print("MODO VISUALIZACIÓN - SIN ENTRENAMIENTO (TEXTO)")
    print("=" * 70)
    print("El león tomará decisiones aleatorias")
    
    ui = PasoAPasoUI()
    
    import random
    try:
        entrada = input("\nPosición inicial del león (1-8, Enter=aleatoria): ").strip()
        if entrada:
            posicion = int(entrada)
            if not 1 <= posicion <= 8:
                posicion = 1
        else:
            posicion = random.randint(1, 8)
            print(f"   → Posición aleatoria seleccionada: {posicion}")
    except:
        posicion = random.randint(1, 8)
        print(f"   → Posición aleatoria seleccionada: {posicion}")
    
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
    
    guardados = listar_guardados("modelos")
    
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
        
        import random
        entrada = input("\nPosición inicial del león (1-8, Enter=aleatoria): ").strip()
        if entrada:
            posicion = int(entrada)
            if not 1 <= posicion <= 8:
                posicion = 1
        else:
            posicion = random.randint(1, 8)
            print(f"   → Posición aleatoria seleccionada: {posicion}")
        
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
    directorios = ['modelos']
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
