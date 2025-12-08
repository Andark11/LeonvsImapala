"""
Interfaz de usuario para configurar y ejecutar ciclos de entrenamiento.
"""

from typing import Optional
import os

from learning.entrenamiento import Entrenador
from simulation.caceria import ModoBehaviorImpala
from storage.guardado import guardar_estado_completo, listar_guardados
from storage.carga import cargar_estado_completo


class EntrenamientoUI:
    """
    Interfaz para configurar y ejecutar entrenamientos.
    """
    
    def __init__(self):
        """Inicializa la interfaz"""
        self.entrenador = Entrenador()
        self.directorio_datos = "modelos"
    
    def ejecutar_entrenamiento_interactivo(self):
        """Ejecuta un entrenamiento con configuración interactiva"""
        print("=" * 70)
        print("CONFIGURACIÓN DE ENTRENAMIENTO")
        print("=" * 70)
        
        # Número de episodios
        while True:
            try:
                num_episodios = int(input("\nNúmero de episodios (ej: 1000): "))
                if num_episodios > 0:
                    break
                print("Debe ser un número positivo")
            except ValueError:
                print("Entrada inválida")
        
        # Posiciones iniciales
        print("\nPosiciones iniciales del león (1-8, separadas por comas)")
        print("Presiona Enter para usar todas")
        entrada_pos = input("Posiciones: ").strip()
        
        if entrada_pos:
            try:
                posiciones = [int(p.strip()) for p in entrada_pos.split(',')]
                posiciones = [p for p in posiciones if 1 <= p <= 8]
            except:
                posiciones = None
        else:
            posiciones = None
        
        # Comportamiento del impala
        print("\nComportamiento del impala:")
        print("1. Aleatorio (recomendado)")
        print("2. Programado")
        
        comportamiento = ModoBehaviorImpala.ALEATORIO
        entrada_comp = input("Opción (1/2): ").strip()
        if entrada_comp == '2':
            comportamiento = ModoBehaviorImpala.PROGRAMADO
        
        # Confirmación
        print("\n" + "=" * 70)
        print("RESUMEN DE CONFIGURACIÓN")
        print("=" * 70)
        print(f"Episodios: {num_episodios}")
        print(f"Posiciones: {posiciones if posiciones else 'Todas (1-8)'}")
        print(f"Comportamiento impala: {comportamiento.value}")
        print("=" * 70)
        
        confirmar = input("\n¿Iniciar entrenamiento? (s/n): ").strip().lower()
        if confirmar != 's':
            print("Entrenamiento cancelado")
            return
        
        # Ejecutar entrenamiento
        print("\nINICIANDO ENTRENAMIENTO...")
        print("(Esto puede tardar varios minutos)")
        print()
        
        def callback_progreso(actual, total, exitosas_sesion, exitosas_totales, cacerias_totales):
            # Tasa de la sesión actual
            tasa_sesion = (exitosas_sesion / actual * 100) if actual > 0 else 0
            # Tasa acumulada (incluyendo entrenamientos anteriores)
            tasa_total = (exitosas_totales / cacerias_totales * 100) if cacerias_totales > 0 else 0
            
            print(f"Progreso: {actual}/{total} | "
                  f"Sesión: {tasa_sesion:.1f}% | "
                  f"Total acumulado: {tasa_total:.1f}% ({exitosas_totales}/{cacerias_totales})")
        
        reporte = self.entrenador.entrenar(
            num_episodios=num_episodios,
            posiciones_iniciales=posiciones,
            comportamiento_impala=comportamiento,
            verbose=False,
            callback_progreso=callback_progreso
        )
        
        # Mostrar resultados
        self._mostrar_resultados(reporte)
        
        # Ofrecer guardar
        guardar = input("\n¿Guardar conocimiento aprendido? (s/n): ").strip().lower()
        if guardar == 's':
            self._guardar_entrenamiento()
    
    def _mostrar_resultados(self, reporte: dict):
        """Muestra los resultados del entrenamiento"""
        print("\n" + "=" * 70)
        print("RESULTADOS DEL ENTRENAMIENTO")
        print("=" * 70)
        
        print(f"\nEpisodios ejecutados: {reporte['episodios']}")
        print(f"Cacerías exitosas: {reporte['exitosas']}")
        print(f"Cacerías fallidas: {reporte['fallidas']}")
        print(f"Tasa de éxito: {reporte['tasa_exito']}%")
        print(f"Duración: {reporte['duracion_segundos']} segundos")
        print(f"Velocidad: {reporte['episodios_por_segundo']} episodios/seg")
        
        print("\nBase de Conocimientos:")
        for key, value in reporte['estadisticas_bc'].items():
            print(f"  {key}: {value}")
        
        print("\nParámetros de Q-Learning:")
        for key, value in reporte['estadisticas_ql'].items():
            print(f"  {key}: {value}")
    
    def _guardar_entrenamiento(self):
        """Guarda el estado del entrenamiento"""
        nombre = input("Nombre para este entrenamiento (opcional): ").strip()
        
        resultado = guardar_estado_completo(
            self.entrenador.base_conocimientos,
            self.entrenador.q_learning,
            self.entrenador.generalizador,
            self.directorio_datos,
            nombre if nombre else None
        )
        
        if resultado.get('exito'):
            print("\n✓ Entrenamiento guardado exitosamente")
            print(f"  Conocimiento: {resultado['conocimiento']}")
            print(f"  Configuración: {resultado['config']}")
            print(f"  Reporte: {resultado['reporte']}")
        else:
            print(f"\n✗ Error al guardar: {resultado.get('error', 'Desconocido')}")
    
    def cargar_entrenamiento_previo(self) -> bool:
        """Carga un entrenamiento guardado previamente"""
        guardados = listar_guardados(self.directorio_datos)
        
        if not guardados:
            print("No hay entrenamientos guardados")
            return False
        
        print("\n" + "=" * 70)
        print("ENTRENAMIENTOS GUARDADOS")
        print("=" * 70)
        
        for i, guardado in enumerate(guardados, 1):
            print(f"\n{i}. {guardado['archivo']}")
            print(f"   Fecha: {guardado['fecha']}")
            print(f"   Estados: {guardado['estados']}")
            print(f"   Tasa de éxito: {guardado['tasa_exito']}%")
        
        try:
            seleccion = int(input("\nSelecciona un entrenamiento (número): ")) - 1
            if 0 <= seleccion < len(guardados):
                guardado = guardados[seleccion]
                
                # Extraer nombre base del archivo
                nombre_archivo = guardado['archivo']
                nombre_base = nombre_archivo.replace('_conocimiento.json', '')
                
                # Cargar
                resultado = cargar_estado_completo(self.directorio_datos, nombre_base)
                
                if resultado and resultado.get('exito'):
                    self.entrenador.base_conocimientos = resultado['base_conocimientos']
                    print("\n✓ Entrenamiento cargado exitosamente")
                    return True
                else:
                    print("\n✗ Error al cargar entrenamiento")
                    return False
        except:
            print("Selección inválida")
            return False
    
    def menu_principal(self):
        """Muestra el menú principal de entrenamiento"""
        while True:
            print("\n" + "=" * 70)
            print("SISTEMA DE ENTRENAMIENTO - LEÓN VS IMPALA")
            print("=" * 70)
            print("1. Nuevo entrenamiento")
            print("2. Continuar entrenamiento existente")
            print("3. Ver estadísticas actuales")
            print("4. Listar entrenamientos guardados")
            print("5. Salir")
            
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == '1':
                self.ejecutar_entrenamiento_interactivo()
            
            elif opcion == '2':
                if self.cargar_entrenamiento_previo():
                    self.ejecutar_entrenamiento_interactivo()
            
            elif opcion == '3':
                self._mostrar_estadisticas_actuales()
            
            elif opcion == '4':
                self._listar_entrenamientos()
            
            elif opcion == '5':
                print("\n¡Hasta luego!")
                break
            
            else:
                print("Opción inválida")
    
    def _mostrar_estadisticas_actuales(self):
        """Muestra las estadísticas del entrenador actual"""
        print("\n" + "=" * 70)
        print("ESTADÍSTICAS ACTUALES")
        print("=" * 70)
        
        stats = self.entrenador.obtener_estadisticas_globales()
        
        print(f"\nTotal de cacerías: {stats['total_cacerias']}")
        print(f"Cacerías exitosas: {stats['cacerias_exitosas']}")
        print(f"Tasa de éxito global: {stats['tasa_exito_global']}%")
        
        print("\nBase de conocimientos:")
        for key, value in stats['base_conocimientos'].items():
            print(f"  {key}: {value}")
    
    def _listar_entrenamientos(self):
        """Lista todos los entrenamientos guardados"""
        guardados = listar_guardados(self.directorio_datos)
        
        if not guardados:
            print("\nNo hay entrenamientos guardados")
            return
        
        print("\n" + "=" * 70)
        print("ENTRENAMIENTOS GUARDADOS")
        print("=" * 70)
        
        for guardado in guardados:
            print(f"\nArchivo: {guardado['archivo']}")
            print(f"  Fecha: {guardado['fecha']}")
            print(f"  Estados únicos: {guardado['estados']}")
            print(f"  Tasa de éxito: {guardado['tasa_exito']}%")


if __name__ == "__main__":
    ui = EntrenamientoUI()
    ui.menu_principal()
