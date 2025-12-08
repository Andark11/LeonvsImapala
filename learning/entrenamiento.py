"""
Módulo de entrenamiento.
Orquesta ciclos de entrenamiento automático.
"""

from typing import List, Dict, Optional, Callable
import time

from environment import Abrevadero
from agents.leon import Leon, AccionLeon
from agents.impala import Impala
from simulation.caceria import Caceria, ResultadoCaceria, ModoBehaviorImpala
from knowledge.base_conocimientos import BaseConocimientos, Estado, Experiencia
from knowledge.generalizacion import Generalizador
from learning.q_learning import QLearning
from learning.recompensas import SistemaRecompensas


class Entrenador:
    """
    Orquesta ciclos de entrenamiento automático del león.
    """
    
    def __init__(self):
        """Inicializa el entrenador"""
        # Componentes del sistema
        self.abrevadero = Abrevadero()
        self.base_conocimientos = BaseConocimientos()
        self.generalizador = Generalizador()
        self.sistema_recompensas = SistemaRecompensas()
        self.q_learning = QLearning(self.base_conocimientos, self.sistema_recompensas)
        
        # Estadísticas globales
        self.total_cacerias = 0
        self.cacerias_exitosas = 0
        self.tiempo_inicio = None
        self.tiempo_fin = None
    
    def entrenar(self, num_episodios: int,
                posiciones_iniciales: List[int] = None,
                comportamiento_impala: ModoBehaviorImpala = ModoBehaviorImpala.ALEATORIO,
                verbose: bool = False,
                callback_progreso: Optional[Callable] = None) -> Dict:
        """
        Ejecuta un ciclo de entrenamiento.
        
        Args:
            num_episodios: Número de cacerías a simular
            posiciones_iniciales: Posiciones iniciales posibles (default: todas 1-8)
            comportamiento_impala: Modo de comportamiento del impala
            verbose: Si True, imprime información detallada
            callback_progreso: Función a llamar con el progreso (opcional)
            
        Returns:
            Diccionario con resultados del entrenamiento
        """
        import random
        
        if posiciones_iniciales is None:
            posiciones_iniciales = list(range(1, 9))
        
        self.tiempo_inicio = time.time()
        exitosas_en_ciclo = 0
        
        for episodio in range(num_episodios):
            # Ajustar parámetros de aprendizaje dinámicamente
            progreso = episodio / num_episodios
            self.q_learning.ajustar_epsilon(progreso)
            self.q_learning.ajustar_alpha(progreso)
            
            # Posición inicial aleatoria
            posicion_inicial = random.choice(posiciones_iniciales)
            
            # Ejecutar cacería de entrenamiento
            resultado = self._ejecutar_caceria_entrenamiento(posicion_inicial, comportamiento_impala)
            
            self.total_cacerias += 1
            if resultado == ResultadoCaceria.EXITO:
                exitosas_en_ciclo += 1
                self.cacerias_exitosas += 1
            
            # Callback de progreso
            if callback_progreso and (episodio + 1) % 100 == 0:
                callback_progreso(episodio + 1, num_episodios, exitosas_en_ciclo)
            
            # Mensaje de progreso
            if verbose and (episodio + 1) % 500 == 0:
                tasa = (exitosas_en_ciclo / (episodio + 1)) * 100
                print(f"Episodio {episodio + 1}/{num_episodios} - Tasa éxito: {tasa:.1f}%")
        
        self.tiempo_fin = time.time()
        
        # Generar reporte
        return self._generar_reporte_entrenamiento(num_episodios, exitosas_en_ciclo)
    
    def _ejecutar_caceria_entrenamiento(self, posicion_inicial: int,
                                       comportamiento_impala: ModoBehaviorImpala) -> ResultadoCaceria:
        """
        Ejecuta una cacería de entrenamiento.
        
        Args:
            posicion_inicial: Posición inicial del león
            comportamiento_impala: Modo de comportamiento del impala
            
        Returns:
            Resultado de la cacería
        """
        caceria = Caceria(self.abrevadero)
        caceria.inicializar_caceria(posicion_inicial, comportamiento_impala)
        
        acciones_leon = ["avanzar", "esconderse", "atacar"]
        
        estado_anterior = None
        distancia_anterior = None
        
        while caceria.resultado == ResultadoCaceria.EN_PROGRESO:
            # Obtener estado actual
            estado_actual = self._crear_estado_desde_caceria(caceria)
            distancia_actual = caceria.verificador.calcular_distancia_actual(caceria.leon)
            
            # Seleccionar acción usando Q-Learning
            accion_leon, _ = self.q_learning.seleccionar_accion(estado_actual, acciones_leon)
            
            # Ejecutar turno
            terminada, _ = caceria.ejecutar_turno(AccionLeon[accion_leon.upper()])
            
            # Calcular recompensa
            if estado_anterior is not None:
                distancia_nueva = caceria.verificador.calcular_distancia_actual(caceria.leon)
                
                # Verificar si impala puede ver al león
                from agents.impala import AccionImpala
                accion_impala_actual = AccionImpala.HUIR if caceria.impala.esta_huyendo else AccionImpala.VER_FRENTE
                impala_puede_ver = caceria.verificador.impala_puede_ver_leon(
                    caceria.leon, caceria.impala, accion_impala_actual
                )
                
                recompensa = self.sistema_recompensas.calcular_recompensa_total(
                    distancia_anterior=distancia_anterior,
                    distancia_nueva=distancia_nueva,
                    accion=accion_leon,
                    leon_escondido=caceria.leon.esta_escondido,
                    impala_puede_ver=impala_puede_ver,
                    impala_huye=caceria.impala.esta_huyendo,
                    caceria_terminada=terminada,
                    exito=(caceria.resultado == ResultadoCaceria.EXITO)
                )
                
                # Crear experiencia y aprender
                siguiente_estado = estado_actual if not terminada else None
                experiencia = Experiencia(
                    estado=estado_anterior,
                    accion=accion_leon,
                    recompensa=recompensa,
                    siguiente_estado=siguiente_estado,
                    exito=(caceria.resultado == ResultadoCaceria.EXITO)
                )
                
                self.q_learning.aprender_de_experiencia(experiencia, acciones_leon)
            
            # Guardar estado para el próximo turno
            estado_anterior = estado_actual
            distancia_anterior = distancia_actual
        
        return caceria.resultado
    
    def _crear_estado_desde_caceria(self, caceria: Caceria) -> Estado:
        """
        Crea un Estado desde el estado actual de la cacería.
        
        Args:
            caceria: Cacería en curso
            
        Returns:
            Estado representado
        """
        # Redondear distancia a 0.5 cuadros para generalización
        distancia = caceria.verificador.calcular_distancia_actual(caceria.leon)
        distancia_redondeada = round(distancia * 2) / 2
        
        # Obtener acción del impala (mapeo de AccionImpala a string)
        accion_impala_map = {
            'ver_izquierda': 'ver_izquierda',
            'ver_derecha': 'ver_derecha',
            'ver_frente': 'ver_frente',
            'beber_agua': 'beber_agua',
            'huir': 'huir'
        }
        
        # Usar la última acción registrada
        from agents.impala import AccionImpala
        accion_impala_enum = AccionImpala.VER_FRENTE  # Default
        accion_impala_str = "ver_frente"
        
        if caceria.impala.esta_huyendo:
            accion_impala_enum = AccionImpala.HUIR
            accion_impala_str = "huir"
        
        # Verificar si el impala puede ver al león
        impala_puede_ver = caceria.verificador.impala_puede_ver_leon(
            caceria.leon, caceria.impala, accion_impala_enum
        )
        
        return Estado(
            posicion_leon=caceria.leon.posicion,
            distancia_impala=distancia_redondeada,
            accion_impala=accion_impala_str,
            leon_escondido=caceria.leon.esta_escondido,
            impala_puede_ver=impala_puede_ver
        )
    
    def _generar_reporte_entrenamiento(self, num_episodios: int,
                                      exitosas: int) -> Dict:
        """
        Genera un reporte del entrenamiento.
        
        Args:
            num_episodios: Número de episodios ejecutados
            exitosas: Número de cacerías exitosas
            
        Returns:
            Diccionario con el reporte
        """
        duracion = self.tiempo_fin - self.tiempo_inicio
        tasa_exito = (exitosas / num_episodios * 100) if num_episodios > 0 else 0
        
        return {
            'episodios': num_episodios,
            'exitosas': exitosas,
            'fallidas': num_episodios - exitosas,
            'tasa_exito': round(tasa_exito, 2),
            'duracion_segundos': round(duracion, 2),
            'episodios_por_segundo': round(num_episodios / duracion, 2) if duracion > 0 else 0,
            'estadisticas_bc': self.base_conocimientos.obtener_estadisticas(),
            'estadisticas_ql': self.q_learning.obtener_estadisticas()
        }
    
    def entrenar_incremental(self, num_episodios: int,
                           checkpoint_cada: int = 1000,
                           callback_checkpoint: Optional[Callable] = None) -> List[Dict]:
        """
        Entrenamiento incremental con checkpoints.
        
        Args:
            num_episodios: Total de episodios
            checkpoint_cada: Guardar checkpoint cada N episodios
            callback_checkpoint: Función a llamar en cada checkpoint
            
        Returns:
            Lista de reportes de cada checkpoint
        """
        reportes = []
        episodios_restantes = num_episodios
        
        while episodios_restantes > 0:
            batch = min(checkpoint_cada, episodios_restantes)
            
            reporte = self.entrenar(batch, verbose=True)
            reportes.append(reporte)
            
            if callback_checkpoint:
                callback_checkpoint(reporte)
            
            episodios_restantes -= batch
        
        return reportes
    
    def obtener_estadisticas_globales(self) -> Dict:
        """
        Obtiene estadísticas globales del entrenamiento.
        
        Returns:
            Diccionario con estadísticas
        """
        return {
            'total_cacerias': self.total_cacerias,
            'cacerias_exitosas': self.cacerias_exitosas,
            'tasa_exito_global': round((self.cacerias_exitosas / self.total_cacerias * 100) 
                                       if self.total_cacerias > 0 else 0, 2),
            'base_conocimientos': self.base_conocimientos.obtener_estadisticas(),
            'q_learning': self.q_learning.obtener_estadisticas()
        }
    
    def generar_reporte_completo(self) -> str:
        """
        Genera un reporte completo en texto.
        
        Returns:
            String con el reporte
        """
        lineas = [
            "=" * 70,
            "REPORTE COMPLETO DE ENTRENAMIENTO",
            "=" * 70,
            ""
        ]
        
        stats = self.obtener_estadisticas_globales()
        
        lineas.append("ESTADÍSTICAS GLOBALES:")
        lineas.append(f"  Total de cacerías: {stats['total_cacerias']}")
        lineas.append(f"  Cacerías exitosas: {stats['cacerias_exitosas']}")
        lineas.append(f"  Tasa de éxito: {stats['tasa_exito_global']}%")
        lineas.append("")
        
        lineas.append("BASE DE CONOCIMIENTOS:")
        for key, value in stats['base_conocimientos'].items():
            lineas.append(f"  {key}: {value}")
        lineas.append("")
        
        lineas.append("Q-LEARNING:")
        for key, value in stats['q_learning'].items():
            lineas.append(f"  {key}: {value}")
        lineas.append("")
        
        return "\n".join(lineas)
    
    def resetear(self):
        """Resetea todo el sistema de entrenamiento"""
        self.base_conocimientos.limpiar()
        self.q_learning.resetear_estadisticas()
        self.total_cacerias = 0
        self.cacerias_exitosas = 0


if __name__ == "__main__":
    # Pruebas básicas
    print("=== Pruebas del Entrenador ===\n")
    
    entrenador = Entrenador()
    
    # Entrenamiento corto de prueba
    print("Ejecutando entrenamiento de 100 episodios...")
    reporte = entrenador.entrenar(
        num_episodios=100,
        posiciones_iniciales=[1, 3, 5, 7],
        verbose=True
    )
    
    print("\n" + "=" * 70)
    print("RESULTADOS DEL ENTRENAMIENTO")
    print("=" * 70)
    for key, value in reporte.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"{key}: {value}")
    
    print("\n" + entrenador.generar_reporte_completo())
