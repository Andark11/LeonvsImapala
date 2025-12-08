"""
Tests básicos para el proyecto León vs Impala.
Ejecutar con: python -m pytest tests/
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from environment import Abrevadero, Direccion
from agents.leon import Leon, AccionLeon
from agents.impala import Impala, AccionImpala
from simulation.caceria import Caceria, ResultadoCaceria
from knowledge.base_conocimientos import BaseConocimientos, Estado
from learning.q_learning import QLearning
from learning.recompensas import SistemaRecompensas


def test_abrevadero_coordenadas():
    """Test: Abrevadero calcula coordenadas correctamente"""
    abrevadero = Abrevadero()
    
    # Posición 1 debe estar en el norte
    x, y = abrevadero.obtener_coordenadas(1)
    assert x == 0 and y == 5
    
    # Posición 5 debe estar en el sur
    x, y = abrevadero.obtener_coordenadas(5)
    assert x == 0 and y == -5


def test_abrevadero_distancia():
    """Test: Cálculo de distancia funciona"""
    abrevadero = Abrevadero()
    
    distancia = abrevadero.calcular_distancia((0, 5), (0, 0))
    assert distancia == 5.0


def test_leon_acciones():
    """Test: León ejecuta acciones correctamente"""
    leon = Leon()
    leon.resetear(1)
    
    # Avanzar
    desc = leon.ejecutar_accion(AccionLeon.AVANZAR)
    assert "avanza" in desc.lower()
    
    # Esconderse
    leon.resetear(1)
    desc = leon.ejecutar_accion(AccionLeon.ESCONDERSE)
    assert leon.esta_escondido
    
    # Atacar
    leon.resetear(1)
    desc = leon.ejecutar_accion(AccionLeon.ATACAR)
    assert leon.esta_atacando


def test_impala_acciones():
    """Test: Impala ejecuta acciones"""
    impala = Impala()
    impala.resetear()
    
    # Ver frente
    desc = impala.ejecutar_accion(AccionImpala.VER_FRENTE)
    assert "mirando" in desc.lower()
    
    # Huir
    desc = impala.ejecutar_accion(AccionImpala.HUIR)
    assert impala.esta_huyendo
    assert impala.velocidad_huida > 0


def test_base_conocimientos():
    """Test: Base de conocimientos almacena y recupera"""
    bc = BaseConocimientos()
    
    estado = Estado(1, 5.0, "ver_frente", False, True)
    
    # Actualizar valor Q
    bc.actualizar_valor_q(estado, "avanzar", 10.5)
    
    # Recuperar valor
    valor = bc.obtener_valor_q(estado, "avanzar")
    assert valor == 10.5
    
    # Mejor acción
    mejor, valor = bc.obtener_mejor_accion(estado, ["avanzar", "esconderse"])
    assert mejor == "avanzar"


def test_q_learning_seleccion():
    """Test: Q-Learning selecciona acciones"""
    bc = BaseConocimientos()
    sr = SistemaRecompensas()
    ql = QLearning(bc, sr)
    
    estado = Estado(1, 5.0, "ver_frente", False, True)
    acciones = ["avanzar", "esconderse", "atacar"]
    
    accion, tipo = ql.seleccionar_accion(estado, acciones)
    
    assert accion in acciones
    assert tipo in ["exploración", "explotación"]


def test_recompensas():
    """Test: Sistema de recompensas calcula correctamente"""
    sr = SistemaRecompensas()
    
    # Recompensa por éxito
    r = sr.calcular_recompensa_final(True)
    assert r == 100.0
    
    # Penalización por fracaso
    r = sr.calcular_recompensa_final(False)
    assert r == -50.0
    
    # Recompensa por acercamiento
    r = sr.calcular_recompensa_acercamiento(5.0, 4.0)
    assert r > 0


def test_caceria_completa():
    """Test: Cacería completa se ejecuta"""
    abrevadero = Abrevadero()
    caceria = Caceria(abrevadero)
    
    def estrategia_simple(leon, impala, estado):
        return AccionLeon.AVANZAR
    
    resultado = caceria.ejecutar_caceria_completa(
        posicion_inicial_leon=1,
        estrategia_leon=estrategia_simple,
        verbose=False
    )
    
    # Debe terminar (éxito o fracaso)
    assert resultado in [ResultadoCaceria.EXITO, ResultadoCaceria.FRACASO]


def test_caceria_turno_a_turno():
    """Test: Cacería ejecuta turnos individuales"""
    abrevadero = Abrevadero()
    caceria = Caceria(abrevadero)
    caceria.inicializar_caceria(1)
    
    # Ejecutar algunos turnos
    for _ in range(5):
        terminada, _ = caceria.ejecutar_turno(AccionLeon.AVANZAR)
        if terminada:
            break
    
    # Debe haber registrado eventos
    assert caceria.tiempo.obtener_tiempo_actual() > 0


if __name__ == "__main__":
    print("Ejecutando tests básicos...\n")
    
    tests = [
        ("Abrevadero - Coordenadas", test_abrevadero_coordenadas),
        ("Abrevadero - Distancia", test_abrevadero_distancia),
        ("León - Acciones", test_leon_acciones),
        ("Impala - Acciones", test_impala_acciones),
        ("Base Conocimientos", test_base_conocimientos),
        ("Q-Learning - Selección", test_q_learning_seleccion),
        ("Sistema Recompensas", test_recompensas),
        ("Cacería Completa", test_caceria_completa),
        ("Cacería Turno a Turno", test_caceria_turno_a_turno),
    ]
    
    exitosos = 0
    fallidos = 0
    
    for nombre, test_func in tests:
        try:
            test_func()
            print(f"✓ {nombre}")
            exitosos += 1
        except AssertionError as e:
            print(f"✗ {nombre}: {e}")
            fallidos += 1
        except Exception as e:
            print(f"✗ {nombre}: ERROR - {e}")
            fallidos += 1
    
    print(f"\n{'=' * 50}")
    print(f"Resultados: {exitosos} exitosos, {fallidos} fallidos")
    print(f"{'=' * 50}")
