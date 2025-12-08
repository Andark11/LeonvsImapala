"""
Sistema explicador de decisiones del león.
"""

from typing import List, Tuple

from knowledge.base_conocimientos import BaseConocimientos, Estado
from knowledge.generalizacion import Generalizador


class Explicador:
    """
    Explica por qué el león tomó una decisión específica.
    """
    
    def __init__(self, base_conocimientos: BaseConocimientos,
                 generalizador: Generalizador):
        """
        Inicializa el explicador.
        
        Args:
            base_conocimientos: Base de conocimientos del león
            generalizador: Generalizador de patrones
        """
        self.base_conocimientos = base_conocimientos
        self.generalizador = generalizador
    
    def explicar_decision(self, estado: Estado, accion_elegida: str,
                         acciones_posibles: List[str]) -> str:
        """
        Explica por qué se eligió una acción específica.
        
        Args:
            estado: Estado del mundo
            accion_elegida: Acción que se eligió
            acciones_posibles: Todas las acciones disponibles
            
        Returns:
            Explicación en texto
        """
        lineas = [
            "=" * 70,
            "EXPLICACIÓN DE DECISIÓN",
            "=" * 70,
            ""
        ]
        
        # Descripción del estado
        lineas.append("ESTADO ACTUAL:")
        lineas.append(f"  {estado}")
        lineas.append("")
        
        # Valores Q de todas las acciones
        lineas.append("VALORES Q DE ACCIONES POSIBLES:")
        valores_q = []
        for accion in acciones_posibles:
            valor = self.base_conocimientos.obtener_valor_q(estado, accion)
            visitas = self.base_conocimientos.obtener_visitas(estado, accion)
            valores_q.append((accion, valor, visitas))
            
            marcador = " ← ELEGIDA" if accion == accion_elegida else ""
            lineas.append(f"  {accion.upper()}: Q={valor:.2f} (visitada {visitas} veces){marcador}")
        
        lineas.append("")
        
        # Análisis de la decisión
        mejor_accion = max(valores_q, key=lambda x: x[1])
        
        if accion_elegida == mejor_accion[0]:
            lineas.append("RAZÓN DE LA DECISIÓN:")
            lineas.append(f"  '{accion_elegida.upper()}' tiene el mayor valor Q ({mejor_accion[1]:.2f})")
            lineas.append("  Esta acción ha demostrado ser la más efectiva en situaciones similares.")
        else:
            lineas.append("RAZÓN DE LA DECISIÓN:")
            lineas.append("  Esta fue una acción de EXPLORACIÓN (no la mejor conocida)")
            lineas.append("  El león está probando alternativas para aprender más.")
        
        lineas.append("")
        
        # Generalización
        estado_gen = self.generalizador.crear_estado_generalizado(estado)
        lineas.append("ANÁLISIS GENERALIZADO:")
        lineas.append(f"  Zona: {estado_gen['posicion_zona']}")
        lineas.append(f"  Distancia: {estado_gen['distancia_categoria']}")
        lineas.append(f"  Impala: {estado_gen['impala_accion_general']}")
        lineas.append(f"  León escondido: {estado_gen['leon_escondido']}")
        
        # Recomendaciones por reglas
        recomendaciones = self.generalizador.obtener_recomendacion_por_regla(estado)
        if recomendaciones:
            lineas.append("")
            lineas.append("RECOMENDACIONES POR PATRONES GENERALIZADOS:")
            for accion, efectividad in recomendaciones[:3]:  # Top 3
                lineas.append(f"  {accion.upper()}: {efectividad:.1%} de efectividad")
        
        # Experiencia similar
        estados_similares = self.generalizador.encontrar_estados_similares(
            estado, self.base_conocimientos
        )
        
        if estados_similares:
            lineas.append("")
            lineas.append(f"EXPERIENCIA PREVIA: {len(estados_similares)} estados similares conocidos")
        
        return "\n".join(lineas)
    
    def comparar_acciones(self, estado: Estado,
                         acciones: List[str]) -> str:
        """
        Compara todas las acciones posibles para un estado.
        
        Args:
            estado: Estado del mundo
            acciones: Acciones a comparar
            
        Returns:
            Comparación en texto
        """
        lineas = [
            "=" * 70,
            "COMPARACIÓN DE ACCIONES",
            "=" * 70,
            f"Estado: {estado}",
            ""
        ]
        
        # Obtener valores y ordenar
        valores = [
            (accion, self.base_conocimientos.obtener_valor_q(estado, accion),
             self.base_conocimientos.obtener_visitas(estado, accion))
            for accion in acciones
        ]
        valores.sort(key=lambda x: x[1], reverse=True)
        
        lineas.append("RANKING DE ACCIONES:")
        for i, (accion, valor, visitas) in enumerate(valores, 1):
            barra = "█" * int(max(0, min(20, valor)))
            lineas.append(f"  {i}. {accion.upper():12} | Q={valor:6.2f} | Visitas={visitas:4} | {barra}")
        
        return "\n".join(lineas)
    
    def analizar_patron_caceria(self, historia_eventos: List) -> str:
        """
        Analiza un patrón de decisiones durante una cacería completa.
        
        Args:
            historia_eventos: Lista de eventos de una cacería
            
        Returns:
            Análisis en texto
        """
        lineas = [
            "=" * 70,
            "ANÁLISIS DE PATRÓN DE CACERÍA",
            "=" * 70,
            ""
        ]
        
        # Contar acciones
        acciones_leon = {}
        for evento in historia_eventos:
            accion = evento.accion_leon.split(':')[0]
            acciones_leon[accion] = acciones_leon.get(accion, 0) + 1
        
        lineas.append("DISTRIBUCIÓN DE ACCIONES:")
        total_acciones = sum(acciones_leon.values())
        for accion, cantidad in sorted(acciones_leon.items(), key=lambda x: x[1], reverse=True):
            porcentaje = (cantidad / total_acciones * 100) if total_acciones > 0 else 0
            barra = "█" * int(porcentaje / 5)
            lineas.append(f"  {accion:12}: {cantidad:3} veces ({porcentaje:5.1f}%) {barra}")
        
        lineas.append("")
        lineas.append(f"TOTAL DE TURNOS: {len(historia_eventos)}")
        
        # Análisis de estrategia
        lineas.append("")
        lineas.append("ANÁLISIS ESTRATÉGICO:")
        
        if acciones_leon.get('Esconderse', 0) > len(historia_eventos) * 0.3:
            lineas.append("  ▸ Estrategia CAUTELOSA: Se escondió frecuentemente")
        
        if acciones_leon.get('Avanzar', 0) > len(historia_eventos) * 0.5:
            lineas.append("  ▸ Estrategia AGRESIVA: Avanzó constantemente")
        
        if acciones_leon.get('Atacar', 0) > 0:
            turno_ataque = None
            for i, evento in enumerate(historia_eventos):
                if 'Atacar' in evento.accion_leon:
                    turno_ataque = i + 1
                    break
            
            if turno_ataque:
                lineas.append(f"  ▸ Primer ataque en turno {turno_ataque}")
                if turno_ataque < 5:
                    lineas.append("    (Ataque temprano - riesgoso)")
                elif turno_ataque > 10:
                    lineas.append("    (Ataque tardío - cauteloso)")
        
        return "\n".join(lineas)
    
    def generar_reporte_aprendizaje(self) -> str:
        """
        Genera un reporte del aprendizaje actual del león.
        
        Returns:
            Reporte en texto
        """
        lineas = [
            "=" * 70,
            "REPORTE DE APRENDIZAJE DEL LEÓN",
            "=" * 70,
            ""
        ]
        
        stats = self.base_conocimientos.obtener_estadisticas()
        
        lineas.append("ESTADÍSTICAS GENERALES:")
        for key, value in stats.items():
            lineas.append(f"  {key}: {value}")
        
        lineas.append("")
        lineas.append("LECCIONES PRINCIPALES:")
        
        # Encontrar las mejores acciones por categoría de distancia
        distancias = ["muy_cerca", "cerca", "media", "lejos"]
        acciones = ["avanzar", "esconderse", "atacar"]
        
        for dist in distancias:
            mejor_valor = -float('inf')
            mejor_accion = None
            
            # Buscar estados con esta distancia
            for estado in self.base_conocimientos.obtener_estados_conocidos():
                estado_gen = self.generalizador.crear_estado_generalizado(estado)
                if estado_gen['distancia_categoria'] == dist:
                    for accion in acciones:
                        valor = self.base_conocimientos.obtener_valor_q(estado, accion)
                        if valor > mejor_valor:
                            mejor_valor = valor
                            mejor_accion = accion
            
            if mejor_accion:
                lineas.append(f"  • Cuando está {dist}: {mejor_accion.upper()} (Q={mejor_valor:.2f})")
        
        return "\n".join(lineas)


if __name__ == "__main__":
    # Pruebas básicas
    from knowledge.base_conocimientos import Estado, BaseConocimientos
    
    print("=== Pruebas del Explicador ===\n")
    
    # Crear componentes
    bc = BaseConocimientos()
    gen = Generalizador()
    explicador = Explicador(bc, gen)
    
    # Crear estado de prueba
    estado = Estado(1, 4.0, "ver_frente", False, True)
    
    # Agregar algunos valores Q
    bc.actualizar_valor_q(estado, "avanzar", 8.5)
    bc.actualizar_valor_q(estado, "esconderse", 12.3)
    bc.actualizar_valor_q(estado, "atacar", 3.2)
    
    # Explicar decisión
    print(explicador.explicar_decision(estado, "esconderse", ["avanzar", "esconderse", "atacar"]))
    
    print("\n" + explicador.comparar_acciones(estado, ["avanzar", "esconderse", "atacar"]))
    
    print("\n" + explicador.generar_reporte_aprendizaje())
