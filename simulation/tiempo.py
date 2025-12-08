"""
Módulo de gestión del tiempo de simulación.
Maneja las unidades de tiempo T.
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class EventoTiempo:
    """Representa un evento que ocurre en una unidad de tiempo"""
    tiempo: int
    accion_impala: str
    accion_leon: str
    resultado: str
    estado_mundo: dict


class TiempoSimulacion:
    """
    Gestiona el tiempo de la simulación.
    Registra eventos que ocurren en cada unidad de tiempo T.
    """
    
    def __init__(self):
        """Inicializa el gestor de tiempo"""
        self.tiempo_actual = 0
        self.historia: List[EventoTiempo] = []
    
    def resetear(self):
        """Resetea el tiempo a T=0 y limpia la historia"""
        self.tiempo_actual = 0
        self.historia.clear()
    
    def avanzar_tiempo(self) -> int:
        """
        Avanza una unidad de tiempo.
        
        Returns:
            Nuevo valor del tiempo actual
        """
        self.tiempo_actual += 1
        return self.tiempo_actual
    
    def registrar_evento(self, accion_impala: str, accion_leon: str,
                        resultado: str, estado_mundo: dict):
        """
        Registra un evento en el tiempo actual.
        
        Args:
            accion_impala: Descripción de la acción del impala
            accion_leon: Descripción de la acción del león
            resultado: Resultado de las acciones
            estado_mundo: Estado del mundo después de las acciones
        """
        evento = EventoTiempo(
            tiempo=self.tiempo_actual,
            accion_impala=accion_impala,
            accion_leon=accion_leon,
            resultado=resultado,
            estado_mundo=estado_mundo.copy()
        )
        self.historia.append(evento)
    
    def obtener_tiempo_actual(self) -> int:
        """
        Obtiene el tiempo actual.
        
        Returns:
            Tiempo actual (número de unidades de tiempo transcurridas)
        """
        return self.tiempo_actual
    
    def obtener_historia(self) -> List[EventoTiempo]:
        """
        Obtiene la historia completa de eventos.
        
        Returns:
            Lista de eventos registrados
        """
        return self.historia.copy()
    
    def obtener_ultimo_evento(self) -> Optional[EventoTiempo]:
        """
        Obtiene el último evento registrado.
        
        Returns:
            Último evento o None si no hay eventos
        """
        return self.historia[-1] if self.historia else None
    
    def obtener_evento(self, tiempo: int) -> EventoTiempo:
        """
        Obtiene el evento de una unidad de tiempo específica.
        
        Args:
            tiempo: Número de tiempo a consultar
            
        Returns:
            Evento correspondiente
            
        Raises:
            IndexError: Si el tiempo especificado no existe
        """
        if tiempo < 1 or tiempo > len(self.historia):
            raise IndexError(f"No existe evento para T={tiempo}")
        
        return self.historia[tiempo - 1]
    
    def obtener_ultimos_eventos(self, n: int) -> List[EventoTiempo]:
        """
        Obtiene los últimos N eventos.
        
        Args:
            n: Número de eventos a obtener
            
        Returns:
            Lista con los últimos N eventos
        """
        return self.historia[-n:] if n > 0 else []
    
    def generar_resumen(self) -> str:
        """
        Genera un resumen textual de toda la simulación.
        
        Returns:
            String con el resumen de todos los eventos
        """
        if not self.historia:
            return "No hay eventos registrados"
        
        lineas = [f"=== Resumen de Cacería ({len(self.historia)} unidades de tiempo) ===\n"]
        
        for evento in self.historia:
            lineas.append(f"T={evento.tiempo}:")
            lineas.append(f"  Impala: {evento.accion_impala}")
            lineas.append(f"  León: {evento.accion_leon}")
            lineas.append(f"  Resultado: {evento.resultado}")
            lineas.append(f"  Distancia: {evento.estado_mundo.get('distancia_leon_impala', '?')} cuadros")
            lineas.append("")
        
        return "\n".join(lineas)
    
    def generar_resumen_compacto(self) -> List[Tuple[int, str, str]]:
        """
        Genera un resumen compacto de la simulación.
        
        Returns:
            Lista de tuplas (tiempo, accion_impala, accion_leon)
        """
        return [
            (e.tiempo, e.accion_impala, e.accion_leon)
            for e in self.historia
        ]
    
    def __len__(self) -> int:
        """Retorna el número de eventos registrados"""
        return len(self.historia)
    
    def __str__(self) -> str:
        """Representación en string del tiempo"""
        return f"TiempoSimulacion(T={self.tiempo_actual}, Eventos={len(self.historia)})"


if __name__ == "__main__":
    # Pruebas básicas
    print("=== Pruebas de TiempoSimulacion ===\n")
    
    tiempo = TiempoSimulacion()
    print(f"Estado inicial: {tiempo}\n")
    
    # Simular algunos eventos
    print("Simulando eventos...")
    for i in range(5):
        tiempo.avanzar_tiempo()
        tiempo.registrar_evento(
            accion_impala=f"Ver frente",
            accion_leon=f"Avanzar" if i < 3 else "Atacar",
            resultado="León avanza sin ser detectado" if i < 3 else "León inicia ataque",
            estado_mundo={
                'distancia_leon_impala': 5 - i,
                'leon_escondido': False,
                'impala_huyendo': False
            }
        )
    
    print(f"\nEstado final: {tiempo}\n")
    
    # Mostrar resumen
    print(tiempo.generar_resumen())
    
    # Mostrar evento específico
    print("--- Evento T=3 ---")
    evento = tiempo.obtener_evento(3)
    print(f"Acción impala: {evento.accion_impala}")
    print(f"Acción león: {evento.accion_leon}")
    print(f"Distancia: {evento.estado_mundo['distancia_leon_impala']}")
