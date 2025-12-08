"""
Módulo de sistema de recompensas.
Define las recompensas y penalizaciones para el aprendizaje.
"""

from typing import Dict


class SistemaRecompensas:
    """
    Sistema de recompensas para el aprendizaje del león.
    Define los incentivos que guían el aprendizaje.
    """
    
    # Recompensas principales
    EXITO_CACERIA = 100.0       # León captura al impala
    FRACASO_CACERIA = -50.0     # Impala escapa
    
    # Recompensas parciales
    ACERCAMIENTO = 1.0          # León se acerca al impala
    ALEJAMIENTO = -2.0          # León se aleja del impala
    DETECCION_TEMPRANA = -5.0   # Impala detecta al león demasiado pronto
    
    # Penalizaciones de tiempo
    TIEMPO_EXCESIVO = -0.1      # Penalización por cada turno (incentiva eficiencia)
    
    # Bonos estratégicos
    BUEN_USO_ESCONDERSE = 2.0   # Se esconde cuando impala puede verlo
    MAL_USO_ESCONDERSE = -1.0   # Se esconde innecesariamente
    ATAQUE_CERCANO = 5.0        # Ataca cuando está cerca
    ATAQUE_LEJANO = -3.0        # Ataca estando lejos
    
    def __init__(self):
        """Inicializa el sistema de recompensas"""
        self.configuracion = {
            'exito': self.EXITO_CACERIA,
            'fracaso': self.FRACASO_CACERIA,
            'acercamiento': self.ACERCAMIENTO,
            'alejamiento': self.ALEJAMIENTO,
            'deteccion': self.DETECCION_TEMPRANA,
            'tiempo': self.TIEMPO_EXCESIVO
        }
    
    def calcular_recompensa_final(self, exito: bool) -> float:
        """
        Calcula la recompensa al final de una cacería.
        
        Args:
            exito: Si la cacería fue exitosa
            
        Returns:
            Recompensa final
        """
        return self.EXITO_CACERIA if exito else self.FRACASO_CACERIA
    
    def calcular_recompensa_acercamiento(self, distancia_anterior: float,
                                         distancia_nueva: float) -> float:
        """
        Calcula la recompensa por cambio en la distancia.
        
        Args:
            distancia_anterior: Distancia en el turno anterior
            distancia_nueva: Distancia en el turno actual
            
        Returns:
            Recompensa por acercamiento/alejamiento
        """
        diferencia = distancia_anterior - distancia_nueva
        
        if diferencia > 0:  # Se acercó
            # Recompensa proporcional al acercamiento
            return self.ACERCAMIENTO * diferencia
        elif diferencia < 0:  # Se alejó
            # Penalización proporcional al alejamiento
            return self.ALEJAMIENTO * abs(diferencia)
        else:
            return 0.0
    
    def calcular_recompensa_deteccion(self, impala_huye: bool,
                                     distancia_actual: float) -> float:
        """
        Calcula la penalización por detección temprana.
        
        Args:
            impala_huye: Si el impala inició la huida
            distancia_actual: Distancia actual al impala
            
        Returns:
            Penalización por detección (negativa o 0)
        """
        if not impala_huye:
            return 0.0
        
        # Mayor penalización si detectado estando lejos
        if distancia_actual > 4:
            return self.DETECCION_TEMPRANA * 2
        elif distancia_actual > 3:
            return self.DETECCION_TEMPRANA
        else:
            return 0.0  # No penalizar si ya está cerca
    
    def calcular_recompensa_accion(self, accion: str, distancia: float,
                                  leon_escondido: bool,
                                  impala_puede_ver: bool) -> float:
        """
        Calcula la recompensa por una acción específica.
        
        Args:
            accion: Acción ejecutada por el león
            distancia: Distancia actual al impala
            leon_escondido: Si el león está escondido
            impala_puede_ver: Si el impala puede ver al león
            
        Returns:
            Recompensa por la acción
        """
        recompensa = 0.0
        
        # Evaluar uso de "esconderse"
        if accion == "esconderse":
            if impala_puede_ver and not leon_escondido:
                # Buen uso: se esconde cuando puede ser visto
                recompensa += self.BUEN_USO_ESCONDERSE
            elif not impala_puede_ver:
                # Mal uso: se esconde cuando no es necesario
                recompensa += self.MAL_USO_ESCONDERSE
        
        # Evaluar uso de "atacar"
        elif accion == "atacar":
            if distancia < 2:
                # Buen uso: ataca cuando está cerca
                recompensa += self.ATAQUE_CERCANO
            elif distancia > 3:
                # Mal uso: ataca estando lejos
                recompensa += self.ATAQUE_LEJANO
        
        # Penalización por tiempo
        recompensa += self.TIEMPO_EXCESIVO
        
        return recompensa
    
    def calcular_recompensa_total(self, distancia_anterior: float,
                                 distancia_nueva: float,
                                 accion: str,
                                 leon_escondido: bool,
                                 impala_puede_ver: bool,
                                 impala_huye: bool,
                                 caceria_terminada: bool,
                                 exito: bool) -> float:
        """
        Calcula la recompensa total de un turno.
        
        Args:
            distancia_anterior: Distancia antes de la acción
            distancia_nueva: Distancia después de la acción
            accion: Acción ejecutada
            leon_escondido: Si el león está escondido
            impala_puede_ver: Si el impala puede ver al león
            impala_huye: Si el impala inició la huida
            caceria_terminada: Si la cacería terminó
            exito: Si fue exitosa (solo relevante si terminó)
            
        Returns:
            Recompensa total
        """
        recompensa = 0.0
        
        # Recompensa por acercamiento/alejamiento
        recompensa += self.calcular_recompensa_acercamiento(distancia_anterior, distancia_nueva)
        
        # Recompensa por la acción específica
        recompensa += self.calcular_recompensa_accion(
            accion, distancia_nueva, leon_escondido, impala_puede_ver
        )
        
        # Penalización por detección
        recompensa += self.calcular_recompensa_deteccion(impala_huye, distancia_nueva)
        
        # Recompensa final si terminó
        if caceria_terminada:
            recompensa += self.calcular_recompensa_final(exito)
        
        return recompensa
    
    def ajustar_configuracion(self, nuevos_valores: Dict[str, float]):
        """
        Ajusta los valores de recompensa.
        
        Args:
            nuevos_valores: Diccionario con nuevos valores
        """
        self.configuracion.update(nuevos_valores)
        
        # Actualizar constantes
        if 'exito' in nuevos_valores:
            self.EXITO_CACERIA = nuevos_valores['exito']
        if 'fracaso' in nuevos_valores:
            self.FRACASO_CACERIA = nuevos_valores['fracaso']
    
    def obtener_configuracion(self) -> Dict[str, float]:
        """
        Obtiene la configuración actual.
        
        Returns:
            Diccionario con todos los valores de recompensa
        """
        return self.configuracion.copy()
    
    def __str__(self) -> str:
        """Representación en string"""
        return f"SistemaRecompensas(Éxito={self.EXITO_CACERIA}, Fracaso={self.FRACASO_CACERIA})"


if __name__ == "__main__":
    # Pruebas básicas
    print("=== Pruebas del Sistema de Recompensas ===\n")
    
    sistema = SistemaRecompensas()
    
    # Prueba 1: Recompensa por acercamiento
    print("1. Recompensa por acercamiento:")
    r = sistema.calcular_recompensa_acercamiento(5.0, 4.0)
    print(f"   De 5.0 a 4.0 cuadros: {r:+.2f}")
    
    # Prueba 2: Penalización por alejamiento
    print("\n2. Penalización por alejamiento:")
    r = sistema.calcular_recompensa_acercamiento(4.0, 5.0)
    print(f"   De 4.0 a 5.0 cuadros: {r:+.2f}")
    
    # Prueba 3: Buen uso de esconderse
    print("\n3. Buen uso de esconderse:")
    r = sistema.calcular_recompensa_accion("esconderse", 4.0, False, True)
    print(f"   Esconderse cuando es visible: {r:+.2f}")
    
    # Prueba 4: Mal uso de esconderse
    print("\n4. Mal uso de esconderse:")
    r = sistema.calcular_recompensa_accion("esconderse", 4.0, False, False)
    print(f"   Esconderse cuando no es visible: {r:+.2f}")
    
    # Prueba 5: Buen ataque
    print("\n5. Buen ataque:")
    r = sistema.calcular_recompensa_accion("atacar", 1.5, False, False)
    print(f"   Atacar a 1.5 cuadros: {r:+.2f}")
    
    # Prueba 6: Mal ataque
    print("\n6. Mal ataque:")
    r = sistema.calcular_recompensa_accion("atacar", 4.0, False, False)
    print(f"   Atacar a 4.0 cuadros: {r:+.2f}")
    
    # Prueba 7: Recompensa total éxito
    print("\n7. Recompensa total (éxito):")
    r = sistema.calcular_recompensa_total(
        distancia_anterior=2.0,
        distancia_nueva=1.0,
        accion="atacar",
        leon_escondido=False,
        impala_puede_ver=False,
        impala_huye=False,
        caceria_terminada=True,
        exito=True
    )
    print(f"   Recompensa total: {r:+.2f}")
    
    # Prueba 8: Recompensa total fracaso
    print("\n8. Recompensa total (fracaso):")
    r = sistema.calcular_recompensa_total(
        distancia_anterior=4.0,
        distancia_nueva=5.0,
        accion="avanzar",
        leon_escondido=False,
        impala_puede_ver=True,
        impala_huye=True,
        caceria_terminada=True,
        exito=False
    )
    print(f"   Recompensa total: {r:+.2f}")
    
    print(f"\n{sistema}")
