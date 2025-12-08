"""
Módulo de gestión del entorno del abrevadero.
Maneja el mapa, posiciones, distancias y línea de visión.
"""

import math
from typing import Tuple, Dict
from enum import Enum


class Direccion(Enum):
    """Direcciones cardinales para la orientación del impala"""
    NORTE = 0
    NORESTE = 45
    ESTE = 90
    SURESTE = 135
    SUR = 180
    SUROESTE = 225
    OESTE = 270
    NOROESTE = 315


class Abrevadero:
    """
    Representa el abrevadero con 8 posiciones alrededor y el centro.
    
    Configuración del mapa:
         8    1    2
         7    I    3
         6    5    4
    """
    
    # Radio del círculo de posiciones (en cuadros)
    RADIO = 9.5  # Ajustado para coincidir con grid 19×19
    
    # Posición central del impala
    CENTRO = (0, 0)
    
    # Ángulo de visión del impala (en grados)
    ANGULO_VISION = 120  # 60 grados a cada lado
    
    # Distancia mínima para que el impala huya
    DISTANCIA_MINIMA_HUIDA = 3
    
    def __init__(self):
        """Inicializa el abrevadero con las 8 posiciones predefinidas"""
        self.posiciones = self._calcular_posiciones()
    
    def _calcular_posiciones(self) -> Dict[int, Tuple[float, float]]:
        """
        Calcula las coordenadas cartesianas de las 8 posiciones.
        
        Returns:
            Dict con posición (1-8) como clave y (x, y) como valor
        """
        posiciones = {}
        
        # Ángulos para cada posición (en grados, empezando desde el norte)
        # Posición 1: 0° (norte)
        # Posición 2: 45° (noreste)
        # etc.
        angulos = {
            1: 0,      # Norte
            2: 45,     # Noreste
            3: 90,     # Este
            4: 135,    # Sureste
            5: 180,    # Sur
            6: 225,    # Suroeste
            7: 270,    # Oeste
            8: 315     # Noroeste
        }
        
        for pos, angulo in angulos.items():
            radianes = math.radians(angulo)
            x = self.RADIO * math.sin(radianes)
            y = self.RADIO * math.cos(radianes)
            posiciones[pos] = (round(x, 2), round(y, 2))
        
        return posiciones
    
    def obtener_coordenadas(self, posicion: int) -> Tuple[float, float]:
        """
        Obtiene las coordenadas de una posición específica.
        
        Args:
            posicion: Número de posición (1-8)
            
        Returns:
            Tupla (x, y) con las coordenadas
        """
        if posicion not in range(1, 9):
            raise ValueError(f"Posición debe estar entre 1 y 8, recibido: {posicion}")
        return self.posiciones[posicion]
    
    def calcular_distancia(self, pos1: Tuple[float, float], 
                          pos2: Tuple[float, float]) -> float:
        """
        Calcula la distancia euclidiana entre dos posiciones.
        
        Args:
            pos1: Coordenadas (x, y) del primer punto
            pos2: Coordenadas (x, y) del segundo punto
            
        Returns:
            Distancia en cuadros
        """
        x1, y1 = pos1
        x2, y2 = pos2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def distancia_leon_impala(self, posicion_leon: int) -> float:
        """
        Calcula la distancia entre el león y el impala.
        
        Args:
            posicion_leon: Posición actual del león (1-8)
            
        Returns:
            Distancia en cuadros
        """
        coord_leon = self.obtener_coordenadas(posicion_leon)
        return self.calcular_distancia(coord_leon, self.CENTRO)
    
    def calcular_angulo(self, desde: Tuple[float, float], 
                       hacia: Tuple[float, float]) -> float:
        """
        Calcula el ángulo desde un punto hacia otro (en grados, 0° = Norte).
        
        Args:
            desde: Coordenadas (x, y) del punto origen
            hacia: Coordenadas (x, y) del punto destino
            
        Returns:
            Ángulo en grados (0-360)
        """
        x1, y1 = desde
        x2, y2 = hacia
        
        # Calcular ángulo en radianes
        radianes = math.atan2(x2 - x1, y2 - y1)
        
        # Convertir a grados y normalizar (0-360)
        angulo = math.degrees(radianes)
        if angulo < 0:
            angulo += 360
            
        return angulo
    
    def leon_en_angulo_vision(self, posicion_leon: int, 
                              direccion_impala: Direccion) -> bool:
        """
        Verifica si el león está dentro del ángulo de visión del impala.
        
        Args:
            posicion_leon: Posición actual del león (1-8)
            direccion_impala: Dirección hacia donde mira el impala
            
        Returns:
            True si el león está visible, False en caso contrario
        """
        coord_leon = self.obtener_coordenadas(posicion_leon)
        
        # Ángulo desde el impala hacia el león
        angulo_leon = self.calcular_angulo(self.CENTRO, coord_leon)
        
        # Dirección del impala en grados
        dir_impala = direccion_impala.value
        
        # Calcular diferencia angular
        diff = abs(angulo_leon - dir_impala)
        if diff > 180:
            diff = 360 - diff
        
        # Verificar si está dentro del ángulo de visión
        return diff <= (self.ANGULO_VISION / 2)
    
    def calcular_nueva_posicion_avance(self, posicion_actual: int, 
                                       hacia_impala: bool = True) -> Tuple[float, float]:
        """
        Calcula la nueva posición cuando el león avanza 1 cuadro.
        
        Args:
            posicion_actual: Posición actual del león (1-8)
            hacia_impala: Si avanza hacia el impala (True) o se aleja (False)
            
        Returns:
            Nueva coordenada (x, y)
        """
        coord_actual = self.obtener_coordenadas(posicion_actual)
        
        # Vector unitario desde el león hacia el impala (o viceversa)
        x, y = coord_actual
        distancia = self.calcular_distancia(coord_actual, self.CENTRO)
        
        if distancia == 0:
            return coord_actual
        
        # Normalizar y avanzar 1 cuadro
        factor = 1 if hacia_impala else -1
        dx = -x / distancia * factor
        dy = -y / distancia * factor
        
        nueva_x = x + dx
        nueva_y = y + dy
        
        return (round(nueva_x, 2), round(nueva_y, 2))
    
    def __str__(self) -> str:
        """Representación en string del abrevadero"""
        return f"Abrevadero(Radio={self.RADIO}, Posiciones={len(self.posiciones)})"


if __name__ == "__main__":
    # Pruebas básicas
    abrevadero = Abrevadero()
    
    print("=== Pruebas del Abrevadero ===\n")
    
    print("Posiciones del mapa:")
    for pos in range(1, 9):
        coord = abrevadero.obtener_coordenadas(pos)
        dist = abrevadero.distancia_leon_impala(pos)
        print(f"  Posición {pos}: {coord}, Distancia al centro: {dist:.2f}")
    
    print("\n¿León visible desde impala mirando al norte?")
    for pos in range(1, 9):
        visible = abrevadero.leon_en_angulo_vision(pos, Direccion.NORTE)
        print(f"  Posición {pos}: {'Sí' if visible else 'No'}")
