"""
Módulo de verificación de condiciones.
Verifica condiciones de huida, éxito y fracaso.
"""

from enum import Enum
from typing import Tuple
from environment import Abrevadero
from agents.leon import Leon
from agents.impala import Impala, AccionImpala


class CondicionHuida(Enum):
    """Condiciones que provocan la huida del impala"""
    LEON_VISIBLE = "leon_visible_en_angulo_vision"
    LEON_ATACA = "leon_inicia_ataque"
    DISTANCIA_MINIMA = "distancia_menor_a_tres_cuadros"
    NO_HUYE = "no_se_cumplen_condiciones"


class Verificador:
    """
    Verifica las condiciones del mundo durante la simulación.
    """
    
    def __init__(self, abrevadero: Abrevadero):
        """
        Inicializa el verificador.
        
        Args:
            abrevadero: Instancia del abrevadero para cálculos
        """
        self.abrevadero = abrevadero
    
    def verificar_condicion_huida(self, leon: Leon, impala: Impala,
                                  accion_impala: AccionImpala) -> Tuple[bool, CondicionHuida]:
        """
        Verifica si se cumplen las condiciones para que el impala huya.
        
        Args:
            leon: Instancia del león
            impala: Instancia del impala
            accion_impala: Última acción ejecutada por el impala
            
        Returns:
            Tupla (debe_huir, condicion)
        """
        # Si ya está huyendo, no necesita verificación
        if impala.esta_huyendo:
            return True, CondicionHuida.NO_HUYE
        
        # Condición 1: León inicia ataque
        if leon.esta_atacando:
            return True, CondicionHuida.LEON_ATACA
        
        # Condición 2: Distancia menor a 3 cuadros
        distancia = self.abrevadero.distancia_leon_impala(leon.posicion)
        if distancia < self.abrevadero.DISTANCIA_MINIMA_HUIDA:
            return True, CondicionHuida.DISTANCIA_MINIMA
        
        # Condición 3: Impala ve al león
        # (solo si no está bebiendo y el león es visible)
        if accion_impala != AccionImpala.BEBER_AGUA and leon.es_visible():
            if self.abrevadero.leon_en_angulo_vision(leon.posicion, impala.direccion_vista):
                return True, CondicionHuida.LEON_VISIBLE
        
        return False, CondicionHuida.NO_HUYE
    
    def verificar_exito_caceria(self, leon: Leon, impala: Impala) -> bool:
        """
        Verifica si el león alcanzó al impala exitosamente.
        
        Args:
            leon: Instancia del león
            impala: Instancia del impala
            
        Returns:
            True si el león alcanzó al impala
        """
        if not leon.esta_atacando:
            return False
        
        # Calcular distancia actual
        distancia = self.abrevadero.distancia_leon_impala(leon.posicion)
        
        # El león alcanza al impala si la distancia es <= 0.5 cuadros
        return distancia <= 0.5
    
    def verificar_fracaso_caceria(self, leon: Leon, impala: Impala) -> bool:
        """
        Verifica si la cacería ha fracasado (león no puede alcanzar).
        
        Args:
            leon: Instancia del león
            impala: Instancia del impala
            
        Returns:
            True si la cacería ha fracasado
        """
        if not impala.esta_huyendo:
            return False
        
        # Calcular si el león puede alcanzar al impala
        # El impala acelera: 1, 2, 3, 4... cuadros/T
        # El león ataca a velocidad constante: 2 cuadros/T
        
        # Si la velocidad del impala supera la del león, no podrá alcanzarlo
        if impala.velocidad_huida > leon.VELOCIDAD_ATAQUE:
            return True
        
        return False
    
    def calcular_distancia_actual(self, leon: Leon) -> float:
        """
        Calcula la distancia actual entre el león y el impala.
        
        Args:
            leon: Instancia del león
            
        Returns:
            Distancia en cuadros
        """
        if leon.posicion_exacta:
            return self.abrevadero.calcular_distancia(
                leon.posicion_exacta, 
                self.abrevadero.CENTRO
            )
        else:
            return self.abrevadero.distancia_leon_impala(leon.posicion)
    
    def impala_puede_ver_leon(self, leon: Leon, impala: Impala,
                              accion_impala: AccionImpala) -> bool:
        """
        Determina si el impala puede ver al león en su estado actual.
        
        Args:
            leon: Instancia del león
            impala: Instancia del impala
            accion_impala: Acción actual del impala
            
        Returns:
            True si el impala puede ver al león
        """
        # Si está bebiendo, no puede ver
        if accion_impala == AccionImpala.BEBER_AGUA:
            return False
        
        # Si el león está escondido, no puede verlo
        if not leon.es_visible():
            return False
        
        # Verificar ángulo de visión
        return self.abrevadero.leon_en_angulo_vision(leon.posicion, impala.direccion_vista)
    
    def obtener_estado_mundo(self, leon: Leon, impala: Impala) -> dict:
        """
        Obtiene un snapshot del estado actual del mundo.
        
        Args:
            leon: Instancia del león
            impala: Instancia del impala
            
        Returns:
            Diccionario con el estado del mundo
        """
        distancia = self.calcular_distancia_actual(leon)
        
        return {
            'posicion_leon': leon.posicion,
            'posicion_exacta_leon': leon.posicion_exacta,
            'leon_escondido': leon.esta_escondido,
            'leon_atacando': leon.esta_atacando,
            'direccion_impala': impala.direccion_vista.name,
            'impala_huyendo': impala.esta_huyendo,
            'velocidad_huida_impala': impala.velocidad_huida,
            'distancia_leon_impala': round(distancia, 2),
        }


if __name__ == "__main__":
    # Pruebas básicas
    from agents.leon import Leon, AccionLeon
    from agents.impala import Impala, AccionImpala
    from environment import Abrevadero, Direccion
    
    print("=== Pruebas del Verificador ===\n")
    
    abrevadero = Abrevadero()
    verificador = Verificador(abrevadero)
    leon = Leon(posicion_inicial=1)
    impala = Impala(Direccion.NORTE)
    
    # Prueba 1: León visible en ángulo de visión
    print("Prueba 1: León en posición 1, impala mirando al norte")
    debe_huir, condicion = verificador.verificar_condicion_huida(
        leon, impala, AccionImpala.VER_FRENTE
    )
    print(f"  ¿Debe huir? {debe_huir}")
    print(f"  Condición: {condicion.value}\n")
    
    # Prueba 2: León escondido
    print("Prueba 2: León escondido en posición 1")
    leon.ejecutar_accion(AccionLeon.ESCONDERSE)
    debe_huir, condicion = verificador.verificar_condicion_huida(
        leon, impala, AccionImpala.VER_FRENTE
    )
    print(f"  ¿Debe huir? {debe_huir}")
    print(f"  Condición: {condicion.value}\n")
    
    # Prueba 3: León ataca
    print("Prueba 3: León inicia ataque")
    leon.resetear()
    leon.ejecutar_accion(AccionLeon.ATACAR)
    debe_huir, condicion = verificador.verificar_condicion_huida(
        leon, impala, AccionImpala.BEBER_AGUA
    )
    print(f"  ¿Debe huir? {debe_huir}")
    print(f"  Condición: {condicion.value}\n")
    
    # Prueba 4: Estado del mundo
    print("Prueba 4: Estado del mundo")
    leon.resetear()
    estado = verificador.obtener_estado_mundo(leon, impala)
    for clave, valor in estado.items():
        print(f"  {clave}: {valor}")
