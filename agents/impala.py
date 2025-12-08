"""
Módulo del agente Impala.
Define el comportamiento y acciones del impala.
"""

from enum import Enum
from typing import List, Optional
import random
from environment import Direccion


class AccionImpala(Enum):
    """Acciones posibles del impala"""
    VER_IZQUIERDA = "ver_izquierda"
    VER_DERECHA = "ver_derecha"
    VER_FRENTE = "ver_frente"
    BEBER_AGUA = "beber_agua"
    HUIR = "huir"


class Impala:
    """
    Representa al impala en el abrevadero.
    
    Attributes:
        direccion_vista: Dirección hacia donde está mirando
        esta_huyendo: Indica si el impala está en modo de huida
        velocidad_huida: Velocidad actual de huida (aumenta progresivamente)
        direccion_huida: Dirección de la huida (este u oeste)
    """
    
    def __init__(self, direccion_inicial: Direccion = Direccion.NORTE):
        """
        Inicializa el impala.
        
        Args:
            direccion_inicial: Dirección inicial hacia donde mira el impala
        """
        self.direccion_vista = direccion_inicial
        self.esta_huyendo = False
        self.velocidad_huida = 0
        self.direccion_huida: Optional[Direccion] = None
        self.tiempo_huyendo = 0
        self.posicion_leon_detectada: Optional[int] = None
    
    def resetear(self):
        """Resetea el estado del impala a su estado inicial"""
        self.direccion_vista = Direccion.NORTE
        self.esta_huyendo = False
        self.velocidad_huida = 0
        self.direccion_huida = None
        self.tiempo_huyendo = 0
        self.posicion_leon_detectada = None
    
    def ejecutar_accion(self, accion: AccionImpala) -> str:
        """
        Ejecuta una acción del impala.
        
        Args:
            accion: Acción a ejecutar
            
        Returns:
            Descripción de lo que ocurrió
        """
        if self.esta_huyendo:
            return self._continuar_huida()
        
        if accion == AccionImpala.VER_IZQUIERDA:
            return self._ver_izquierda()
        elif accion == AccionImpala.VER_DERECHA:
            return self._ver_derecha()
        elif accion == AccionImpala.VER_FRENTE:
            return self._ver_frente()
        elif accion == AccionImpala.BEBER_AGUA:
            return self._beber_agua()
        elif accion == AccionImpala.HUIR:
            return self._iniciar_huida()
        else:
            raise ValueError(f"Acción desconocida: {accion}")
    
    def _ver_izquierda(self) -> str:
        """Gira la vista 90 grados a la izquierda"""
        angulo_actual = self.direccion_vista.value
        nuevo_angulo = (angulo_actual - 90) % 360
        
        # Encontrar la dirección más cercana
        self.direccion_vista = self._angulo_a_direccion(nuevo_angulo)
        
        return f"Impala gira su vista a la izquierda (ahora mira hacia {self.direccion_vista.name})"
    
    def _ver_derecha(self) -> str:
        """Gira la vista 90 grados a la derecha"""
        angulo_actual = self.direccion_vista.value
        nuevo_angulo = (angulo_actual + 90) % 360
        
        self.direccion_vista = self._angulo_a_direccion(nuevo_angulo)
        
        return f"Impala gira su vista a la derecha (ahora mira hacia {self.direccion_vista.name})"
    
    def _ver_frente(self) -> str:
        """Mantiene la vista al frente"""
        return f"Impala mantiene su vista al frente (mirando hacia {self.direccion_vista.name})"
    
    def _beber_agua(self) -> str:
        """
        Bebe agua. Cuando bebe, solo ve su reflejo (no puede ver al león).
        """
        return "Impala baja su cabeza y bebe agua (no puede ver nada)"
    
    def _iniciar_huida(self) -> str:
        """Inicia la huida del impala"""
        self.esta_huyendo = True
        self.velocidad_huida = 1
        self.tiempo_huyendo = 1
        
        # Determinar dirección de huida basada en la posición del león
        if self.posicion_leon_detectada is not None:
            # Huir en dirección opuesta al león
            # Si león está en Este (3) → huir Oeste (7)
            # Si león está en Oeste (7) → huir Este (3)
            # Si león está en Norte (1) → huir Sur (5)
            # Si león está en Sur (5) → huir Norte (1)
            # Para otras posiciones, elegir el más lejano (Este u Oeste)
            
            if self.posicion_leon_detectada in [1, 2, 8]:  # Norte, NE, NO
                self.direccion_huida = Direccion.SUR
            elif self.posicion_leon_detectada in [5, 6, 4]:  # Sur, SO, SE
                self.direccion_huida = Direccion.NORTE
            elif self.posicion_leon_detectada == 3:  # Este
                self.direccion_huida = Direccion.OESTE
            elif self.posicion_leon_detectada == 7:  # Oeste
                self.direccion_huida = Direccion.ESTE
            else:
                # Por defecto, elegir aleatoriamente
                self.direccion_huida = random.choice([Direccion.ESTE, Direccion.OESTE])
        else:
            # Si no sabe dónde está el león, huir aleatoriamente (Este u Oeste)
            self.direccion_huida = random.choice([Direccion.ESTE, Direccion.OESTE])
        
        return f"¡IMPALA INICIA HUIDA hacia {self.direccion_huida.name}! (Velocidad: {self.velocidad_huida} cuadros/T)"
    
    def _continuar_huida(self) -> str:
        """Continúa la huida aumentando la velocidad"""
        self.tiempo_huyendo += 1
        self.velocidad_huida = self.tiempo_huyendo
        
        return f"Impala continúa huyendo hacia {self.direccion_huida.name} (Velocidad: {self.velocidad_huida} cuadros/T)"
    
    def _angulo_a_direccion(self, angulo: float) -> Direccion:
        """
        Convierte un ángulo a la dirección cardinal más cercana.
        
        Args:
            angulo: Ángulo en grados (0-360)
            
        Returns:
            Dirección cardinal correspondiente
        """
        angulo = angulo % 360
        
        direcciones = [
            (0, Direccion.NORTE),
            (45, Direccion.NORESTE),
            (90, Direccion.ESTE),
            (135, Direccion.SURESTE),
            (180, Direccion.SUR),
            (225, Direccion.SUROESTE),
            (270, Direccion.OESTE),
            (315, Direccion.NOROESTE),
        ]
        
        # Encontrar la dirección más cercana
        min_diff = float('inf')
        direccion_cercana = Direccion.NORTE
        
        for ang, dir in direcciones:
            diff = abs(angulo - ang)
            if diff > 180:
                diff = 360 - diff
            
            if diff < min_diff:
                min_diff = diff
                direccion_cercana = dir
        
        return direccion_cercana
    
    def puede_ver_posicion(self, angulo_objetivo: float, bebiendo: bool = False) -> bool:
        """
        Verifica si el impala puede ver una posición específica.
        
        Args:
            angulo_objetivo: Ángulo hacia la posición objetivo
            bebiendo: Si el impala está bebiendo agua
            
        Returns:
            True si puede ver la posición, False en caso contrario
        """
        if bebiendo:
            return False
        
        dir_actual = self.direccion_vista.value
        diff = abs(angulo_objetivo - dir_actual)
        if diff > 180:
            diff = 360 - diff
        
        # Ángulo de visión: 120 grados (60 a cada lado)
        return diff <= 60
    
    def generar_secuencia_aleatoria(self, longitud: int) -> List[AccionImpala]:
        """
        Genera una secuencia aleatoria de acciones (excluyendo HUIR).
        
        Args:
            longitud: Número de acciones a generar
            
        Returns:
            Lista de acciones aleatorias
        """
        acciones_posibles = [
            AccionImpala.VER_IZQUIERDA,
            AccionImpala.VER_DERECHA,
            AccionImpala.VER_FRENTE,
            AccionImpala.BEBER_AGUA
        ]
        
        return [random.choice(acciones_posibles) for _ in range(longitud)]
    
    def __str__(self) -> str:
        """Representación en string del impala"""
        estado = "HUYENDO" if self.esta_huyendo else "TRANQUILO"
        return f"Impala(Estado={estado}, Mirando={self.direccion_vista.name})"


if __name__ == "__main__":
    # Pruebas básicas
    print("=== Pruebas del Impala ===\n")
    
    impala = Impala()
    print(f"Estado inicial: {impala}\n")
    
    # Probar acciones
    acciones = [
        AccionImpala.VER_FRENTE,
        AccionImpala.VER_IZQUIERDA,
        AccionImpala.VER_DERECHA,
        AccionImpala.BEBER_AGUA,
    ]
    
    for accion in acciones:
        resultado = impala.ejecutar_accion(accion)
        print(f"{accion.value}: {resultado}")
    
    # Probar huida
    print("\n--- Iniciando huida ---")
    for i in range(5):
        resultado = impala.ejecutar_accion(AccionImpala.HUIR if i == 0 else AccionImpala.VER_FRENTE)
        print(f"T{i+1}: {resultado}")
