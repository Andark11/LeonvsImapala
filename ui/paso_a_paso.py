"""
Interfaz para visualización paso a paso de cacerías.
"""

from typing import Optional
import time

from environment import Abrevadero
from simulation.caceria import Caceria, ModoBehaviorImpala, AccionLeon
from agents.leon import Leon
from agents.impala import Impala
from knowledge.base_conocimientos import BaseConocimientos


class PasoAPasoUI:
    """
    Interfaz para visualizar cacerías paso a paso.
    """
    
    def __init__(self, base_conocimientos: Optional[BaseConocimientos] = None):
        """
        Inicializa la interfaz.
        
        Args:
            base_conocimientos: Base de conocimientos del león (opcional)
        """
        self.abrevadero = Abrevadero()
        self.caceria = Caceria(self.abrevadero)
        self.base_conocimientos = base_conocimientos
    
    def visualizar_caceria(self, posicion_inicial: int = 1,
                          comportamiento_impala: ModoBehaviorImpala = ModoBehaviorImpala.ALEATORIO):
        """
        Visualiza una cacería paso a paso.
        
        Args:
            posicion_inicial: Posición inicial del león
            comportamiento_impala: Comportamiento del impala
        """
        print("\n" + "=" * 70)
        print("VISUALIZACIÓN PASO A PASO - CACERÍA")
        print("=" * 70)
        
        # Inicializar cacería
        self.caceria.inicializar_caceria(posicion_inicial, comportamiento_impala)
        
        print(f"\nPosición inicial del león: {posicion_inicial}")
        print(f"Comportamiento del impala: {comportamiento_impala.value}")
        print("\nPresiona Enter para avanzar cada turno, 'q' para terminar")
        input("\nPresiona Enter para comenzar...")
        
        turno = 0
        acciones_leon = ["avanzar", "esconderse", "atacar"]
        
        while self.caceria.resultado.value == "en_progreso":
            turno += 1
            
            # Mostrar estado actual
            self._mostrar_estado_turno(turno)
            
            # Decidir acción del león
            if self.base_conocimientos:
                accion = self._decidir_accion_con_conocimiento(acciones_leon)
            else:
                accion = self._pedir_accion_usuario(acciones_leon)
            
            if accion == 'q':
                print("\nCacería interrumpida por el usuario")
                break
            
            # Ejecutar turno
            terminada, mensaje = self.caceria.ejecutar_turno(AccionLeon[accion.upper()])
            
            # Mostrar resultado del turno
            self._mostrar_resultado_turno()
            
            if terminada:
                print(f"\n{'=' * 70}")
                print(f"CACERÍA TERMINADA: {mensaje}")
                print(f"{'=' * 70}")
                break
            
            # Esperar input del usuario
            entrada = input("\nPresiona Enter para continuar, 'q' para salir: ").strip().lower()
            if entrada == 'q':
                print("\nVisualización interrumpida")
                break
        
        # Mostrar resumen
        self._mostrar_resumen()
    
    def _mostrar_estado_turno(self, turno: int):
        """Muestra el estado del mundo en un turno"""
        print("\n" + "-" * 70)
        print(f"TURNO {turno}")
        print("-" * 70)
        
        leon = self.caceria.leon
        impala = self.caceria.impala
        
        distancia = self.caceria.verificador.calcular_distancia_actual(leon)
        
        print(f"\nLEÓN:")
        print(f"  Posición: {leon.posicion}")
        print(f"  Escondido: {'Sí' if leon.esta_escondido else 'No'}")
        print(f"  Atacando: {'Sí' if leon.esta_atacando else 'No'}")
        
        print(f"\nIMPALA:")
        print(f"  En el centro (bebiendo/mirando)")
        print(f"  Huyendo: {'Sí' if impala.esta_huyendo else 'No'}")
        if impala.esta_huyendo:
            print(f"  Velocidad de huida: {impala.velocidad_huida} cuadros/T")
            print(f"  Distancia recorrida: {impala.distancia_huida:.1f} cuadros")
        
        print(f"\nDISTANCIA: {distancia:.2f} cuadros")
    
    def _decidir_accion_con_conocimiento(self, acciones: list) -> str:
        """Decide la acción usando la base de conocimientos"""
        # Crear estado actual
        from knowledge.base_conocimientos import Estado
        
        distancia = self.caceria.verificador.calcular_distancia_actual(self.caceria.leon)
        
        estado = Estado(
            posicion_leon=self.caceria.leon.posicion,
            distancia_impala=round(distancia * 2) / 2,
            accion_impala="ver_frente",  # Simplificado
            leon_escondido=self.caceria.leon.esta_escondido,
            impala_puede_ver=self.caceria.impala.puede_ver_leon
        )
        
        # Obtener mejor acción
        accion, valor_q = self.base_conocimientos.obtener_mejor_accion(estado, acciones)
        
        print(f"\nACCIÓN DECIDIDA POR EL LEÓN: {accion.upper()}")
        print(f"Valor Q: {valor_q:.2f}")
        print(f"(Basado en conocimiento aprendido)")
        
        return accion
    
    def _pedir_accion_usuario(self, acciones: list) -> str:
        """Pide al usuario que elija una acción"""
        print("\nACCIONES DISPONIBLES:")
        for i, accion in enumerate(acciones, 1):
            print(f"  {i}. {accion.capitalize()}")
        
        while True:
            entrada = input("\nSelecciona una acción (número o nombre): ").strip().lower()
            
            if entrada == 'q':
                return 'q'
            
            # Verificar si es un número
            try:
                indice = int(entrada) - 1
                if 0 <= indice < len(acciones):
                    return acciones[indice]
            except:
                pass
            
            # Verificar si es un nombre
            if entrada in acciones:
                return entrada
            
            print("Acción inválida")
    
    def _mostrar_resultado_turno(self):
        """Muestra el resultado del último turno"""
        ultimo_evento = self.caceria.tiempo.obtener_ultimo_evento()
        
        if ultimo_evento:
            print(f"\n┌─ Acciones ejecutadas ─────────────────────────────────")
            print(f"│ Impala: {ultimo_evento.accion_impala}")
            print(f"│ León: {ultimo_evento.accion_leon}")
            print(f"│ Resultado: {ultimo_evento.resultado}")
            print(f"└───────────────────────────────────────────────────────")
    
    def _mostrar_resumen(self):
        """Muestra un resumen de la cacería"""
        print("\n" + "=" * 70)
        print("RESUMEN DE LA CACERÍA")
        print("=" * 70)
        
        resumen = self.caceria.obtener_resumen()
        
        print(f"\nResultado: {resumen['resultado'].upper()}")
        print(f"Razón: {resumen['razon']}")
        print(f"Duración: {resumen['duracion']} turnos")
        
        print("\n--- Historial Completo ---")
        print(self.caceria.tiempo.generar_resumen())
    
    def visualizar_con_delay(self, posicion_inicial: int = 1,
                            delay: float = 1.0):
        """
        Visualiza una cacería con delay automático.
        
        Args:
            posicion_inicial: Posición inicial del león
            delay: Segundos entre turnos
        """
        print("\n" + "=" * 70)
        print("VISUALIZACIÓN AUTOMÁTICA - CACERÍA")
        print("=" * 70)
        
        self.caceria.inicializar_caceria(posicion_inicial, ModoBehaviorImpala.ALEATORIO)
        
        turno = 0
        acciones_leon = ["avanzar", "esconderse", "atacar"]
        
        while self.caceria.resultado.value == "en_progreso":
            turno += 1
            
            self._mostrar_estado_turno(turno)
            
            # Decidir acción
            if self.base_conocimientos:
                accion = self._decidir_accion_con_conocimiento(acciones_leon)
            else:
                import random
                accion = random.choice(acciones_leon)
                print(f"\nACCIÓN ALEATORIA: {accion.upper()}")
            
            # Ejecutar turno
            terminada, mensaje = self.caceria.ejecutar_turno(AccionLeon[accion.upper()])
            
            self._mostrar_resultado_turno()
            
            if terminada:
                print(f"\n{'=' * 70}")
                print(f"CACERÍA TERMINADA: {mensaje}")
                print(f"{'=' * 70}")
                break
            
            time.sleep(delay)
        
        self._mostrar_resumen()


if __name__ == "__main__":
    print("=== Demostración Paso a Paso ===\n")
    
    ui = PasoAPasoUI()
    
    print("Opción de visualización:")
    print("1. Paso a paso (manual)")
    print("2. Automática (con delay)")
    
    opcion = input("\nSelecciona (1/2): ").strip()
    
    posicion = int(input("Posición inicial del león (1-8): ") or "1")
    
    if opcion == '2':
        delay = float(input("Delay entre turnos (segundos): ") or "1.0")
        ui.visualizar_con_delay(posicion, delay)
    else:
        ui.visualizar_caceria(posicion)
