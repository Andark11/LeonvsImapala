"""
Interfaz visual en terminal (ASCII) con grid 19×19.
Sin dependencias de matplotlib, solo caracteres en la terminal.
"""

from typing import Optional
import math
import os
import time

from environment import Abrevadero, Direccion
from simulation.caceria import Caceria, ModoBehaviorImpala, ResultadoCaceria
from agents.leon import AccionLeon
from knowledge.base_conocimientos import BaseConocimientos, Estado
from learning.q_learning import QLearning


class InterfazTerminalGrid:
    """
    Interfaz visual en terminal usando ASCII art para mostrar el grid 19×19.
    """
    
    GRID_SIZE = 19
    ESCALA = 1.9  # Factor de escala: 9.5 cuadros polares = 18.05 cuadros grid
    
    # Caracteres para visualización
    CHAR_VACIO = '·'
    CHAR_LEON = '🦁'
    CHAR_LEON_SIMPLE = 'L'
    CHAR_IMPALA = '🦌'
    CHAR_IMPALA_SIMPLE = 'I'
    CHAR_ABREVADERO = '▓'
    CHAR_TRAYECTORIA = '○'
    CHAR_POSICION = '●'
    CHAR_VISION = '░'
    
    # Colores ANSI
    COLOR_RESET = '\033[0m'
    COLOR_LEON = '\033[91m'  # Rojo brillante
    COLOR_LEON_ESCONDIDO = '\033[90m'  # Gris
    COLOR_LEON_ATACANDO = '\033[95m'  # Magenta
    COLOR_IMPALA = '\033[92m'  # Verde
    COLOR_IMPALA_HUYENDO = '\033[93m'  # Amarillo
    COLOR_ABREVADERO = '\033[94m'  # Azul
    COLOR_TRAYECTORIA = '\033[96m'  # Cian
    COLOR_VISION = '\033[43m'  # Fondo amarillo
    COLOR_BORDE = '\033[90m'  # Gris oscuro
    
    def __init__(self, base_conocimientos: Optional[BaseConocimientos] = None,
                 agente_q: Optional[QLearning] = None,
                 usar_emojis: bool = True):
        """
        Inicializa la interfaz en terminal.
        
        Args:
            base_conocimientos: Base de conocimientos del león
            agente_q: Agente Q-Learning
            usar_emojis: Si usar emojis o caracteres ASCII simples
        """
        self.abrevadero = Abrevadero()
        self.caceria = Caceria(self.abrevadero)
        self.base_conocimientos = base_conocimientos
        self.agente_q = agente_q
        self.usar_emojis = usar_emojis
        
        # Grid para dibujar
        self.grid = [[' ' for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.grid_colores = [['' for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        
        # Historia de posiciones
        self.historia_leon = []
    
    def _coord_polar_a_grid(self, x_polar: float, y_polar: float) -> tuple:
        """Convierte coordenadas polares a índices del grid."""
        centro = self.GRID_SIZE / 2
        col = int(centro + (x_polar * self.ESCALA))
        fila = int(centro - (y_polar * self.ESCALA))
        # Asegurar que esté dentro del grid
        col = max(0, min(self.GRID_SIZE - 1, col))
        fila = max(0, min(self.GRID_SIZE - 1, fila))
        return col, fila
    
    def _limpiar_pantalla(self):
        """Limpia la pantalla del terminal."""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def _inicializar_grid(self):
        """Inicializa el grid vacío."""
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                self.grid[i][j] = self.CHAR_VACIO
                self.grid_colores[i][j] = ''
    
    def _dibujar_abrevadero(self):
        """Dibuja el abrevadero en el centro del grid."""
        centro = self.GRID_SIZE // 2
        # Rectángulo de 4×2 en el centro
        for i in range(centro - 1, centro + 2):
            for j in range(centro - 2, centro + 3):
                if 0 <= i < self.GRID_SIZE and 0 <= j < self.GRID_SIZE:
                    self.grid[i][j] = self.CHAR_ABREVADERO
                    self.grid_colores[i][j] = self.COLOR_ABREVADERO
    
    def _dibujar_posiciones_iniciales(self):
        """Dibuja las 8 posiciones iniciales del león."""
        for pos in range(1, 9):
            x_polar, y_polar = self.abrevadero.obtener_coordenadas(pos)
            col, fila = self._coord_polar_a_grid(x_polar, y_polar)
            if self.grid[fila][col] == self.CHAR_VACIO:
                self.grid[fila][col] = str(pos)
                self.grid_colores[fila][col] = self.COLOR_BORDE
    
    def _dibujar_vision_impala(self):
        """Dibuja el cono de visión del impala."""
        centro = self.GRID_SIZE // 2
        direccion = self.caceria.impala.direccion_vista
        angulo_central = direccion.value
        
        # Dibujar líneas de visión (simplificado)
        for distancia in range(1, self.GRID_SIZE // 2):
            for angulo_offset in range(-60, 61, 15):  # 120° total
                angulo = angulo_central + angulo_offset
                rad = math.radians(angulo)
                
                x = distancia * math.sin(rad)
                y = distancia * math.cos(rad)
                
                col, fila = self._coord_polar_a_grid(x, y)
                
                if (0 <= fila < self.GRID_SIZE and 0 <= col < self.GRID_SIZE and
                    self.grid[fila][col] == self.CHAR_VACIO):
                    self.grid[fila][col] = self.CHAR_VISION
                    self.grid_colores[fila][col] = self.COLOR_VISION
    
    def _dibujar_trayectoria(self):
        """Dibuja la trayectoria del león."""
        for col, fila in self.historia_leon[:-1]:  # Excluir posición actual
            if (0 <= fila < self.GRID_SIZE and 0 <= col < self.GRID_SIZE and
                self.grid[fila][col] in [self.CHAR_VACIO, self.CHAR_VISION]):
                self.grid[fila][col] = self.CHAR_TRAYECTORIA
                self.grid_colores[fila][col] = self.COLOR_TRAYECTORIA
    
    def _dibujar_impala(self):
        """Dibuja el impala en su posición actual."""
        # Si la cacería ya terminó
        if self.caceria.resultado == ResultadoCaceria.FRACASO:
            return  # El impala escapó exitosamente, ya no se ve
        elif self.caceria.resultado == ResultadoCaceria.EXITO:
            # León atrapó al impala - NO dibujar aquí, se dibujará junto con el león
            return
        
        # Si está huyendo, calcular su posición en movimiento
        if self.caceria.impala.esta_huyendo and self.caceria.impala.direccion_huida:
            # Calcular desplazamiento acumulado basado en tiempo huyendo
            tiempo_huyendo = self.caceria.impala.tiempo_huyendo
            velocidad = self.caceria.impala.velocidad_huida
            
            # Distancia total recorrida
            distancia_total = tiempo_huyendo * velocidad
            
            # Determinar dirección (este = positivo X, oeste = negativo X)
            if self.caceria.impala.direccion_huida == Direccion.ESTE:
                x_impala = distancia_total
                y_impala = 0
            else:  # OESTE
                x_impala = -distancia_total
                y_impala = 0
            
            col, fila = self._coord_polar_a_grid(x_impala, y_impala)
        else:
            # Si no está huyendo, está en el centro del abrevadero
            centro = self.GRID_SIZE // 2
            col, fila = centro, centro
        
        char = self.CHAR_IMPALA if self.usar_emojis else self.CHAR_IMPALA_SIMPLE
        color = self.COLOR_IMPALA_HUYENDO if self.caceria.impala.esta_huyendo else self.COLOR_IMPALA
        
        # Verificar que esté dentro del grid
        if 0 <= fila < self.GRID_SIZE and 0 <= col < self.GRID_SIZE:
            self.grid[fila][col] = char
            self.grid_colores[fila][col] = color
    
    def _dibujar_leon(self):
        """Dibuja el león en su posición actual."""
        # Obtener posición
        if self.caceria.leon.posicion_exacta:
            x_polar, y_polar = self.caceria.leon.posicion_exacta
        else:
            x_polar, y_polar = self.abrevadero.obtener_coordenadas(self.caceria.leon.posicion)
        
        col, fila = self._coord_polar_a_grid(x_polar, y_polar)
        
        # Guardar en historia
        self.historia_leon.append((col, fila))
        
        # Si capturó al impala, mostrar ambos juntos
        if self.caceria.resultado == ResultadoCaceria.EXITO:
            if self.usar_emojis:
                char = "🦁🦌"  # León e impala juntos
            else:
                char = "LI"  # León e impala juntos (versión texto)
            color = self.COLOR_LEON_ATACANDO  # Color de éxito
        else:
            # Determinar carácter y color normal
            if self.usar_emojis:
                char = self.CHAR_LEON
            else:
                char = self.CHAR_LEON_SIMPLE
            
            if self.caceria.leon.esta_atacando:
                color = self.COLOR_LEON_ATACANDO
            elif self.caceria.leon.esta_escondido:
                color = self.COLOR_LEON_ESCONDIDO
            else:
                color = self.COLOR_LEON
        
        self.grid[fila][col] = char
        self.grid_colores[fila][col] = color
    
    def _calcular_distancia_actual(self) -> float:
        """Calcula la distancia actual león-impala."""
        # Posición del león
        if self.caceria.leon.posicion_exacta:
            leon_x, leon_y = self.caceria.leon.posicion_exacta
        else:
            leon_x, leon_y = self.abrevadero.obtener_coordenadas(self.caceria.leon.posicion)
        
        # Posición del impala
        if self.caceria.impala.esta_huyendo and self.caceria.impala.direccion_huida:
            tiempo = self.caceria.impala.tiempo_huyendo
            velocidad = self.caceria.impala.velocidad_huida
            distancia = tiempo * velocidad
            
            if self.caceria.impala.direccion_huida == Direccion.ESTE:
                impala_x, impala_y = distancia, 0
            else:  # OESTE
                impala_x, impala_y = -distancia, 0
        else:
            impala_x, impala_y = 0, 0  # Centro del abrevadero
        
        # Distancia euclidiana
        return math.sqrt((leon_x - impala_x)**2 + (leon_y - impala_y)**2)
    
    def _renderizar_grid(self):
        """Renderiza el grid en la terminal."""
        # Borde superior
        print(self.COLOR_BORDE + "┌" + "─" * (self.GRID_SIZE * 2 + 1) + "┐" + self.COLOR_RESET)
        
        # Contenido del grid
        for i in range(self.GRID_SIZE):
            linea = self.COLOR_BORDE + "│ " + self.COLOR_RESET
            for j in range(self.GRID_SIZE):
                color = self.grid_colores[i][j]
                char = self.grid[i][j]
                linea += color + char + self.COLOR_RESET + " "
            linea += self.COLOR_BORDE + "│" + self.COLOR_RESET
            print(linea)
        
        # Borde inferior
        print(self.COLOR_BORDE + "└" + "─" * (self.GRID_SIZE * 2 + 1) + "┘" + self.COLOR_RESET)
    
    def _mostrar_info_panel(self, turno: int, accion_impala: str, accion_leon: str):
        """Muestra panel de información debajo del grid."""
        distancia = self._calcular_distancia_actual()
        distancia_grid = distancia * self.ESCALA  # Convertir a celdas del grid 19×19
        
        print("\n" + "=" * 70)
        print(f"  TURNO {turno}  |  Distancia: {distancia_grid:.1f} celdas del grid (≈{distancia:.2f} unidades)")
        print("=" * 70)
        print(f"  Impala: {accion_impala:50s}")
        print(f"  León: {accion_leon:50s}")
        
        # Mostrar posiciones (debug)
        if self.caceria.leon.posicion_exacta:
            leon_x, leon_y = self.caceria.leon.posicion_exacta
            print(f"  🦁 Posición León: ({leon_x:.2f}, {leon_y:.2f})")
        else:
            print(f"  🦁 Posición León: #{self.caceria.leon.posicion} (inicial)")
        
        if self.caceria.resultado == ResultadoCaceria.EXITO:
            # León atrapó al impala
            print(f"  🦌 Impala CAPTURADO por el león ✓")
        elif self.caceria.resultado == ResultadoCaceria.FRACASO:
            # Ya escapó completamente
            tiempo = self.caceria.impala.tiempo_huyendo
            vel = self.caceria.impala.velocidad_huida
            dist = tiempo * vel
            dist_grid = dist * self.ESCALA
            dir_str = "ESTE ➡️" if self.caceria.impala.direccion_huida == Direccion.ESTE else "OESTE ⬅️"
            print(f"  🦌 Impala ESCAPÓ: {dist_grid:.1f} celdas hacia {dir_str} - ¡Fuera de alcance!")
        elif self.caceria.impala.esta_huyendo:
            # Está huyendo pero aún en el grid
            tiempo = self.caceria.impala.tiempo_huyendo
            vel = self.caceria.impala.velocidad_huida
            dist = tiempo * vel
            dist_grid = dist * self.ESCALA
            dir_str = "ESTE ➡️" if self.caceria.impala.direccion_huida == Direccion.ESTE else "OESTE ⬅️"
            print(f"  🦌 Impala huyendo: {dist_grid:.1f} celdas hacia {dir_str} (vel={vel}, t={tiempo})")
        else:
            print(f"  🦌 Impala en abrevadero: (0.0, 0.0)")
        
        # Estados
        estados = []
        if self.caceria.leon.esta_escondido:
            estados.append("ESCONDIDO")
        if self.caceria.leon.esta_atacando:
            estados.append("ATACANDO")
        if self.caceria.resultado == ResultadoCaceria.EXITO:
            estados.append("IMPALA CAPTURADO ✓")
        elif self.caceria.resultado == ResultadoCaceria.FRACASO:
            estados.append(f"IMPALA ESCAPÓ 💨 - Cacería fallida")
        elif self.caceria.impala.esta_huyendo:
            estados.append(f"IMPALA HUYENDO 💨 (vel {self.caceria.impala.velocidad_huida})")
        
        if estados:
            print(f"  Estado: {' | '.join(estados)}")
        
        print("=" * 70)
    
    def _mostrar_leyenda(self):
        """Muestra la leyenda de símbolos."""
        print("\n📋 LEYENDA:")
        if self.usar_emojis:
            print(f"  {self.COLOR_LEON}🦁{self.COLOR_RESET} León  |  "
                  f"{self.COLOR_IMPALA}🦌{self.COLOR_RESET} Impala  |  "
                  f"{self.COLOR_ABREVADERO}{self.CHAR_ABREVADERO}{self.COLOR_RESET} Abrevadero  |  "
                  f"{self.COLOR_TRAYECTORIA}{self.CHAR_TRAYECTORIA}{self.COLOR_RESET} Trayectoria  |  "
                  f"{self.COLOR_VISION}{self.CHAR_VISION}{self.COLOR_RESET} Visión")
        else:
            print(f"  {self.COLOR_LEON}L{self.COLOR_RESET} León  |  "
                  f"{self.COLOR_IMPALA}I{self.COLOR_RESET} Impala  |  "
                  f"{self.COLOR_ABREVADERO}{self.CHAR_ABREVADERO}{self.COLOR_RESET} Abrevadero  |  "
                  f"{self.COLOR_TRAYECTORIA}{self.CHAR_TRAYECTORIA}{self.COLOR_RESET} Trayectoria  |  "
                  f"{self.COLOR_VISION}{self.CHAR_VISION}{self.COLOR_RESET} Visión")
        print(f"\n  💡 Grid: 19×19 celdas | Centro: (9.5, 9.5) | RADIO inicial: 9.5 cuadros (≈18 celdas)")
    
    def visualizar_caceria_interactiva(self,
                                       posicion_inicial: int = 1,
                                       comportamiento_impala: ModoBehaviorImpala = ModoBehaviorImpala.ALEATORIO,
                                       usar_agente_entrenado: bool = False,
                                       delay: float = 0.5):
        """
        Visualiza una cacería de forma interactiva en terminal.
        
        Args:
            posicion_inicial: Posición inicial del león (1-8)
            comportamiento_impala: Comportamiento del impala
            usar_agente_entrenado: Si usar agente Q-Learning
            delay: Delay entre turnos en modo automático (segundos)
        """
        self._limpiar_pantalla()
        
        print("\n" + "="*70)
        print("VISUALIZACIÓN EN TERMINAL - GRID 19×19")
        print("="*70)
        
        # Inicializar cacería
        self.caceria.inicializar_caceria(posicion_inicial, comportamiento_impala)
        self.historia_leon = []
        
        print(f"\n🦁 León inicia en posición: {posicion_inicial}")
        print(f"🦌 Comportamiento impala: {comportamiento_impala.value}")
        print(f"🧠 Modo: {'Agente Entrenado' if usar_agente_entrenado else 'Manual'}")
        print(f"📏 Radio: {self.abrevadero.RADIO} cuadros")
        
        if not usar_agente_entrenado:
            print("\n📋 CONTROLES:")
            print("   • Enter = Avanzar (1 cuadro)")
            print("   • 2 = Esconderse")
            print("   • 3 = Atacar (2 cuadros)")
            print("   • q = Salir")
        
        input("\nPresiona Enter para comenzar...")
        
        turno = 0
        
        while self.caceria.resultado == ResultadoCaceria.EN_PROGRESO:
            turno += 1
            
            # Decidir acción del león
            if usar_agente_entrenado and self.agente_q:
                from simulation.verificador import Verificador
                from agents.leon import AccionLeon as AL
                from agents.impala import AccionImpala
                verificador = Verificador(self.abrevadero)
                
                # Crear objeto Estado correctamente (no usar dict)
                distancia = verificador.calcular_distancia_actual(self.caceria.leon)
                distancia_redondeada = round(distancia * 2) / 2
                
                # Determinar acción del impala
                accion_impala_str = "ver_frente"
                accion_impala_enum = AccionImpala.VER_FRENTE
                if self.caceria.impala.esta_huyendo:
                    accion_impala_str = "huir"
                    accion_impala_enum = AccionImpala.HUIR
                
                # Verificar si el impala puede ver al león
                impala_puede_ver = verificador.impala_puede_ver_leon(
                    self.caceria.leon, self.caceria.impala, accion_impala_enum
                )
                
                # Crear objeto Estado
                estado = Estado(
                    posicion_leon=self.caceria.leon.posicion,
                    distancia_impala=distancia_redondeada,
                    accion_impala=accion_impala_str,
                    leon_escondido=self.caceria.leon.esta_escondido,
                    impala_puede_ver=impala_puede_ver
                )
                
                acciones_posibles = [AL.AVANZAR.value, AL.ESCONDERSE.value, AL.ATACAR.value]
                accion_str, _ = self.agente_q.seleccionar_accion(estado, acciones_posibles, forzar_exploracion=False)
                # Convertir string a enum
                if accion_str == AL.AVANZAR.value:
                    accion_leon = AL.AVANZAR
                elif accion_str == AL.ESCONDERSE.value:
                    accion_leon = AL.ESCONDERSE
                else:
                    accion_leon = AL.ATACAR
            else:
                # Modo manual
                self._limpiar_pantalla()
                
                # Dibujar estado actual antes de pedir acción
                self._inicializar_grid()
                self._dibujar_vision_impala()
                self._dibujar_abrevadero()
                self._dibujar_trayectoria()
                self._dibujar_impala()
                self._dibujar_leon()
                self._dibujar_posiciones_iniciales()
                
                self._renderizar_grid()
                
                distancia = self._calcular_distancia_actual()
                distancia_grid = distancia * self.ESCALA
                print(f"\n📊 TURNO {turno}")
                print(f"   Distancia: {distancia_grid:.1f} celdas del grid 19×19 (≈{distancia:.2f} unidades)")
                print(f"   Posición león: {self.caceria.leon.posicion}")
                
                print("\n¿Qué debe hacer el león?")
                print("  Enter = Avanzar (1 cuadro)")
                print("  2 = Esconderse")
                print("  3 = Atacar (2 cuadros)")
                print("  q = Salir")
                
                opcion = input("\nAcción: ").strip().lower()
                
                if opcion == 'q':
                    print("\n👋 Simulación terminada por el usuario")
                    return
                elif opcion == '2':
                    accion_leon = AccionLeon.ESCONDERSE
                elif opcion == '3':
                    accion_leon = AccionLeon.ATACAR
                else:
                    accion_leon = AccionLeon.AVANZAR
            
            # Ejecutar turno
            terminada, mensaje = self.caceria.ejecutar_turno(accion_leon)
            
            # Obtener acciones del evento
            if self.caceria.tiempo.historia:
                ultimo_evento = self.caceria.tiempo.historia[-1]
                accion_impala_str = ultimo_evento.accion_impala
                accion_leon_str = ultimo_evento.accion_leon
            else:
                accion_impala_str = "N/A"
                accion_leon_str = accion_leon.value
            
            # Dibujar estado después de la acción
            self._limpiar_pantalla()
            self._inicializar_grid()
            self._dibujar_vision_impala()
            self._dibujar_abrevadero()
            self._dibujar_trayectoria()
            self._dibujar_impala()
            self._dibujar_leon()
            self._dibujar_posiciones_iniciales()
            
            self._renderizar_grid()
            self._mostrar_info_panel(turno, accion_impala_str, accion_leon_str)
            self._mostrar_leyenda()
            
            # Verificar si terminó
            if terminada:
                print("\n" + "="*70)
                if self.caceria.resultado == ResultadoCaceria.EXITO:
                    print("🎉 ¡CACERÍA EXITOSA! El león atrapó al impala")
                else:
                    print("❌ CACERÍA FALLIDA - El impala escapó")
                print("="*70)
                print(f"Turnos totales: {turno}")
                if self.caceria.resultado == ResultadoCaceria.EXITO:
                    print(f"Distancia final: 0.0 celdas (león alcanzó al impala)")
                else:
                    distancia_final = self._calcular_distancia_actual()
                    distancia_grid_final = distancia_final * self.ESCALA
                    print(f"Distancia final: {distancia_grid_final:.1f} celdas del grid (impala escapó)")
                
                # Preguntar si quiere repetir
                repetir = input("\n¿Intentar de nuevo con nueva posición aleatoria? (s/n, Enter=s): ").strip().lower()
                if repetir == '' or repetir == 's':
                    # Reiniciar con posición aleatoria del león
                    import random
                    nueva_posicion = random.randint(1, 8)
                    print(f"\n🎲 Nueva posición aleatoria del león: {nueva_posicion}")
                    self.visualizar_caceria_interactiva(
                        posicion_inicial=nueva_posicion,
                        comportamiento_impala=comportamiento_impala,
                        usar_agente_entrenado=usar_agente_entrenado,
                        delay=delay
                    )
                return
            
            # Pausa
            if usar_agente_entrenado:
                time.sleep(delay)
            else:
                input("\nPresiona Enter para continuar...")


def main():
    """Función principal para probar la interfaz."""
    from learning.q_learning import QLearning
    from learning.recompensas import SistemaRecompensas
    from knowledge.base_conocimientos import BaseConocimientos
    
    print("\n🎮 INTERFAZ VISUAL EN TERMINAL - GRID 19×19")
    print("="*70)
    
    # Detectar soporte de emojis
    usar_emojis = True
    try:
        print("🦁🦌 ¿Puedes ver estos emojis?")
        respuesta = input("(s/n, Enter=s): ").strip().lower()
        if respuesta == 'n':
            usar_emojis = False
    except:
        usar_emojis = False
    
    print("\n¿Qué modo deseas usar?")
    print("  1. Manual (tú decides las acciones del león)")
    print("  2. Agente entrenado (Q-Learning decide)")
    print("  3. Salir")
    
    opcion = input("\nElige opción (1-3): ").strip()
    
    if opcion == '3':
        return
    
    usar_agente = (opcion == '2')
    
    # Crear interfaz
    base_conocimientos = BaseConocimientos()
    agente_q = None
    
    if usar_agente:
        print("\n🧠 Cargando agente entrenado...")
        try:
            from storage.carga import cargar_conocimiento
            base_conocimientos = cargar_conocimiento()
            if base_conocimientos:
                print("✓ Base de conocimientos cargada")
            else:
                print("⚠️  No se encontró conocimiento previo, usando agente nuevo")
                print("⚠️  NOTA: El agente debe ser re-entrenado con RADIO=9.5")
        except Exception as e:
            print(f"⚠️  Error: {e}")
        
        sistema_recompensas = SistemaRecompensas()
        agente_q = QLearning(base_conocimientos, sistema_recompensas)
    
    interfaz = InterfazTerminalGrid(base_conocimientos, agente_q, usar_emojis)
    
    # Pedir posición inicial
    import random
    try:
        entrada = input("\n🦁 Posición inicial del león (1-8, Enter=aleatoria): ").strip()
        if entrada:
            posicion = int(entrada)
            posicion = max(1, min(8, posicion))
        else:
            posicion = random.randint(1, 8)
            print(f"   → Posición aleatoria seleccionada: {posicion}")
    except:
        posicion = random.randint(1, 8)
        print(f"   → Posición aleatoria seleccionada: {posicion}")
    
    # Delay para modo automático
    delay = 1.0
    if usar_agente:
        try:
            delay = float(input("⏱️  Delay entre turnos en segundos (Enter=1.0): ").strip() or "1.0")
        except:
            delay = 1.0
    
    # Visualizar
    try:
        interfaz.visualizar_caceria_interactiva(
            posicion_inicial=posicion,
            usar_agente_entrenado=usar_agente,
            delay=delay
        )
    except KeyboardInterrupt:
        print("\n\n👋 Visualización interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
