"""
Módulo de Q-Learning.
Implementa el algoritmo de aprendizaje por refuerzo.
"""

import random
from typing import List, Optional, Tuple

from knowledge.base_conocimientos import BaseConocimientos, Estado, Experiencia
from learning.recompensas import SistemaRecompensas


class QLearning:
    """
    Implementa el algoritmo Q-Learning para el aprendizaje del león.
    """
    
    def __init__(self, base_conocimientos: BaseConocimientos,
                 sistema_recompensas: SistemaRecompensas,
                 alpha: float = 0.1,
                 gamma: float = 0.9,
                 epsilon: float = 0.1):
        """
        Inicializa el algoritmo Q-Learning.
        
        Args:
            base_conocimientos: Base de conocimientos del león
            sistema_recompensas: Sistema de recompensas
            alpha: Tasa de aprendizaje (0-1)
            gamma: Factor de descuento (0-1)
            epsilon: Probabilidad de exploración (0-1)
        """
        self.base_conocimientos = base_conocimientos
        self.sistema_recompensas = sistema_recompensas
        
        # Hiperparámetros
        self.alpha = alpha      # Learning rate
        self.gamma = gamma      # Discount factor
        self.epsilon = epsilon  # Exploration rate
        
        # Estadísticas de aprendizaje
        self.total_actualizaciones = 0
        self.exploraciones = 0
        self.explotaciones = 0
    
    def seleccionar_accion(self, estado: Estado,
                          acciones_posibles: List[str],
                          forzar_exploracion: bool = False) -> Tuple[str, str]:
        """
        Selecciona una acción usando la política epsilon-greedy.
        
        Args:
            estado: Estado actual
            acciones_posibles: Lista de acciones válidas
            forzar_exploracion: Si True, fuerza exploración
            
        Returns:
            Tupla (accion_seleccionada, tipo) donde tipo es 'exploración' o 'explotación'
        """
        # Decidir entre exploración y explotación
        if forzar_exploracion or random.random() < self.epsilon:
            # EXPLORACIÓN: acción aleatoria
            accion = random.choice(acciones_posibles)
            self.exploraciones += 1
            return accion, "exploración"
        else:
            # EXPLOTACIÓN: mejor acción conocida
            accion, _ = self.base_conocimientos.obtener_mejor_accion(estado, acciones_posibles)
            self.explotaciones += 1
            return accion, "explotación"
    
    def actualizar_valor_q(self, estado: Estado, accion: str,
                          recompensa: float,
                          siguiente_estado: Optional[Estado],
                          acciones_posibles: List[str]) -> float:
        """
        Actualiza el valor Q usando la ecuación de Bellman.
        
        Q(s,a) = Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]
        
        Args:
            estado: Estado actual
            accion: Acción ejecutada
            recompensa: Recompensa recibida
            siguiente_estado: Estado resultante (None si terminó)
            acciones_posibles: Acciones posibles en el siguiente estado
            
        Returns:
            Nuevo valor Q
        """
        # Obtener valor Q actual
        q_actual = self.base_conocimientos.obtener_valor_q(estado, accion)
        
        # Calcular valor Q del siguiente estado
        if siguiente_estado is not None:
            # Obtener el máximo Q del siguiente estado
            _, max_q_siguiente = self.base_conocimientos.obtener_mejor_accion(
                siguiente_estado, acciones_posibles
            )
        else:
            # Estado terminal, no hay siguiente estado
            max_q_siguiente = 0.0
        
        # Ecuación de Bellman
        nuevo_q = q_actual + self.alpha * (recompensa + self.gamma * max_q_siguiente - q_actual)
        
        # Actualizar en la base de conocimientos
        self.base_conocimientos.actualizar_valor_q(estado, accion, nuevo_q)
        
        self.total_actualizaciones += 1
        
        return nuevo_q
    
    def aprender_de_experiencia(self, experiencia: Experiencia,
                                acciones_posibles: List[str]) -> float:
        """
        Aprende de una experiencia individual.
        
        Args:
            experiencia: Experiencia a procesar
            acciones_posibles: Acciones posibles en el siguiente estado
            
        Returns:
            Nuevo valor Q
        """
        # Agregar experiencia a la base de conocimientos
        self.base_conocimientos.agregar_experiencia(experiencia)
        
        # Actualizar valor Q
        nuevo_q = self.actualizar_valor_q(
            experiencia.estado,
            experiencia.accion,
            experiencia.recompensa,
            experiencia.siguiente_estado,
            acciones_posibles
        )
        
        return nuevo_q
    
    def ajustar_epsilon(self, progreso: float):
        """
        Ajusta epsilon (exploración) según el progreso del entrenamiento.
        Decae epsilon con el tiempo para favorecer explotación.
        
        Args:
            progreso: Progreso del entrenamiento (0-1)
        """
        # Decaimiento lineal
        epsilon_inicial = 0.5
        epsilon_final = 0.01
        self.epsilon = epsilon_inicial - (epsilon_inicial - epsilon_final) * progreso
    
    def ajustar_alpha(self, progreso: float):
        """
        Ajusta alpha (tasa de aprendizaje) según el progreso.
        
        Args:
            progreso: Progreso del entrenamiento (0-1)
        """
        # Decaimiento suave
        alpha_inicial = 0.3
        alpha_final = 0.05
        self.alpha = alpha_inicial - (alpha_inicial - alpha_final) * progreso
    
    def obtener_estadisticas(self) -> dict:
        """
        Obtiene estadísticas del aprendizaje.
        
        Returns:
            Diccionario con estadísticas
        """
        total_decisiones = self.exploraciones + self.explotaciones
        tasa_exploracion = (self.exploraciones / total_decisiones * 100) if total_decisiones > 0 else 0
        
        return {
            'actualizaciones_q': self.total_actualizaciones,
            'exploraciones': self.exploraciones,
            'explotaciones': self.explotaciones,
            'tasa_exploracion': round(tasa_exploracion, 2),
            'alpha': round(self.alpha, 3),
            'gamma': round(self.gamma, 3),
            'epsilon': round(self.epsilon, 3)
        }
    
    def resetear_estadisticas(self):
        """Resetea las estadísticas de aprendizaje"""
        self.total_actualizaciones = 0
        self.exploraciones = 0
        self.explotaciones = 0
    
    def __str__(self) -> str:
        """Representación en string"""
        return f"QLearning(α={self.alpha:.3f}, γ={self.gamma:.3f}, ε={self.epsilon:.3f})"


if __name__ == "__main__":
    # Pruebas básicas
    from knowledge.base_conocimientos import Estado, BaseConocimientos, Experiencia
    
    print("=== Pruebas de Q-Learning ===\n")
    
    # Inicializar componentes
    bc = BaseConocimientos()
    sr = SistemaRecompensas()
    ql = QLearning(bc, sr, alpha=0.1, gamma=0.9, epsilon=0.3)
    
    print(f"Configuración inicial: {ql}\n")
    
    # Crear estados de prueba
    estado1 = Estado(1, 5.0, "ver_frente", False, True)
    estado2 = Estado(1, 4.0, "beber_agua", False, False)
    
    acciones = ["avanzar", "esconderse", "atacar"]
    
    # Prueba 1: Selección de acción (exploración vs explotación)
    print("1. Selección de acciones (10 pruebas):")
    for i in range(10):
        accion, tipo = ql.seleccionar_accion(estado1, acciones)
        print(f"   Prueba {i+1}: {accion} ({tipo})")
    
    # Prueba 2: Actualización de valor Q
    print("\n2. Actualización de valores Q:")
    print(f"   Q inicial (estado1, avanzar): {bc.obtener_valor_q(estado1, 'avanzar'):.2f}")
    
    # Simular una experiencia positiva
    nuevo_q = ql.actualizar_valor_q(estado1, "avanzar", 5.0, estado2, acciones)
    print(f"   Q después de recompensa +5.0: {nuevo_q:.2f}")
    
    # Otra actualización
    nuevo_q = ql.actualizar_valor_q(estado1, "avanzar", 10.0, estado2, acciones)
    print(f"   Q después de recompensa +10.0: {nuevo_q:.2f}")
    
    # Prueba 3: Aprender de experiencia
    print("\n3. Aprender de experiencia completa:")
    experiencia = Experiencia(
        estado=estado1,
        accion="esconderse",
        recompensa=2.0,
        siguiente_estado=estado2,
        exito=False
    )
    nuevo_q = ql.aprender_de_experiencia(experiencia, acciones)
    print(f"   Q aprendido (estado1, esconderse): {nuevo_q:.2f}")
    
    # Prueba 4: Ajuste dinámico de parámetros
    print("\n4. Ajuste dinámico de epsilon y alpha:")
    print(f"   Inicial - Alpha: {ql.alpha:.3f}, Epsilon: {ql.epsilon:.3f}")
    
    ql.ajustar_epsilon(0.5)  # 50% progreso
    ql.ajustar_alpha(0.5)
    print(f"   50% progreso - Alpha: {ql.alpha:.3f}, Epsilon: {ql.epsilon:.3f}")
    
    ql.ajustar_epsilon(1.0)  # 100% progreso
    ql.ajustar_alpha(1.0)
    print(f"   100% progreso - Alpha: {ql.alpha:.3f}, Epsilon: {ql.epsilon:.3f}")
    
    # Prueba 5: Estadísticas
    print("\n5. Estadísticas de aprendizaje:")
    stats = ql.obtener_estadisticas()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print(f"\nBase de conocimientos: {bc}")
