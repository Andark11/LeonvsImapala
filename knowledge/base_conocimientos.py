"""
Módulo de base de conocimientos.
Almacena y gestiona el conocimiento adquirido por el león.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict
import json


@dataclass
class Estado:
    """
    Representa un estado del mundo desde la perspectiva del león.
    
    Attributes:
        posicion_leon: Posición del león (1-8)
        distancia_impala: Distancia al impala (redondeada)
        accion_impala: Qué está haciendo el impala
        leon_escondido: Si el león está escondido
        impala_puede_ver: Si el impala puede ver al león
    """
    posicion_leon: int
    distancia_impala: float  # Redondeada a 0.5 cuadros
    accion_impala: str
    leon_escondido: bool
    impala_puede_ver: bool
    
    def __hash__(self):
        """Permite usar Estado como key en diccionarios"""
        return hash((
            self.posicion_leon,
            self.distancia_impala,
            self.accion_impala,
            self.leon_escondido,
            self.impala_puede_ver
        ))
    
    def to_dict(self) -> dict:
        """Convierte el estado a diccionario"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Estado':
        """Crea un Estado desde un diccionario"""
        return cls(**data)
    
    def __str__(self) -> str:
        """Representación legible del estado"""
        partes = [
            f"Pos={self.posicion_leon}",
            f"Dist={self.distancia_impala:.1f}",
            f"Impala={self.accion_impala}",
        ]
        if self.leon_escondido:
            partes.append("ESCONDIDO")
        if self.impala_puede_ver:
            partes.append("VISIBLE")
        return f"Estado({', '.join(partes)})"


@dataclass
class Experiencia:
    """
    Representa una experiencia: Estado → Acción → Resultado.
    
    Attributes:
        estado: Estado del mundo
        accion: Acción ejecutada por el león
        recompensa: Recompensa obtenida
        siguiente_estado: Estado resultante (puede ser None si terminó)
        exito: Si la cacería fue exitosa
    """
    estado: Estado
    accion: str
    recompensa: float
    siguiente_estado: Optional[Estado]
    exito: bool
    
    def to_dict(self) -> dict:
        """Convierte la experiencia a diccionario"""
        return {
            'estado': self.estado.to_dict(),
            'accion': self.accion,
            'recompensa': self.recompensa,
            'siguiente_estado': self.siguiente_estado.to_dict() if self.siguiente_estado else None,
            'exito': self.exito
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Experiencia':
        """Crea una Experiencia desde un diccionario"""
        return cls(
            estado=Estado.from_dict(data['estado']),
            accion=data['accion'],
            recompensa=data['recompensa'],
            siguiente_estado=Estado.from_dict(data['siguiente_estado']) if data['siguiente_estado'] else None,
            exito=data['exito']
        )


class BaseConocimientos:
    """
    Base de conocimientos del león.
    Almacena experiencias y permite consultas eficientes.
    """
    
    def __init__(self):
        """Inicializa la base de conocimientos vacía"""
        # Tabla Q: (estado, accion) -> valor Q
        self.q_table: Dict[Tuple[Estado, str], float] = defaultdict(float)
        
        # Contador de visitas: (estado, accion) -> número de veces vista
        self.visitas: Dict[Tuple[Estado, str], int] = defaultdict(int)
        
        # Experiencias almacenadas (para análisis posterior)
        self.experiencias: List[Experiencia] = []
        
        # Estadísticas
        self.total_experiencias = 0
        self.cacerias_exitosas = 0
        self.cacerias_fallidas = 0
    
    def agregar_experiencia(self, experiencia: Experiencia):
        """
        Agrega una nueva experiencia a la base de conocimientos.
        
        Args:
            experiencia: Experiencia a agregar
        """
        self.experiencias.append(experiencia)
        self.total_experiencias += 1
        
        # Actualizar estadísticas
        if experiencia.exito:
            self.cacerias_exitosas += 1
        elif experiencia.siguiente_estado is None:  # Terminó sin éxito
            self.cacerias_fallidas += 1
        
        # Actualizar contador de visitas
        key = (experiencia.estado, experiencia.accion)
        self.visitas[key] += 1
    
    def actualizar_valor_q(self, estado: Estado, accion: str, valor: float):
        """
        Actualiza el valor Q de un par (estado, acción).
        
        Args:
            estado: Estado del mundo
            accion: Acción ejecutada
            valor: Nuevo valor Q
        """
        key = (estado, accion)
        self.q_table[key] = valor
    
    def obtener_valor_q(self, estado: Estado, accion: str) -> float:
        """
        Obtiene el valor Q de un par (estado, acción).
        
        Args:
            estado: Estado del mundo
            accion: Acción a consultar
            
        Returns:
            Valor Q (0.0 si nunca se ha visto)
        """
        key = (estado, accion)
        return self.q_table.get(key, 0.0)
    
    def obtener_mejor_accion(self, estado: Estado, 
                            acciones_posibles: List[str]) -> Tuple[str, float]:
        """
        Obtiene la mejor acción para un estado dado.
        
        Args:
            estado: Estado actual
            acciones_posibles: Lista de acciones válidas
            
        Returns:
            Tupla (mejor_accion, valor_q)
        """
        mejor_accion = None
        mejor_valor = float('-inf')
        
        for accion in acciones_posibles:
            valor = self.obtener_valor_q(estado, accion)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_accion = accion
        
        # Si no hay mejor acción (todos son 0), devolver la primera
        if mejor_accion is None:
            mejor_accion = acciones_posibles[0]
            mejor_valor = 0.0
        
        return mejor_accion, mejor_valor
    
    def obtener_visitas(self, estado: Estado, accion: str) -> int:
        """
        Obtiene el número de veces que se ha visitado un par (estado, acción).
        
        Args:
            estado: Estado del mundo
            accion: Acción a consultar
            
        Returns:
            Número de visitas
        """
        key = (estado, accion)
        return self.visitas.get(key, 0)
    
    def obtener_estados_conocidos(self) -> Set[Estado]:
        """
        Obtiene todos los estados conocidos.
        
        Returns:
            Conjunto de estados únicos
        """
        estados = set()
        for (estado, _) in self.q_table.keys():
            estados.add(estado)
        return estados
    
    def obtener_estadisticas(self) -> dict:
        """
        Obtiene estadísticas de la base de conocimientos.
        
        Returns:
            Diccionario con estadísticas
        """
        total_cacerias = self.cacerias_exitosas + self.cacerias_fallidas
        tasa_exito = (self.cacerias_exitosas / total_cacerias * 100) if total_cacerias > 0 else 0
        
        return {
            'total_experiencias': self.total_experiencias,
            'cacerias_exitosas': self.cacerias_exitosas,
            'cacerias_fallidas': self.cacerias_fallidas,
            'tasa_exito': round(tasa_exito, 2),
            'estados_unicos': len(self.obtener_estados_conocidos()),
            'pares_estado_accion': len(self.q_table)
        }
    
    def limpiar(self):
        """Limpia toda la base de conocimientos"""
        self.q_table.clear()
        self.visitas.clear()
        self.experiencias.clear()
        self.total_experiencias = 0
        self.cacerias_exitosas = 0
        self.cacerias_fallidas = 0
    
    def exportar_a_json(self) -> str:
        """
        Exporta la base de conocimientos a formato JSON.
        
        Returns:
            String JSON con toda la información
        """
        # Convertir q_table a formato serializable
        q_table_list = [
            {
                'estado': estado.to_dict(),
                'accion': accion,
                'valor_q': valor
            }
            for (estado, accion), valor in self.q_table.items()
        ]
        
        # Convertir experiencias
        experiencias_list = [exp.to_dict() for exp in self.experiencias[-1000:]]  # Últimas 1000
        
        data = {
            'q_table': q_table_list,
            'estadisticas': self.obtener_estadisticas(),
            'experiencias_recientes': experiencias_list
        }
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def importar_desde_json(self, json_str: str):
        """
        Importa la base de conocimientos desde JSON.
        
        Args:
            json_str: String JSON con la información
        """
        data = json.loads(json_str)
        
        # Limpiar primero
        self.limpiar()
        
        # Importar q_table
        for item in data['q_table']:
            estado = Estado.from_dict(item['estado'])
            accion = item['accion']
            valor = item['valor_q']
            self.q_table[(estado, accion)] = valor
        
        # Importar estadísticas
        stats = data['estadisticas']
        self.total_experiencias = stats['total_experiencias']
        self.cacerias_exitosas = stats['cacerias_exitosas']
        self.cacerias_fallidas = stats['cacerias_fallidas']
    
    def generar_reporte_legible(self) -> str:
        """
        Genera un reporte legible de la base de conocimientos.
        
        Returns:
            String con el reporte
        """
        lineas = [
            "=" * 70,
            "REPORTE DE BASE DE CONOCIMIENTOS",
            "=" * 70,
            ""
        ]
        
        # Estadísticas
        stats = self.obtener_estadisticas()
        lineas.append("ESTADÍSTICAS:")
        for key, value in stats.items():
            lineas.append(f"  {key}: {value}")
        lineas.append("")
        
        # Top 10 acciones más valiosas
        lineas.append("TOP 10 ACCIONES MÁS VALIOSAS:")
        q_items = sorted(self.q_table.items(), key=lambda x: x[1], reverse=True)[:10]
        for i, ((estado, accion), valor) in enumerate(q_items, 1):
            lineas.append(f"  {i}. {estado}")
            lineas.append(f"     Acción: {accion} | Valor Q: {valor:.2f}")
            lineas.append("")
        
        return "\n".join(lineas)
    
    def __len__(self) -> int:
        """Retorna el número de pares (estado, acción) conocidos"""
        return len(self.q_table)
    
    def __str__(self) -> str:
        """Representación en string"""
        stats = self.obtener_estadisticas()
        return f"BaseConocimientos(Estados={stats['estados_unicos']}, Pares={stats['pares_estado_accion']}, Éxito={stats['tasa_exito']}%)"


if __name__ == "__main__":
    # Pruebas básicas
    print("=== Pruebas de Base de Conocimientos ===\n")
    
    bc = BaseConocimientos()
    
    # Crear algunos estados de ejemplo
    estado1 = Estado(
        posicion_leon=1,
        distancia_impala=5.0,
        accion_impala="ver_frente",
        leon_escondido=False,
        impala_puede_ver=True
    )
    
    estado2 = Estado(
        posicion_leon=1,
        distancia_impala=4.0,
        accion_impala="beber_agua",
        leon_escondido=True,
        impala_puede_ver=False
    )
    
    # Agregar experiencias
    exp1 = Experiencia(estado1, "esconderse", -1.0, estado2, False)
    exp2 = Experiencia(estado2, "avanzar", 5.0, None, True)
    
    bc.agregar_experiencia(exp1)
    bc.agregar_experiencia(exp2)
    
    # Actualizar valores Q
    bc.actualizar_valor_q(estado1, "esconderse", 10.5)
    bc.actualizar_valor_q(estado1, "avanzar", 5.2)
    
    print(f"Base de conocimientos: {bc}\n")
    
    # Obtener mejor acción
    mejor_accion, valor = bc.obtener_mejor_accion(estado1, ["esconderse", "avanzar", "atacar"])
    print(f"Mejor acción para {estado1}:")
    print(f"  Acción: {mejor_accion}, Valor Q: {valor}\n")
    
    # Estadísticas
    print("Estadísticas:")
    for key, value in bc.obtener_estadisticas().items():
        print(f"  {key}: {value}")
