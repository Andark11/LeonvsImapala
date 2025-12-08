#!/usr/bin/env python3
"""
Demostración Visual del Sistema León vs Impala
Muestra cómo funciona una cacería paso a paso
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from environment import Abrevadero
from simulation.caceria import Caceria, ModoBehaviorImpala, AccionLeon
from agents.impala import AccionImpala
import time

def mostrar_mapa_abrevadero():
    """Muestra una representación visual del abrevadero"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║              MAPA DEL ABREVADERO (Vista Superior)            ║
    ╚══════════════════════════════════════════════════════════════╝
    
                            [1] Norte
                             🦁 
                              |
                              |
              [8]             |             [2]
         Noroeste ---------(Centro)--------- Noreste
                           IMPALA 🦌
                              |
                              |
              [7]             |             [3]
          Suroeste ---------(Centro)--------- Sureste
                              |
                              |
                            [6] Sur
                           [4][5]
    
    • El IMPALA está siempre en el centro bebiendo agua
    • El LEÓN empieza en una de las 8 posiciones (1-8)
    • Cada posición está a 5 cuadros del centro
    • Posiciones numeradas: 1=Norte, 2=NE, 3=E, 4=SE, 5=S, 6=SO, 7=O, 8=NO
    """)

def mostrar_caceria_simple():
    """Muestra una cacería simple paso a paso"""
    print("\n" + "="*70)
    print("DEMOSTRACIÓN: CACERÍA PASO A PASO")
    print("="*70)
    
    # Crear cacería
    abrevadero = Abrevadero()
    caceria = Caceria(abrevadero)
    
    # Configurar: León en posición 1 (Norte)
    posicion_inicial = 1
    print(f"\n📍 Posición inicial del león: {posicion_inicial} (Norte)")
    print(f"📍 Impala en el centro bebiendo agua")
    print(f"📏 Distancia inicial: 5.0 cuadros\n")
    
    # Inicializar cacería con comportamiento aleatorio del impala
    caceria.inicializar_caceria(posicion_inicial, ModoBehaviorImpala.ALEATORIO)
    
    turno = 0
    acciones_leon = [
        AccionLeon.AVANZAR,
        AccionLeon.AVANZAR,
        AccionLeon.ESCONDERSE,
        AccionLeon.AVANZAR,
        AccionLeon.ATACAR,
    ]
    
    print("🎬 INICIO DE LA CACERÍA")
    print("-" * 70)
    
    for accion in acciones_leon:
        if caceria.resultado.value != "en_progreso":
            break
        
        turno += 1
        
        # Estado antes del turno
        distancia_antes = caceria.verificador.calcular_distancia_actual(caceria.leon)
        
        print(f"\n⏱️  TURNO {turno}")
        print(f"   León en posición: {caceria.leon.posicion}")
        print(f"   Distancia: {distancia_antes:.1f} cuadros")
        print(f"   León escondido: {'Sí' if caceria.leon.esta_escondido else 'No'}")
        
        # Ejecutar turno
        terminada, mensaje = caceria.ejecutar_turno(accion)
        
        # Mostrar qué pasó
        ultimo_evento = caceria.tiempo.obtener_ultimo_evento()
        if ultimo_evento:
            print(f"\n   🦌 Impala: {ultimo_evento.accion_impala}")
            print(f"   🦁 León: {ultimo_evento.accion_leon}")
            
            if caceria.impala.esta_huyendo:
                print(f"   ⚠️  ¡IMPALA HUYENDO! Velocidad: {caceria.impala.velocidad_huida} cuadros/turno")
        
        if terminada:
            print(f"\n{'='*70}")
            print(f"🏁 FIN DE LA CACERÍA")
            print(f"{'='*70}")
            print(f"Resultado: {caceria.resultado.value.upper()}")
            print(f"Razón: {mensaje}")
            print(f"Duración: {turno} turnos")
            break
        
        time.sleep(0.5)  # Pausa para leer
    
    # Mostrar resumen
    print(f"\n{'='*70}")
    print("📊 HISTORIAL COMPLETO")
    print("="*70)
    print(caceria.tiempo.generar_resumen())

def mostrar_explicacion_conceptos():
    """Explica los conceptos clave del sistema"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║           CONCEPTOS CLAVE DEL SISTEMA                        ║
    ╚══════════════════════════════════════════════════════════════╝
    
    🦁 ACCIONES DEL LEÓN:
    ─────────────────────
    • AVANZAR: Se mueve 1 cuadro hacia el impala
    • ESCONDERSE: Se oculta (impala no puede verlo)
    • ATACAR: Corre rápido 2 cuadros/turno hacia el impala
    • SITUARSE: Mantiene posición actual
    
    🦌 ACCIONES DEL IMPALA:
    ──────────────────────
    • VER_IZQUIERDA: Mira 120° a su izquierda
    • VER_DERECHA: Mira 120° a su derecha
    • VER_FRENTE: Mira 120° al frente
    • BEBER_AGUA: Bebe (no puede ver)
    • HUIR: Escapa acelerando progresivamente (1→2→3→4...)
    
    ⚠️  CONDICIONES DE HUIDA DEL IMPALA:
    ───────────────────────────────────
    1. Ve al león (dentro de su ángulo de visión Y león NO escondido)
    2. León inicia ATAQUE (impala lo escucha)
    3. Distancia < 3 cuadros (instinto de supervivencia)
    
    🎯 OBJETIVOS:
    ────────────
    • LEÓN: Alcanzar al impala (distancia ≤ 0.5 cuadros)
    • IMPALA: Escapar antes de ser alcanzado
    
    🤖 APRENDIZAJE:
    ──────────────
    • El león NO tiene estrategia preprogramada
    • Aprende mediante Q-Learning (prueba y error)
    • Recibe recompensas (+) o penalizaciones (-)
    • Con miles de intentos, descubre la mejor estrategia
    
    💡 ESTRATEGIA ÓPTIMA (que el león debe aprender):
    ────────────────────────────────────────────────
    1. Esconderse cuando el impala puede verlo
    2. Avanzar cautelosamente cuando está escondido
    3. Atacar solo cuando está MUY cerca (< 2 cuadros)
    4. Evitar ser detectado tempranamente
    """)

def menu_demostracion():
    """Menú de demostración"""
    while True:
        print("\n" + "="*70)
        print("DEMOSTRACIÓN VISUAL - LEÓN VS IMPALA")
        print("="*70)
        print("1. Ver mapa del abrevadero")
        print("2. Ver cacería simple paso a paso")
        print("3. Explicación de conceptos clave")
        print("4. Ver todas las demos en secuencia")
        print("5. Salir")
        
        try:
            opcion = input("\nSelecciona una opción (1-5): ").strip()
            
            if opcion == '1':
                mostrar_mapa_abrevadero()
            elif opcion == '2':
                mostrar_caceria_simple()
            elif opcion == '3':
                mostrar_explicacion_conceptos()
            elif opcion == '4':
                mostrar_mapa_abrevadero()
                input("\nPresiona Enter para continuar...")
                mostrar_explicacion_conceptos()
                input("\nPresiona Enter para ver la cacería...")
                mostrar_caceria_simple()
            elif opcion == '5':
                print("\n👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida")
        
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrumpido")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    try:
        menu_demostracion()
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
