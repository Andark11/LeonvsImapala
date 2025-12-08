"""
Interfaz visual moderna con grid 19×19 para visualización de cacerías.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np
from typing import Optional, List, Tuple
import math

from environment import Abrevadero, Direccion
from simulation.caceria import Caceria, ModoBehaviorImpala, ResultadoCaceria
from agents.leon import AccionLeon
from knowledge.base_conocimientos import BaseConocimientos, Estado
from learning.q_learning import QLearning


class InterfazVisualGrid:
    """
    Interfaz visual con grid 19×19 para mostrar cacerías paso a paso.
    """
    
    # Constantes del grid
    GRID_SIZE = 19
    ESCALA = 1.9  # Factor de escala: 5 cuadros polares = 9.5 cuadros grid
    
    # Colores
    COLOR_GRID = '#E8E8E8'
    COLOR_ABREVADERO = '#1E88E5'
    COLOR_LEON = '#FF6B35'
    COLOR_LEON_ESCONDIDO = '#A0A0A0'
    COLOR_LEON_ATACANDO = '#D32F2F'
    COLOR_IMPALA = '#4CAF50'
    COLOR_IMPALA_HUYENDO = '#FFC107'
    COLOR_TRAYECTORIA = '#FF9800'
    COLOR_VISION = '#FF5252'
    COLOR_POSICIONES = '#BDBDBD'
    
    def __init__(self, base_conocimientos: Optional[BaseConocimientos] = None,
                 agente_q: Optional[QLearning] = None):
        """
        Inicializa la interfaz visual.
        
        Args:
            base_conocimientos: Base de conocimientos del león
            agente_q: Agente de Q-Learning para mostrar decisiones
        """
        self.abrevadero = Abrevadero()
        self.caceria = Caceria(self.abrevadero)
        self.base_conocimientos = base_conocimientos
        self.agente_q = agente_q
        
        # Historia de posiciones para trayectoria
        self.historia_leon: List[Tuple[float, float]] = []
        self.historia_acciones: List[Tuple[str, str]] = []  # (accion_impala, accion_leon)
        
        # Figura de matplotlib
        self.fig = None
        self.ax = None
    
    def _coord_polar_a_grid(self, x_polar: float, y_polar: float) -> Tuple[float, float]:
        """
        Convierte coordenadas polares a posición en el grid 19×19.
        
        Args:
            x_polar: Coordenada X polar
            y_polar: Coordenada Y polar
            
        Returns:
            (col, fila) en el grid
        """
        centro = self.GRID_SIZE / 2
        col = centro + (x_polar * self.ESCALA)
        fila = centro - (y_polar * self.ESCALA)  # Y invertido para grid
        return col, fila
    
    def _dibujar_grid_base(self):
        """
        Dibuja el grid base 19×19 con el abrevadero.
        """
        self.ax.clear()
        
        # Configurar límites y aspecto
        self.ax.set_xlim(0, self.GRID_SIZE)
        self.ax.set_ylim(0, self.GRID_SIZE)
        self.ax.set_aspect('equal')
        
        # Dibujar grid
        for i in range(self.GRID_SIZE + 1):
            self.ax.plot([0, self.GRID_SIZE], [i, i], color=self.COLOR_GRID, 
                        linewidth=0.5, alpha=0.6)
            self.ax.plot([i, i], [0, self.GRID_SIZE], color=self.COLOR_GRID, 
                        linewidth=0.5, alpha=0.6)
        
        # Centro del grid
        centro = self.GRID_SIZE / 2
        
        # Dibujar abrevadero (rectángulo en el centro)
        abrev_width = 3.8  # 2 * ESCALA
        abrev_height = 1.9  # 1 * ESCALA
        abrevadero_rect = patches.Rectangle(
            (centro - abrev_width/2, centro - abrev_height/2),
            abrev_width, abrev_height,
            linewidth=2, edgecolor=self.COLOR_ABREVADERO, 
            facecolor=self.COLOR_ABREVADERO, alpha=0.7, zorder=5
        )
        self.ax.add_patch(abrevadero_rect)
        
        # Etiqueta del abrevadero
        self.ax.text(centro, centro, 'ABREVADERO', 
                    ha='center', va='center', color='white',
                    fontsize=8, weight='bold', zorder=6)
        
        # Dibujar las 8 posiciones iniciales
        for pos in range(1, 9):
            x_polar, y_polar = self.abrevadero.obtener_coordenadas(pos)
            col, fila = self._coord_polar_a_grid(x_polar, y_polar)
            
            # Círculo de posición
            circulo = plt.Circle((col, fila), 0.4, 
                                color=self.COLOR_POSICIONES, alpha=0.3, zorder=3)
            self.ax.add_patch(circulo)
            
            # Número de posición
            self.ax.text(col, fila, str(pos), ha='center', va='center',
                        fontsize=9, color='gray', alpha=0.6, zorder=4)
        
        # Invertir eje Y para que coincida con convención de grid
        self.ax.invert_yaxis()
        
        # Quitar ticks para limpieza visual
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Bordes del grid
        self.ax.spines['top'].set_visible(True)
        self.ax.spines['right'].set_visible(True)
        self.ax.spines['bottom'].set_visible(True)
        self.ax.spines['left'].set_visible(True)
    
    def _dibujar_vision_impala(self, direccion: Direccion):
        """
        Dibuja el cono de visión del impala.
        
        Args:
            direccion: Dirección hacia donde mira el impala
        """
        centro = self.GRID_SIZE / 2
        
        # Ángulo de visión: 120° total (60° a cada lado)
        angulo_central = direccion.value
        angulo_izq = angulo_central - 60
        angulo_der = angulo_central + 60
        
        # Longitud del cono (hasta el borde del grid)
        longitud = self.GRID_SIZE / 2
        
        # Calcular puntos del cono
        puntos = [(centro, centro)]  # Centro
        
        # Arco del cono
        for angulo in np.linspace(angulo_izq, angulo_der, 30):
            rad = math.radians(angulo)
            # Nota: En grid, Y está invertido
            col = centro + longitud * math.sin(rad)
            fila = centro - longitud * math.cos(rad)
            puntos.append((col, fila))
        
        puntos.append((centro, centro))  # Cerrar
        
        # Dibujar cono de visión
        poligono = patches.Polygon(puntos, alpha=0.15, 
                                   facecolor=self.COLOR_VISION,
                                   edgecolor=self.COLOR_VISION,
                                   linewidth=1.5, linestyle='--', zorder=2)
        self.ax.add_patch(poligono)
        
        # Línea central de visión
        rad = math.radians(angulo_central)
        col_fin = centro + longitud * math.sin(rad)
        fila_fin = centro - longitud * math.cos(rad)
        self.ax.plot([centro, col_fin], [centro, fila_fin],
                    color=self.COLOR_VISION, linewidth=2, alpha=0.5,
                    linestyle='--', zorder=2)
    
    def _dibujar_impala(self, huyendo: bool = False):
        """
        Dibuja el impala en su posición actual.
        
        Args:
            huyendo: Si el impala está huyendo
        """
        centro = self.GRID_SIZE / 2
        
        # Calcular posición del impala
        if huyendo and self.caceria.impala.direccion_huida:
            # Calcular desplazamiento basado en tiempo y velocidad de huida
            tiempo_huyendo = self.caceria.impala.tiempo_huyendo
            velocidad = self.caceria.impala.velocidad_huida
            distancia_total = tiempo_huyendo * velocidad
            
            # Convertir a coordenadas del grid
            if self.caceria.impala.direccion_huida.value == 90:  # ESTE
                x_impala = centro + (distancia_total * self.ESCALA)
                y_impala = centro
            else:  # OESTE (270)
                x_impala = centro - (distancia_total * self.ESCALA)
                y_impala = centro
        else:
            # En el centro del abrevadero
            x_impala = centro
            y_impala = centro
        
        color = self.COLOR_IMPALA_HUYENDO if huyendo else self.COLOR_IMPALA
        
        # Círculo del impala
        circulo = plt.Circle((x_impala, y_impala), 0.6, 
                            color=color, alpha=0.8, zorder=10,
                            edgecolor='black', linewidth=2)
        self.ax.add_patch(circulo)
        
        # Símbolo
        simbolo = '💨' if huyendo else '🦌'
        self.ax.text(x_impala, y_impala, simbolo, ha='center', va='center',
                    fontsize=20, zorder=11)
        
        # Etiqueta de estado
        if huyendo:
            self.ax.text(centro, centro + 1.5, 'HUYENDO!',
                        ha='center', va='center', color=self.COLOR_IMPALA_HUYENDO,
                        fontsize=10, weight='bold',
                        bbox=dict(boxstyle='round', facecolor='white', 
                                 edgecolor=self.COLOR_IMPALA_HUYENDO, linewidth=2),
                        zorder=12)
    
    def _dibujar_leon(self, escondido: bool = False, atacando: bool = False):
        """
        Dibuja el león en su posición actual.
        
        Args:
            escondido: Si el león está escondido
            atacando: Si el león está atacando
        """
        # Obtener posición actual del león
        if self.caceria.leon.posicion_exacta:
            x_polar, y_polar = self.caceria.leon.posicion_exacta
        else:
            x_polar, y_polar = self.abrevadero.obtener_coordenadas(
                self.caceria.leon.posicion
            )
        
        col, fila = self._coord_polar_a_grid(x_polar, y_polar)
        
        # Agregar a historia
        self.historia_leon.append((col, fila))
        
        # Determinar color y tamaño
        if atacando:
            color = self.COLOR_LEON_ATACANDO
            radio = 0.8
            simbolo = '🦁⚡'
        elif escondido:
            color = self.COLOR_LEON_ESCONDIDO
            radio = 0.5
            simbolo = '🦁💤'
        else:
            color = self.COLOR_LEON
            radio = 0.6
            simbolo = '🦁'
        
        # Círculo del león
        circulo = plt.Circle((col, fila), radio,
                            color=color, alpha=0.9 if not escondido else 0.5,
                            zorder=10, edgecolor='black', linewidth=2)
        self.ax.add_patch(circulo)
        
        # Símbolo
        self.ax.text(col, fila, simbolo, ha='center', va='center',
                    fontsize=18 if not atacando else 20, zorder=11)
        
        # Etiqueta de estado
        if atacando:
            self.ax.text(col, fila - 1.5, 'ATACANDO!',
                        ha='center', va='center', color=self.COLOR_LEON_ATACANDO,
                        fontsize=10, weight='bold',
                        bbox=dict(boxstyle='round', facecolor='white',
                                 edgecolor=self.COLOR_LEON_ATACANDO, linewidth=2),
                        zorder=12)
        elif escondido:
            self.ax.text(col, fila - 1.2, 'Escondido',
                        ha='center', va='center', color=self.COLOR_LEON_ESCONDIDO,
                        fontsize=9, style='italic',
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.7),
                        zorder=12)
        
        # Mostrar posición discreta
        self.ax.text(col, fila + 1.8, f'Pos {self.caceria.leon.posicion}',
                    ha='center', va='center', fontsize=8,
                    bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8),
                    zorder=12)
    
    def _dibujar_trayectoria(self):
        """
        Dibuja la trayectoria completa del león.
        """
        if len(self.historia_leon) > 1:
            cols = [pos[0] for pos in self.historia_leon]
            filas = [pos[1] for pos in self.historia_leon]
            
            # Línea de trayectoria
            self.ax.plot(cols, filas, color=self.COLOR_TRAYECTORIA,
                        linewidth=2, alpha=0.6, linestyle='--',
                        marker='o', markersize=4, zorder=7)
    
    def _calcular_distancia_actual(self) -> float:
        """
        Calcula la distancia actual león-impala.
        
        Returns:
            Distancia en cuadros polares
        """
        if self.caceria.leon.posicion_exacta:
            x, y = self.caceria.leon.posicion_exacta
        else:
            x, y = self.abrevadero.obtener_coordenadas(self.caceria.leon.posicion)
        
        return math.sqrt(x**2 + y**2)
    
    def _dibujar_info_panel(self, turno: int, accion_impala: str, accion_leon: str):
        """
        Dibuja panel de información del turno.
        
        Args:
            turno: Número de turno
            accion_impala: Acción del impala
            accion_leon: Acción del león
        """
        # Panel de información en la parte superior
        info_text = f'TURNO {turno}\n'
        info_text += f'━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
        info_text += f'Impala: {accion_impala}\n'
        info_text += f'León: {accion_leon}\n'
        
        # Distancia
        distancia = self._calcular_distancia_actual()
        info_text += f'Distancia: {distancia:.2f} cuadros'
        
        # Estado del león
        estados = []
        if self.caceria.leon.esta_escondido:
            estados.append('ESCONDIDO')
        if self.caceria.leon.esta_atacando:
            estados.append('ATACANDO')
        
        if estados:
            info_text += f'\nEstado León: {", ".join(estados)}'
        
        # Estado del impala
        if self.caceria.impala.esta_huyendo:
            info_text += f'\nEstado Impala: HUYENDO (velocidad {self.caceria.impala.velocidad_huida})'
        
        self.ax.text(0.5, 1.08, info_text,
                    transform=self.ax.transAxes,
                    ha='center', va='top',
                    fontsize=10, family='monospace',
                    bbox=dict(boxstyle='round', facecolor='lightblue', 
                             alpha=0.9, edgecolor='blue', linewidth=2))
    
    def _dibujar_q_values(self):
        """
        Dibuja los Q-values si hay agente disponible.
        """
        if not self.agente_q:
            return
        
        # Obtener estado actual
        from simulation.verificador import Verificador
        verificador = Verificador(self.abrevadero)
        estado = verificador.obtener_estado_mundo(
            self.caceria.leon, self.caceria.impala
        )
        
        # Obtener Q-values
        estado_str = str(estado)
        if estado_str in self.agente_q.q_table:
            q_values = self.agente_q.q_table[estado_str]
            
            # Panel de Q-values
            q_text = 'Q-VALUES\n━━━━━━━━━━\n'
            acciones_nombres = {
                AccionLeon.AVANZAR: 'Avanzar',
                AccionLeon.ESCONDERSE: 'Esconderse',
                AccionLeon.ATACAR: 'Atacar'
            }
            
            for accion, valor in q_values.items():
                nombre = acciones_nombres.get(accion, str(accion))
                q_text += f'{nombre}: {valor:.2f}\n'
            
            self.ax.text(1.02, 0.5, q_text,
                        transform=self.ax.transAxes,
                        ha='left', va='center',
                        fontsize=9, family='monospace',
                        bbox=dict(boxstyle='round', facecolor='lightyellow',
                                 alpha=0.9, edgecolor='orange', linewidth=2))
    
    def visualizar_caceria_interactiva(self, 
                                       posicion_inicial: int = 1,
                                       comportamiento_impala: ModoBehaviorImpala = ModoBehaviorImpala.ALEATORIO,
                                       usar_agente_entrenado: bool = False):
        """
        Visualiza una cacería de forma interactiva paso a paso.
        
        Args:
            posicion_inicial: Posición inicial del león
            comportamiento_impala: Comportamiento del impala
            usar_agente_entrenado: Si usar el agente Q-Learning para decisiones
        """
        print("\n" + "="*70)
        print("VISUALIZACIÓN INTERACTIVA - GRID 19×19")
        print("="*70)
        
        # Inicializar cacería
        self.caceria.inicializar_caceria(posicion_inicial, comportamiento_impala)
        self.historia_leon = []
        self.historia_acciones = []
        
        print(f"\n🦁 León inicia en posición: {posicion_inicial}")
        print(f"🦌 Comportamiento impala: {comportamiento_impala.value}")
        print(f"🧠 Modo: {'Agente Entrenado' if usar_agente_entrenado else 'Manual'}")
        
        print("\n📋 INSTRUCCIONES:")
        print("   • Presiona Enter para avanzar cada turno")
        print("   • Escribe 'q' para terminar")
        print("   • Escribe 's' para guardar imagen actual")
        
        input("\nPresiona Enter para comenzar...")
        
        # Crear figura
        self.fig, self.ax = plt.subplots(figsize=(12, 12))
        self.fig.canvas.manager.set_window_title('León vs Impala - Simulación')
        
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
                # Modo manual: preguntar al usuario
                print(f"\n{'='*70}")
                print(f"TURNO {turno}")
                print(f"{'='*70}")
                print(f"Distancia actual: {self._calcular_distancia_actual():.2f} cuadros")
                print("\n¿Qué debe hacer el león?")
                print("  1. Avanzar (1 cuadro)")
                print("  2. Esconderse")
                print("  3. Atacar (2 cuadros)")
                
                while True:
                    opcion = input("\nElige opción (1-3, o Enter para avanzar): ").strip()
                    if opcion == '' or opcion == '1':
                        accion_leon = AccionLeon.AVANZAR
                        break
                    elif opcion == '2':
                        accion_leon = AccionLeon.ESCONDERSE
                        break
                    elif opcion == '3':
                        accion_leon = AccionLeon.ATACAR
                        break
                    elif opcion.lower() == 'q':
                        print("\n👋 Simulación terminada por el usuario")
                        plt.close()
                        return
                    elif opcion.lower() == 's':
                        self.fig.savefig(f'caceria_turno_{turno-1}.png', 
                                        dpi=150, bbox_inches='tight')
                        print(f"✓ Imagen guardada: caceria_turno_{turno-1}.png")
                    else:
                        print("❌ Opción inválida")
            
            # Ejecutar turno
            terminada, mensaje = self.caceria.ejecutar_turno(accion_leon)
            
            # Obtener acciones realizadas del último evento
            if self.caceria.tiempo.historia:
                ultimo_evento = self.caceria.tiempo.historia[-1]
                accion_impala_str = ultimo_evento.accion_impala
                accion_leon_str = ultimo_evento.accion_leon
            else:
                accion_impala_str = "N/A"
                accion_leon_str = accion_leon.value
            
            self.historia_acciones.append((accion_impala_str, accion_leon_str))
            
            # Dibujar estado actual
            self._dibujar_grid_base()
            self._dibujar_vision_impala(self.caceria.impala.direccion_vista)
            self._dibujar_trayectoria()
            self._dibujar_impala(self.caceria.impala.esta_huyendo)
            self._dibujar_leon(
                self.caceria.leon.esta_escondido,
                self.caceria.leon.esta_atacando
            )
            self._dibujar_info_panel(turno, accion_impala_str, accion_leon_str)
            
            if usar_agente_entrenado:
                self._dibujar_q_values()
            
            # Mostrar
            plt.draw()
            plt.pause(0.1)
            
            # Verificar si terminó
            if terminada:
                # Dibujar mensaje final
                if self.caceria.resultado == ResultadoCaceria.EXITO:
                    mensaje_final = '🎉 ¡CACERÍA EXITOSA!'
                    color_final = 'green'
                else:
                    mensaje_final = '❌ CACERÍA FALLIDA'
                    color_final = 'red'
                
                self.ax.text(0.5, 0.5, mensaje_final,
                            transform=self.ax.transAxes,
                            ha='center', va='center',
                            fontsize=24, weight='bold',
                            color=color_final,
                            bbox=dict(boxstyle='round', facecolor='white',
                                     edgecolor=color_final, linewidth=4,
                                     pad=1),
                            zorder=20)
                
                plt.draw()
                
                print(f"\n{'='*70}")
                print(mensaje_final)
                print(f"{'='*70}")
                print(f"Turnos totales: {turno}")
                print(f"Distancia final: {self._calcular_distancia_actual():.2f} cuadros")
                
                # Guardar imagen final
                self.fig.savefig(f'caceria_final_turno_{turno}.png',
                                dpi=150, bbox_inches='tight')
                print(f"\n✓ Imagen final guardada: caceria_final_turno_{turno}.png")
                
                input("\nPresiona Enter para cerrar...")
                plt.close()
                break
            
            # Pausar para siguiente turno
            if not usar_agente_entrenado:
                respuesta = input("\nPresiona Enter para continuar (q=salir, s=guardar): ").strip()
                if respuesta.lower() == 'q':
                    print("\n👋 Simulación terminada por el usuario")
                    plt.close()
                    break
                elif respuesta.lower() == 's':
                    self.fig.savefig(f'caceria_turno_{turno}.png',
                                    dpi=150, bbox_inches='tight')
                    print(f"✓ Imagen guardada: caceria_turno_{turno}.png")


def main():
    """
    Función principal para probar la interfaz.
    """
    from learning.q_learning import QLearning
    from learning.recompensas import SistemaRecompensas
    from knowledge.base_conocimientos import BaseConocimientos
    
    print("\n🎮 INTERFAZ VISUAL GRID 19×19")
    print("="*70)
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
            print("✓ Base de conocimientos cargada")
        except:
            print("⚠️  No se pudo cargar conocimiento previo, usando agente nuevo")
        
        sistema_recompensas = SistemaRecompensas()
        agente_q = QLearning(base_conocimientos, sistema_recompensas)
    
    interfaz = InterfazVisualGrid(base_conocimientos, agente_q)
    
    # Pedir posición inicial
    print("\n🦁 ¿En qué posición debe iniciar el león? (1-8, Enter=1): ", end='')
    pos_input = input().strip()
    posicion = int(pos_input) if pos_input and pos_input.isdigit() else 1
    posicion = max(1, min(8, posicion))
    
    # Visualizar
    interfaz.visualizar_caceria_interactiva(
        posicion_inicial=posicion,
        comportamiento_impala=ModoBehaviorImpala.ALEATORIO,
        usar_agente_entrenado=usar_agente
    )


if __name__ == "__main__":
    main()
