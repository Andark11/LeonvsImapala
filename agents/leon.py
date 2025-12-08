"""
Módulo del agente León.
Define el comportamiento y acciones del león.
"""

from enum import Enum
from typing import Tuple, Optional


class AccionLeon(Enum):
    """Acciones posibles del león"""
    AVANZAR = "avanzar"
    ESCONDERSE = "esconderse"
    ATACAR = "atacar"
    SITUARSE = "situarse"


class Leon:
    """
    Representa al león cazador.
    
    Attributes:
        posicion: Posición actual del león (1-8)
        esta_escondido: Indica si el león está escondido
        esta_atacando: Indica si el león está en modo de ataque
        posicion_exacta: Coordenadas exactas (x, y) cuando avanza
        velocidad_ataque: Velocidad constante durante el ataque (2 cuadros/T)
    """
    
    VELOCIDAD_AVANCE = 1  # cuadros por unidad de tiempo
    VELOCIDAD_ATAQUE = 2  # cuadros por unidad de tiempo
    
    def __init__(self, posicion_inicial: int = 1):
        """
        Inicializa el león.
        
        Args:
            posicion_inicial: Posición inicial del león (1-8)
        """
        if posicion_inicial not in range(1, 9):
            raise ValueError(f"Posición inicial debe estar entre 1 y 8, recibido: {posicion_inicial}")
        
        self.posicion = posicion_inicial
        self.esta_escondido = False
        self.esta_atacando = False
        self.posicion_exacta: Optional[Tuple[float, float]] = None
        self.velocidad_ataque = self.VELOCIDAD_ATAQUE
    
    def resetear(self, nueva_posicion: Optional[int] = None):
        """
        Resetea el estado del león.
        
        Args:
            nueva_posicion: Nueva posición inicial (si es None, mantiene la actual)
        """
        if nueva_posicion is not None:
            if nueva_posicion not in range(1, 9):
                raise ValueError(f"Posición debe estar entre 1 y 8, recibido: {nueva_posicion}")
            self.posicion = nueva_posicion
        
        self.esta_escondido = False
        self.esta_atacando = False
        self.posicion_exacta = None
    
    def ejecutar_accion(self, accion: AccionLeon, 
                       parametro: Optional[any] = None) -> str:
        """
        Ejecuta una acción del león.
        
        Args:
            accion: Acción a ejecutar
            parametro: Parámetro adicional (ej: nueva posición para SITUARSE)
            
        Returns:
            Descripción de lo que ocurrió
        """
        if self.esta_atacando:
            return self._continuar_ataque()
        
        if accion == AccionLeon.AVANZAR:
            return self._avanzar()
        elif accion == AccionLeon.ESCONDERSE:
            return self._esconderse()
        elif accion == AccionLeon.ATACAR:
            return self._iniciar_ataque()
        elif accion == AccionLeon.SITUARSE:
            if parametro is None:
                raise ValueError("SITUARSE requiere una posición como parámetro")
            return self._situarse(parametro)
        else:
            raise ValueError(f"Acción desconocida: {accion}")
    
    def _avanzar(self) -> str:
        """
        Avanza 1 cuadro en línea recta hacia el impala.
        Si estaba escondido, sale de su escondite.
        """
        estaba_escondido = self.esta_escondido
        self.esta_escondido = False
        
        mensaje = f"León avanza {self.VELOCIDAD_AVANCE} cuadro hacia el impala"
        if estaba_escondido:
            mensaje += " (sale de su escondite)"
        
        return mensaje
    
    def _esconderse(self) -> str:
        """
        Se esconde entre la maleza.
        El impala no puede verlo mientras esté escondido.
        """
        if self.esta_escondido:
            return "León permanece escondido entre la maleza"
        
        self.esta_escondido = True
        return "León se esconde entre la maleza (ahora es invisible para el impala)"
    
    def _iniciar_ataque(self) -> str:
        """
        Inicia el ataque al impala.
        Una vez iniciado el ataque, no puede realizar otras acciones.
        """
        self.esta_atacando = True
        self.esta_escondido = False
        
        return f"¡LEÓN INICIA ATAQUE! (Velocidad: {self.VELOCIDAD_ATAQUE} cuadros/T)"
    
    def _continuar_ataque(self) -> str:
        """Continúa el ataque a velocidad constante"""
        return f"León continúa su ataque (Velocidad: {self.VELOCIDAD_ATAQUE} cuadros/T)"
    
    def _situarse(self, nueva_posicion: int) -> str:
        """
        Se sitúa en una nueva posición.
        Solo se usa al inicio de una incursión.
        
        Args:
            nueva_posicion: Nueva posición (1-8)
            
        Returns:
            Descripción del movimiento
        """
        if nueva_posicion not in range(1, 9):
            raise ValueError(f"Posición debe estar entre 1 y 8, recibido: {nueva_posicion}")
        
        posicion_anterior = self.posicion
        self.posicion = nueva_posicion
        self.esta_escondido = False
        self.esta_atacando = False
        self.posicion_exacta = None
        
        return f"León se sitúa en la posición {nueva_posicion} (antes estaba en {posicion_anterior})"
    
    def es_visible(self) -> bool:
        """
        Verifica si el león es visible para el impala.
        
        Returns:
            True si es visible, False si está escondido
        """
        return not self.esta_escondido
    
    def puede_actuar(self) -> bool:
        """
        Verifica si el león puede realizar acciones.
        
        Returns:
            False si está atacando (no puede cambiar de acción), True en caso contrario
        """
        return not self.esta_atacando
    
    def actualizar_posicion_exacta(self, nueva_posicion: Tuple[float, float]):
        """
        Actualiza la posición exacta del león cuando avanza o ataca.
        
        Args:
            nueva_posicion: Coordenadas exactas (x, y)
        """
        self.posicion_exacta = nueva_posicion
    
    def obtener_posicion_exacta(self) -> Optional[Tuple[float, float]]:
        """
        Obtiene la posición exacta del león.
        
        Returns:
            Coordenadas (x, y) si se han actualizado, None en caso contrario
        """
        return self.posicion_exacta
    
    def __str__(self) -> str:
        """Representación en string del león"""
        estado_partes = [f"Posición={self.posicion}"]
        
        if self.esta_escondido:
            estado_partes.append("ESCONDIDO")
        if self.esta_atacando:
            estado_partes.append("ATACANDO")
        
        estado = ", ".join(estado_partes)
        return f"Leon({estado})"


if __name__ == "__main__":
    # Pruebas básicas
    print("=== Pruebas del León ===\n")
    
    leon = Leon(posicion_inicial=3)
    print(f"Estado inicial: {leon}\n")
    
    # Probar acciones
    print("--- Secuencia de acciones ---")
    acciones = [
        (AccionLeon.ESCONDERSE, None, "Esconderse"),
        (AccionLeon.AVANZAR, None, "Avanzar (saliendo del escondite)"),
        (AccionLeon.AVANZAR, None, "Avanzar de nuevo"),
        (AccionLeon.ESCONDERSE, None, "Volver a esconderse"),
        (AccionLeon.ATACAR, None, "Iniciar ataque"),
    ]
    
    for accion, param, descripcion in acciones:
        resultado = leon.ejecutar_accion(accion, param)
        print(f"{descripcion}:")
        print(f"  {resultado}")
        print(f"  Estado: {leon}")
        print()
    
    # Verificar que no puede hacer otras acciones mientras ataca
    print("--- Intentar avanzar mientras ataca ---")
    resultado = leon.ejecutar_accion(AccionLeon.AVANZAR)
    print(f"  {resultado}")
    print(f"  Estado: {leon}")
