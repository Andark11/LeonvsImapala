#!/usr/bin/env python3
"""
Demostración Visual Simplificada - Sistema León vs Impala
Versión robusta que no se traba
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import time

def separador(titulo=""):
    """Imprime un separador visual"""
    print("\n" + "="*70)
    if titulo:
        print(f"{titulo:^70}")
        print("="*70)

def pausa(segundos=1.0):
    """Pausa para dar tiempo de leer"""
    time.sleep(segundos)

def demo_visual():
    """Demo visual explicativa del sistema"""
    
    separador("🦁 LEÓN VS IMPALA - DEMOSTRACIÓN VISUAL 🦌")
    print("\n¡Bienvenido al sistema de aprendizaje por refuerzo!")
    print("Esta demo te mostrará cómo funciona el sistema paso a paso...\n")
    pausa(2)
    
    # PARTE 1: Explicar el mapa
    separador("📍 PARTE 1: EL MAPA DEL ABREVADERO")
    print("""
    El abrevadero tiene 9 posiciones:
    
                        [Posición 1]
                           NORTE
                             🦁
                             |
                             |
            [8]              |              [2]
        NOROESTE -------(  CENTRO  )------- NORESTE
                         IMPALA 🦌
                             |
                             |
            [7]              |              [3]
         SUROESTE -------(  CENTRO  )------- SURESTE
                             |
                             |
                        [Posición 5]
                            SUR
                         [4]   [6]

    📏 Distancia: Cada posición está a 5 cuadros del centro
    🎯 Objetivo del León: Alcanzar al impala (distancia ≤ 0.5 cuadros)
    🏃 Objetivo del Impala: Detectar al león y escapar a tiempo
    """)
    pausa(3)
    
    # PARTE 2: Acciones disponibles
    separador("⚡ PARTE 2: ACCIONES DISPONIBLES")
    print("""
    🦁 EL LEÓN PUEDE:
    ┌────────────────────────────────────────────────────────────┐
    │ 1. AVANZAR     → Mueve 1 cuadro hacia el impala          │
    │ 2. ESCONDERSE  → Se oculta (impala no lo ve)             │
    │ 3. ATACAR      → Corre 2 cuadros/turno (¡MUY RÁPIDO!)    │
    │ 4. SITUARSE    → Se mantiene en su posición              │
    └────────────────────────────────────────────────────────────┘
    
    🦌 EL IMPALA PUEDE:
    ┌────────────────────────────────────────────────────────────┐
    │ 1. VER (izq/der/frente) → Mira 120° en esa dirección    │
    │ 2. BEBER AGUA          → Bebe (NO puede ver)             │
    │ 3. HUIR                → Escapa acelerando progresivamente│
    │                          (1→2→3→4... cuadros/turno)      │
    └────────────────────────────────────────────────────────────┘
    """)
    pausa(3)
    
    # PARTE 3: Condiciones de huida
    separador("⚠️  PARTE 3: ¿CUÁNDO HUYE EL IMPALA?")
    print("""
    El impala comienza a huir cuando:
    
    ❗ CONDICIÓN 1: Ve al león
       • El león está dentro de su ángulo de visión (120°)
       • Y el león NO está escondido
    
    ❗ CONDICIÓN 2: León inicia ataque
       • El impala escucha al león corriendo
       • Automáticamente huye sin importar posición
    
    ❗ CONDICIÓN 3: León demasiado cerca
       • Distancia < 3 cuadros
       • Instinto de supervivencia
    
    💨 VELOCIDAD DE HUIDA:
       • Turno 1: 1 cuadro/turno
       • Turno 2: 2 cuadros/turno
       • Turno 3: 3 cuadros/turno
       • Y así sucesivamente... ¡acelera constantemente!
    """)
    pausa(4)
    
    # PARTE 4: Ejemplo de cacería
    separador("🎬 PARTE 4: EJEMPLO DE CACERÍA")
    print("\nVamos a simular una cacería paso a paso:\n")
    pausa(1)
    
    # Simulación manual sin ejecutar código real
    print("📍 ESTADO INICIAL:")
    print("   • León: Posición 1 (Norte) - 5 cuadros del impala")
    print("   • Impala: En el centro, bebiendo agua")
    print("   • Distancia: 5.0 cuadros\n")
    pausa(2)
    
    turnos = [
        {
            'num': 1,
            'accion_leon': 'AVANZAR',
            'accion_impala': 'VER_FRENTE',
            'distancia': 4.0,
            'resultado': 'León avanza sin ser detectado',
            'estado': 'Continúa la cacería'
        },
        {
            'num': 2,
            'accion_leon': 'ESCONDERSE',
            'accion_impala': 'BEBER_AGUA',
            'distancia': 4.0,
            'resultado': 'León se esconde mientras impala bebe',
            'estado': 'Posición estratégica'
        },
        {
            'num': 3,
            'accion_leon': 'AVANZAR',
            'accion_impala': 'VER_IZQUIERDA',
            'distancia': 3.0,
            'resultado': 'León avanza escondido',
            'estado': '⚠️  Zona peligrosa (< 3 cuadros)'
        },
        {
            'num': 4,
            'accion_leon': 'ATACAR',
            'accion_impala': 'VER_DERECHA → HUIR',
            'distancia': 1.5,
            'resultado': '¡Impala detecta ataque y huye!',
            'estado': '🏃 Impala huyendo a 1 cuadro/turno'
        },
        {
            'num': 5,
            'accion_leon': 'ATACAR (2 cuadros)',
            'accion_impala': 'HUIR (2 cuadros)',
            'distancia': 1.5,
            'resultado': 'León a 2 cuadros/turno, Impala a 2 cuadros/turno',
            'estado': '⚖️  Empate en velocidad'
        },
        {
            'num': 6,
            'accion_leon': 'ATACAR (2 cuadros)',
            'accion_impala': 'HUIR (3 cuadros)',
            'distancia': 2.5,
            'resultado': 'Impala acelera a 3 cuadros/turno',
            'estado': '❌ León no puede alcanzar - FRACASO'
        }
    ]
    
    for turno in turnos:
        print(f"{'─'*70}")
        print(f"⏱️  TURNO {turno['num']}")
        print(f"{'─'*70}")
        print(f"🦁 León: {turno['accion_leon']}")
        print(f"🦌 Impala: {turno['accion_impala']}")
        print(f"📏 Distancia: {turno['distancia']} cuadros")
        print(f"📊 Resultado: {turno['resultado']}")
        print(f"🎯 Estado: {turno['estado']}")
        pausa(2)
    
    print(f"\n{'='*70}")
    print("🏁 FIN DE LA CACERÍA")
    print(f"{'='*70}")
    print("❌ Resultado: FRACASO - El impala escapó")
    print("📝 Razón: Velocidad de huida superó la velocidad de ataque")
    print("💡 Lección: El león necesita atacar más cerca o cuando el impala no pueda huir")
    pausa(3)
    
    # PARTE 5: Aprendizaje
    separador("🤖 PARTE 5: CÓMO APRENDE EL LEÓN")
    print("""
    El león usa Q-LEARNING (Aprendizaje por Refuerzo):
    
    🔄 PROCESO DE APRENDIZAJE:
    
    1️⃣  EXPLORACIÓN: El león prueba diferentes acciones
       • ¿Qué pasa si avanzo cuando el impala mira?
       • ¿Y si me escondo primero?
       • ¿Cuándo es mejor atacar?
    
    2️⃣  RECOMPENSAS: Recibe puntos por sus acciones
       ✅ +100 puntos: Captura exitosa
       ✅ +1 punto: Se acerca al impala
       ✅ +5 puntos: Ataca en el momento correcto
       ❌ -50 puntos: El impala escapa
       ❌ -5 puntos: Es detectado muy lejos
    
    3️⃣  APRENDIZAJE: Después de muchas cacerías (1000s)
       • Descubre patrones exitosos
       • Evita estrategias que fallan
       • Desarrolla "intuición" de caza
    
    4️⃣  ESTRATEGIAS APRENDIDAS (ejemplos):
       💡 "Si impala mira hacia mí → esconderme"
       💡 "Si estoy cerca y escondido → avanzar sigiloso"
       💡 "Si distancia < 2 cuadros → atacar ahora"
       💡 "Si impala bebe agua → mejor momento para avanzar"
    
    🎯 RESULTADO: ¡El león aprende a cazar sin programación explícita!
    """)
    pausa(4)
    
    # PARTE 6: Estadísticas de ejemplo
    separador("📊 PARTE 6: EJEMPLO DE PROGRESO DE ENTRENAMIENTO")
    print("""
    Evolución del león durante el entrenamiento:
    
    📈 PRIMEROS 100 EPISODIOS:
       • Tasa de éxito: 5%
       • Estrategia: Aleatoria, sin patrón
       • Problema: Ataca demasiado lejos
    
    📈 1,000 EPISODIOS:
       • Tasa de éxito: 25%
       • Estrategia: Empieza a esconderse
       • Mejora: Entiende importancia de no ser visto
    
    📈 5,000 EPISODIOS:
       • Tasa de éxito: 45%
       • Estrategia: Combina esconderse + avanzar
       • Mejora: Sabe cuándo atacar
    
    📈 10,000+ EPISODIOS:
       • Tasa de éxito: 60-70%
       • Estrategia: Sofisticada y adaptativa
       • Maestría: Cazador eficiente
    
    💪 ¡El león mejora con la experiencia como un cazador real!
    """)
    pausa(3)
    
    # PARTE 7: Próximos pasos
    separador("🚀 PARTE 7: CÓMO USAR EL SISTEMA")
    print("""
    Ahora que entiendes cómo funciona, puedes:
    
    1️⃣  ENTRENAR AL LEÓN:
       $ python3 main.py
       └─ Opción 1: Sistema de Entrenamiento
          • Configura cantidad de episodios (ej: 1000)
          • Espera ~30 segundos
          • Guarda el conocimiento aprendido
    
    2️⃣  VER CACERÍAS PASO A PASO:
       $ python3 main.py
       └─ Opción 2: Visualización Paso a Paso
          • Elige posición inicial del león
          • Avanza turno por turno
          • Controla cada acción manualmente
    
    3️⃣  VER LEÓN ENTRENADO EN ACCIÓN:
       $ python3 main.py
       └─ Opción 3: Visualización con León Entrenado
          • Carga un entrenamiento guardado
          • Ve cómo el león aplica lo aprendido
          • ¡Observa estrategias inteligentes!
    
    4️⃣  EJECUTAR TESTS:
       $ python3 tests/test_basico.py
       └─ Verifica que todo funcione correctamente
    
    📚 DOCUMENTACIÓN COMPLETA:
       • README.md - Guía del usuario
       • RESUMEN_PROYECTO.md - Detalles técnicos
       • ESTADO_FINAL.txt - Verificación del sistema
    """)
    pausa(2)
    
    separador("✨ FIN DE LA DEMOSTRACIÓN VISUAL ✨")
    print("""
    🎓 RESUMEN DE LO APRENDIDO:
    
    ✅ El mapa tiene 8 posiciones + centro
    ✅ León y impala tienen diferentes acciones
    ✅ Impala huye bajo 3 condiciones específicas
    ✅ León aprende mediante Q-Learning y recompensas
    ✅ Después de miles de entrenamientos, desarrolla estrategias
    ✅ Sistema completo listo para experimentar
    
    🦁 ¡Ahora el león está listo para aprender a cazar! 🦌
    """)
    print()

if __name__ == "__main__":
    try:
        demo_visual()
    except KeyboardInterrupt:
        print("\n\n👋 Demostración interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
