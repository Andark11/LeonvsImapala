"""
Módulo de generalización de conocimiento.
Abstrae patrones para hacer más eficiente el aprendizaje.
"""

from typing import List, Set, Dict
from knowledge.base_conocimientos import Estado, BaseConocimientos


class Generalizador:
    """
    Generaliza conocimiento para reducir el espacio de búsqueda.
    Crea abstracciones de estados similares.
    """
    
    def __init__(self):
        """Inicializa el generalizador"""
        # Reglas de generalización aprendidas
        self.reglas_generalizacion: List[Dict] = []
    
    def generalizar_accion_impala(self, accion: str) -> str:
        """
        Generaliza la acción del impala en categorías más amplias.
        
        Args:
            accion: Acción específica del impala
            
        Returns:
            Categoría generalizada
        """
        # Mapeo de acciones específicas a categorías generales
        mapeo = {
            'ver_izquierda': 'mirando_lado',
            'ver_derecha': 'mirando_lado',
            'ver_frente': 'mirando_frente',
            'beber_agua': 'bebiendo',
            'huir': 'huyendo'
        }
        
        return mapeo.get(accion, accion)
    
    def generalizar_distancia(self, distancia: float) -> str:
        """
        Generaliza la distancia en categorías discretas.
        
        Args:
            distancia: Distancia exacta en cuadros
            
        Returns:
            Categoría de distancia
        """
        if distancia < 2:
            return "muy_cerca"
        elif distancia < 3:
            return "cerca"
        elif distancia < 4:
            return "media"
        else:
            return "lejos"
    
    def crear_estado_generalizado(self, estado: Estado) -> dict:
        """
        Crea una versión generalizada de un estado.
        
        Args:
            estado: Estado específico
            
        Returns:
            Diccionario con versión generalizada
        """
        return {
            'posicion_zona': self._generalizar_posicion(estado.posicion_leon),
            'distancia_categoria': self.generalizar_distancia(estado.distancia_impala),
            'impala_accion_general': self.generalizar_accion_impala(estado.accion_impala),
            'leon_escondido': estado.leon_escondido,
            'impala_puede_ver': estado.impala_puede_ver
        }
    
    def _generalizar_posicion(self, posicion: int) -> str:
        """
        Generaliza la posición del león en zonas.
        
        Args:
            posicion: Posición específica (1-8)
            
        Returns:
            Zona generalizada
        """
        # Agrupar posiciones en zonas
        # Posiciones 1, 8: Norte
        # Posiciones 2, 3: Este
        # Posiciones 4, 5: Sur
        # Posiciones 6, 7: Oeste
        
        zonas = {
            1: 'norte', 8: 'norte',
            2: 'este', 3: 'este',
            4: 'sur', 5: 'sur',
            6: 'oeste', 7: 'oeste'
        }
        
        return zonas.get(posicion, 'desconocida')
    
    def encontrar_estados_similares(self, estado: Estado, 
                                   base_conocimientos: BaseConocimientos) -> List[Estado]:
        """
        Encuentra estados similares en la base de conocimientos.
        
        Args:
            estado: Estado de referencia
            base_conocimientos: Base de conocimientos donde buscar
            
        Returns:
            Lista de estados similares
        """
        estado_gen = self.crear_estado_generalizado(estado)
        estados_similares = []
        
        for estado_conocido in base_conocimientos.obtener_estados_conocidos():
            estado_conocido_gen = self.crear_estado_generalizado(estado_conocido)
            
            # Comparar versiones generalizadas
            if self._son_similares(estado_gen, estado_conocido_gen):
                estados_similares.append(estado_conocido)
        
        return estados_similares
    
    def _son_similares(self, estado_gen1: dict, estado_gen2: dict) -> bool:
        """
        Verifica si dos estados generalizados son similares.
        
        Args:
            estado_gen1: Primer estado generalizado
            estado_gen2: Segundo estado generalizado
            
        Returns:
            True si son similares
        """
        # Criterios de similitud
        misma_zona = estado_gen1['posicion_zona'] == estado_gen2['posicion_zona']
        misma_distancia = estado_gen1['distancia_categoria'] == estado_gen2['distancia_categoria']
        misma_accion_impala = estado_gen1['impala_accion_general'] == estado_gen2['impala_accion_general']
        
        # Considerar similares si al menos 2 de 3 criterios coinciden
        coincidencias = sum([misma_zona, misma_distancia, misma_accion_impala])
        return coincidencias >= 2
    
    def propagar_conocimiento(self, estado_origen: Estado, accion: str,
                             valor_q: float, base_conocimientos: BaseConocimientos,
                             factor_propagacion: float = 0.5):
        """
        Propaga conocimiento a estados similares.
        
        Args:
            estado_origen: Estado que tiene conocimiento
            accion: Acción con valor Q conocido
            valor_q: Valor Q del par (estado, acción)
            base_conocimientos: Base de conocimientos a actualizar
            factor_propagacion: Factor de reducción al propagar (0-1)
        """
        estados_similares = self.encontrar_estados_similares(estado_origen, base_conocimientos)
        
        for estado_similar in estados_similares:
            # Solo propagar si el estado similar no tiene conocimiento previo
            # o si el nuevo conocimiento es mejor
            valor_actual = base_conocimientos.obtener_valor_q(estado_similar, accion)
            nuevo_valor = valor_q * factor_propagacion
            
            if valor_actual == 0.0 or nuevo_valor > valor_actual:
                base_conocimientos.actualizar_valor_q(estado_similar, accion, nuevo_valor)
    
    def extraer_patron(self, estados: List[Estado]) -> dict:
        """
        Extrae un patrón común de una lista de estados.
        
        Args:
            estados: Lista de estados a analizar
            
        Returns:
            Diccionario con el patrón común
        """
        if not estados:
            return {}
        
        # Generalizar todos los estados
        estados_gen = [self.crear_estado_generalizado(e) for e in estados]
        
        # Encontrar elementos comunes
        patron = {}
        for key in estados_gen[0].keys():
            valores = [e[key] for e in estados_gen]
            # Si todos los valores son iguales, es parte del patrón
            if len(set(valores)) == 1:
                patron[key] = valores[0]
        
        return patron
    
    def crear_regla_generalizacion(self, patron: dict, accion_recomendada: str,
                                   efectividad: float):
        """
        Crea una regla de generalización basada en un patrón.
        
        Args:
            patron: Patrón identificado
            accion_recomendada: Acción que funciona para este patrón
            efectividad: Qué tan efectiva es esta regla (0-1)
        """
        regla = {
            'patron': patron,
            'accion': accion_recomendada,
            'efectividad': efectividad
        }
        
        self.reglas_generalizacion.append(regla)
    
    def obtener_recomendacion_por_regla(self, estado: Estado) -> List[tuple]:
        """
        Obtiene recomendaciones basadas en reglas de generalización.
        
        Args:
            estado: Estado actual
            
        Returns:
            Lista de tuplas (accion, efectividad) ordenadas por efectividad
        """
        estado_gen = self.crear_estado_generalizado(estado)
        recomendaciones = []
        
        for regla in self.reglas_generalizacion:
            # Verificar si el estado coincide con el patrón
            coincide = all(
                estado_gen.get(key) == valor
                for key, valor in regla['patron'].items()
            )
            
            if coincide:
                recomendaciones.append((regla['accion'], regla['efectividad']))
        
        # Ordenar por efectividad
        recomendaciones.sort(key=lambda x: x[1], reverse=True)
        return recomendaciones
    
    def generar_reporte(self) -> str:
        """
        Genera un reporte de las reglas de generalización.
        
        Returns:
            String con el reporte
        """
        lineas = [
            "=" * 60,
            "REGLAS DE GENERALIZACIÓN",
            "=" * 60,
            f"Total de reglas: {len(self.reglas_generalizacion)}",
            ""
        ]
        
        for i, regla in enumerate(self.reglas_generalizacion, 1):
            lineas.append(f"Regla {i}:")
            lineas.append(f"  Patrón: {regla['patron']}")
            lineas.append(f"  Acción recomendada: {regla['accion']}")
            lineas.append(f"  Efectividad: {regla['efectividad']:.2%}")
            lineas.append("")
        
        return "\n".join(lineas)
    
    def __len__(self) -> int:
        """Retorna el número de reglas de generalización"""
        return len(self.reglas_generalizacion)
    
    def __str__(self) -> str:
        """Representación en string"""
        return f"Generalizador(Reglas={len(self.reglas_generalizacion)})"


if __name__ == "__main__":
    # Pruebas básicas
    from knowledge.base_conocimientos import Estado, BaseConocimientos
    
    print("=== Pruebas del Generalizador ===\n")
    
    generalizador = Generalizador()
    
    # Crear estados de prueba
    estado1 = Estado(1, 5.0, "ver_izquierda", False, True)
    estado2 = Estado(1, 4.5, "ver_derecha", False, True)
    estado3 = Estado(2, 5.0, "ver_frente", False, True)
    
    # Generalizar estados
    print("Estados generalizados:")
    for i, estado in enumerate([estado1, estado2, estado3], 1):
        gen = generalizador.crear_estado_generalizado(estado)
        print(f"  Estado {i}: {gen}")
    
    # Encontrar estados similares
    bc = BaseConocimientos()
    bc.actualizar_valor_q(estado1, "avanzar", 10.0)
    bc.actualizar_valor_q(estado2, "esconderse", 8.0)
    bc.actualizar_valor_q(estado3, "avanzar", 5.0)
    
    print(f"\nEstados similares a estado1:")
    similares = generalizador.encontrar_estados_similares(estado1, bc)
    print(f"  Encontrados: {len(similares)}")
    
    # Crear regla
    patron = generalizador.extraer_patron([estado1, estado2])
    print(f"\nPatrón extraído de estado1 y estado2:")
    print(f"  {patron}")
    
    generalizador.crear_regla_generalizacion(patron, "avanzar", 0.85)
    print(f"\n{generalizador}")
    print(generalizador.generar_reporte())
