"""
Módulo de cacería.
Orquesta una incursión completa de cacería del león.
"""

from enum import Enum
from typing import List, Optional, Tuple
import random

from environment import Abrevadero, Direccion
from agents.leon import Leon, AccionLeon
from agents.impala import Impala, AccionImpala
from simulation.tiempo import TiempoSimulacion
from simulation.verificador import Verificador, CondicionHuida


class ResultadoCaceria(Enum):
    """Resultados posibles de una incursión de cacería"""
    EXITO = "exito"
    FRACASO = "fracaso"
    EN_PROGRESO = "en_progreso"


class ModoBehaviorImpala(Enum):
    """Modos de comportamiento del impala durante entrenamiento"""
    ALEATORIO = "aleatorio"
    PROGRAMADO = "programado"


class Caceria:
    """
    Orquesta una incursión completa de cacería.
    Coordina las acciones del león e impala, y determina el resultado.
    """
    
    # Máximo de unidades de tiempo para una cacería
    MAX_TIEMPO = 50
    
    def __init__(self, abrevadero: Abrevadero):
        """
        Inicializa una cacería.
        
        Args:
            abrevadero: Instancia del abrevadero
        """
        self.abrevadero = abrevadero
        self.tiempo = TiempoSimulacion()
        self.verificador = Verificador(abrevadero)
        
        self.leon = Leon()
        self.impala = Impala()
        
        self.resultado: ResultadoCaceria = ResultadoCaceria.EN_PROGRESO
        self.razon_finalizacion: str = ""
    
    def inicializar_caceria(self, posicion_inicial_leon: int,
                           comportamiento_impala: ModoBehaviorImpala = ModoBehaviorImpala.ALEATORIO,
                           secuencia_impala: Optional[List[AccionImpala]] = None):
        """
        Inicializa una nueva cacería.
        
        Args:
            posicion_inicial_leon: Posición inicial del león (1-8)
            comportamiento_impala: Modo de comportamiento del impala
            secuencia_impala: Secuencia programada de acciones (si modo PROGRAMADO)
        """
        # Resetear estados
        self.tiempo.resetear()
        self.leon.resetear(posicion_inicial_leon)
        self.impala.resetear()
        
        self.resultado = ResultadoCaceria.EN_PROGRESO
        self.razon_finalizacion = ""
        
        # Configurar comportamiento del impala
        self.comportamiento_impala = comportamiento_impala
        
        if comportamiento_impala == ModoBehaviorImpala.PROGRAMADO:
            if not secuencia_impala:
                raise ValueError("Modo PROGRAMADO requiere secuencia_impala")
            self.secuencia_impala = secuencia_impala
            self.indice_secuencia = 0
        else:
            self.secuencia_impala = None
            self.indice_secuencia = 0
    
    def ejecutar_turno(self, accion_leon: AccionLeon) -> Tuple[bool, str]:
        """
        Ejecuta un turno completo de la cacería.
        
        Args:
            accion_leon: Acción que ejecutará el león
            
        Returns:
            Tupla (caceria_terminada, mensaje)
        """
        if self.resultado != ResultadoCaceria.EN_PROGRESO:
            return True, self.razon_finalizacion
        
        # Avanzar tiempo
        self.tiempo.avanzar_tiempo()
        
        # 1. IMPALA ACTÚA PRIMERO
        accion_impala = self._obtener_accion_impala()
        desc_impala = self.impala.ejecutar_accion(accion_impala)
        
        # 2. LEÓN REACCIONA
        desc_leon = self.leon.ejecutar_accion(accion_leon)
        
        # Actualizar posición exacta del león si avanzó
        if accion_leon == AccionLeon.AVANZAR:
            nueva_pos = self.abrevadero.calcular_nueva_posicion_avance(self.leon.posicion)
            self.leon.actualizar_posicion_exacta(nueva_pos)
        
        # 3. VERIFICAR CONDICIONES DEL MUNDO
        resultado_verificacion = self._verificar_mundo(accion_impala)
        
        # 4. REGISTRAR EVENTO
        estado_mundo = self.verificador.obtener_estado_mundo(self.leon, self.impala)
        self.tiempo.registrar_evento(desc_impala, desc_leon, resultado_verificacion, estado_mundo)
        
        # 5. VERIFICAR FIN DE CACERÍA
        terminada, mensaje = self._verificar_fin_caceria()
        
        return terminada, mensaje
    
    def _obtener_accion_impala(self) -> AccionImpala:
        """
        Obtiene la siguiente acción del impala según su modo de comportamiento.
        
        Returns:
            Acción que ejecutará el impala
        """
        # Si está huyendo, continúa huyendo
        if self.impala.esta_huyendo:
            return AccionImpala.HUIR
        
        # Modo aleatorio
        if self.comportamiento_impala == ModoBehaviorImpala.ALEATORIO:
            acciones_posibles = [
                AccionImpala.VER_IZQUIERDA,
                AccionImpala.VER_DERECHA,
                AccionImpala.VER_FRENTE,
                AccionImpala.BEBER_AGUA
            ]
            return random.choice(acciones_posibles)
        
        # Modo programado
        else:
            accion = self.secuencia_impala[self.indice_secuencia]
            self.indice_secuencia = (self.indice_secuencia + 1) % len(self.secuencia_impala)
            return accion
    
    def _verificar_mundo(self, ultima_accion_impala: AccionImpala) -> str:
        """
        Verifica las condiciones del mundo y actualiza estados.
        
        Args:
            ultima_accion_impala: Última acción ejecutada por el impala
            
        Returns:
            Descripción del resultado de la verificación
        """
        # Verificar si el impala debe huir
        debe_huir, condicion = self.verificador.verificar_condicion_huida(
            self.leon, self.impala, ultima_accion_impala
        )
        
        if debe_huir and not self.impala.esta_huyendo:
            # Forzar huida del impala
            self.impala.ejecutar_accion(AccionImpala.HUIR)
            
            razones = {
                CondicionHuida.LEON_VISIBLE: "¡Impala detecta al león! Inicia huida",
                CondicionHuida.LEON_ATACA: "¡León inicia ataque! Impala huye",
                CondicionHuida.DISTANCIA_MINIMA: "¡León muy cerca! Impala huye por instinto"
            }
            return razones.get(condicion, "Impala huye")
        
        # Verificar distancia actual
        distancia = self.verificador.calcular_distancia_actual(self.leon)
        
        if self.leon.esta_atacando:
            return f"León atacando (distancia: {distancia:.2f} cuadros)"
        elif self.leon.esta_escondido:
            return f"León escondido (distancia: {distancia:.2f} cuadros)"
        else:
            return f"León avanzando (distancia: {distancia:.2f} cuadros)"
    
    def _verificar_fin_caceria(self) -> Tuple[bool, str]:
        """
        Verifica si la cacería ha terminado.
        
        Returns:
            Tupla (terminada, mensaje)
        """
        # Verificar éxito
        if self.verificador.verificar_exito_caceria(self.leon, self.impala):
            self.resultado = ResultadoCaceria.EXITO
            self.razon_finalizacion = "¡ÉXITO! El león atrapó al impala"
            return True, self.razon_finalizacion
        
        # Verificar fracaso
        if self.verificador.verificar_fracaso_caceria(self.leon, self.impala):
            self.resultado = ResultadoCaceria.FRACASO
            self.razon_finalizacion = "FRACASO: El impala escapó (velocidad de huida > velocidad león)"
            return True, self.razon_finalizacion
        
        # Verificar timeout
        if self.tiempo.obtener_tiempo_actual() >= self.MAX_TIEMPO:
            self.resultado = ResultadoCaceria.FRACASO
            self.razon_finalizacion = f"FRACASO: Tiempo máximo alcanzado (T={self.MAX_TIEMPO})"
            return True, self.razon_finalizacion
        
        return False, "Cacería en progreso"
    
    def ejecutar_caceria_completa(self, posicion_inicial_leon: int,
                                  estrategia_leon: callable,
                                  comportamiento_impala: ModoBehaviorImpala = ModoBehaviorImpala.ALEATORIO,
                                  secuencia_impala: Optional[List[AccionImpala]] = None,
                                  verbose: bool = False) -> ResultadoCaceria:
        """
        Ejecuta una cacería completa usando una estrategia del león.
        
        Args:
            posicion_inicial_leon: Posición inicial del león
            estrategia_leon: Función que decide la acción del león
                             Firma: (leon, impala, estado_mundo) -> AccionLeon
            comportamiento_impala: Modo de comportamiento del impala
            secuencia_impala: Secuencia programada (si modo PROGRAMADO)
            verbose: Si True, imprime información de cada turno
            
        Returns:
            Resultado de la cacería
        """
        self.inicializar_caceria(posicion_inicial_leon, comportamiento_impala, secuencia_impala)
        
        while self.resultado == ResultadoCaceria.EN_PROGRESO:
            # Obtener estado actual
            estado_mundo = self.verificador.obtener_estado_mundo(self.leon, self.impala)
            
            # Decidir acción del león usando la estrategia
            accion_leon = estrategia_leon(self.leon, self.impala, estado_mundo)
            
            # Ejecutar turno
            terminada, mensaje = self.ejecutar_turno(accion_leon)
            
            if verbose and terminada:
                print(f"T={self.tiempo.obtener_tiempo_actual()}: {mensaje}")
        
        return self.resultado
    
    def obtener_resumen(self) -> dict:
        """
        Obtiene un resumen completo de la cacería.
        
        Returns:
            Diccionario con información de la cacería
        """
        return {
            'resultado': self.resultado.value,
            'razon': self.razon_finalizacion,
            'duracion': self.tiempo.obtener_tiempo_actual(),
            'posicion_inicial_leon': self.leon.posicion,
            'historia': self.tiempo.obtener_historia()
        }
    
    def generar_reporte_detallado(self) -> str:
        """
        Genera un reporte textual detallado de la cacería.
        
        Returns:
            String con el reporte completo
        """
        lineas = [
            "=" * 60,
            "REPORTE DE CACERÍA",
            "=" * 60,
            f"Resultado: {self.resultado.value.upper()}",
            f"Razón: {self.razon_finalizacion}",
            f"Duración: {self.tiempo.obtener_tiempo_actual()} unidades de tiempo",
            f"Posición inicial león: {self.leon.posicion}",
            "",
            "--- Historial de Eventos ---",
            ""
        ]
        
        lineas.append(self.tiempo.generar_resumen())
        
        return "\n".join(lineas)


if __name__ == "__main__":
    # Pruebas básicas
    print("=== Pruebas de Cacería ===\n")
    
    abrevadero = Abrevadero()
    caceria = Caceria(abrevadero)
    
    # Estrategia simple: siempre avanzar hasta estar cerca, luego atacar
    def estrategia_simple(leon, impala, estado_mundo):
        if estado_mundo['distancia_leon_impala'] < 2:
            return AccionLeon.ATACAR
        else:
            return AccionLeon.AVANZAR
    
    # Ejecutar una cacería
    print("Ejecutando cacería desde posición 5...")
    resultado = caceria.ejecutar_caceria_completa(
        posicion_inicial_leon=5,
        estrategia_leon=estrategia_simple,
        comportamiento_impala=ModoBehaviorImpala.ALEATORIO,
        verbose=False
    )
    
    print(f"\nResultado: {resultado.value}")
    print(f"\n{caceria.generar_reporte_detallado()}")
