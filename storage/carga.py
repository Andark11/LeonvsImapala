"""
Módulo de carga.
Deserializa y carga el conocimiento del león.
"""

import json
import os
from typing import Optional, Dict

from knowledge.base_conocimientos import BaseConocimientos


def cargar_conocimiento(ruta_archivo: str) -> Optional[BaseConocimientos]:
    """
    Carga una base de conocimientos desde un archivo JSON.
    
    Args:
        ruta_archivo: Ruta del archivo a cargar
        
    Returns:
        BaseConocimientos cargada o None si falló
    """
    try:
        if not os.path.exists(ruta_archivo):
            print(f"Archivo no encontrado: {ruta_archivo}")
            return None
        
        # Leer archivo
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            json_data = f.read()
        
        # Crear base de conocimientos e importar
        bc = BaseConocimientos()
        bc.importar_desde_json(json_data)
        
        return bc
    
    except Exception as e:
        print(f"Error al cargar conocimiento: {e}")
        return None


def cargar_estado_completo(ruta_directorio: str,
                          nombre_base: str) -> Optional[Dict]:
    """
    Carga el estado completo del sistema de aprendizaje.
    
    Args:
        ruta_directorio: Directorio donde están los archivos
        nombre_base: Nombre base de los archivos
        
    Returns:
        Diccionario con componentes cargados o None si falló
    """
    try:
        # Construir rutas
        ruta_bc = os.path.join(ruta_directorio, f"{nombre_base}_conocimiento.json")
        ruta_config = os.path.join(ruta_directorio, f"{nombre_base}_config.json")
        
        # Verificar existencia
        if not os.path.exists(ruta_bc):
            print(f"No se encontró archivo de conocimiento: {ruta_bc}")
            return None
        
        # Cargar base de conocimientos
        bc = cargar_conocimiento(ruta_bc)
        if bc is None:
            return None
        
        # Cargar configuración si existe
        config = None
        if os.path.exists(ruta_config):
            with open(ruta_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        return {
            'base_conocimientos': bc,
            'configuracion': config,
            'exito': True
        }
    
    except Exception as e:
        print(f"Error al cargar estado completo: {e}")
        return None


def validar_archivo_conocimiento(ruta_archivo: str) -> Dict:
    """
    Valida un archivo de conocimiento y retorna información básica.
    
    Args:
        ruta_archivo: Ruta del archivo a validar
        
    Returns:
        Diccionario con información de validación
    """
    try:
        if not os.path.exists(ruta_archivo):
            return {'valido': False, 'error': 'Archivo no existe'}
        
        # Leer y parsear JSON
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verificar estructura básica
        campos_requeridos = ['q_table', 'estadisticas']
        campos_faltantes = [c for c in campos_requeridos if c not in data]
        
        if campos_faltantes:
            return {
                'valido': False,
                'error': f'Campos faltantes: {campos_faltantes}'
            }
        
        # Extraer información
        metadata = data.get('metadata', {})
        stats = data.get('estadisticas', {})
        
        return {
            'valido': True,
            'fecha_guardado': metadata.get('fecha_guardado', 'Desconocida'),
            'version': metadata.get('version', 'Desconocida'),
            'estados_unicos': stats.get('estados_unicos', 0),
            'pares_estado_accion': stats.get('pares_estado_accion', 0),
            'tasa_exito': stats.get('tasa_exito', 0),
            'total_experiencias': stats.get('total_experiencias', 0)
        }
    
    except json.JSONDecodeError:
        return {'valido': False, 'error': 'JSON inválido'}
    except Exception as e:
        return {'valido': False, 'error': str(e)}


def fusionar_conocimientos(bc1: BaseConocimientos,
                          bc2: BaseConocimientos,
                          estrategia: str = 'promedio') -> BaseConocimientos:
    """
    Fusiona dos bases de conocimientos.
    
    Args:
        bc1: Primera base de conocimientos
        bc2: Segunda base de conocimientos
        estrategia: Estrategia de fusión ('promedio', 'maximo', 'minimo')
        
    Returns:
        Nueva base de conocimientos fusionada
    """
    bc_fusionada = BaseConocimientos()
    
    # Obtener todos los estados únicos
    estados_bc1 = bc1.obtener_estados_conocidos()
    estados_bc2 = bc2.obtener_estados_conocidos()
    todos_estados = estados_bc1.union(estados_bc2)
    
    # Acciones posibles
    acciones = ["avanzar", "esconderse", "atacar"]
    
    for estado in todos_estados:
        for accion in acciones:
            q1 = bc1.obtener_valor_q(estado, accion)
            q2 = bc2.obtener_valor_q(estado, accion)
            
            # Aplicar estrategia
            if estrategia == 'promedio':
                if q1 != 0 and q2 != 0:
                    valor_fusionado = (q1 + q2) / 2
                else:
                    valor_fusionado = q1 if q1 != 0 else q2
            
            elif estrategia == 'maximo':
                valor_fusionado = max(q1, q2)
            
            elif estrategia == 'minimo':
                if q1 == 0:
                    valor_fusionado = q2
                elif q2 == 0:
                    valor_fusionado = q1
                else:
                    valor_fusionado = min(q1, q2)
            
            else:
                raise ValueError(f"Estrategia desconocida: {estrategia}")
            
            if valor_fusionado != 0:
                bc_fusionada.actualizar_valor_q(estado, accion, valor_fusionado)
    
    return bc_fusionada


def exportar_a_texto_legible(ruta_json: str, ruta_salida: str) -> bool:
    """
    Exporta un archivo JSON a un formato de texto legible.
    
    Args:
        ruta_json: Ruta del archivo JSON
        ruta_salida: Ruta del archivo de texto de salida
        
    Returns:
        True si fue exitoso
    """
    try:
        bc = cargar_conocimiento(ruta_json)
        if bc is None:
            return False
        
        reporte = bc.generar_reporte_legible()
        
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(reporte)
        
        return True
    
    except Exception as e:
        print(f"Error al exportar a texto: {e}")
        return False


if __name__ == "__main__":
    # Pruebas básicas
    print("=== Pruebas de Carga ===\n")
    
    # Intentar cargar archivo de prueba
    ruta_test = "datos/test_conocimiento.json"
    
    if os.path.exists(ruta_test):
        print(f"Validando archivo {ruta_test}...")
        info = validar_archivo_conocimiento(ruta_test)
        
        print("Información del archivo:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        if info.get('valido'):
            print("\nCargando base de conocimientos...")
            bc = cargar_conocimiento(ruta_test)
            
            if bc:
                print(f"Cargada exitosamente: {bc}")
                print("\nEstadísticas:")
                for key, value in bc.obtener_estadisticas().items():
                    print(f"  {key}: {value}")
    else:
        print(f"Archivo de prueba no existe: {ruta_test}")
        print("Ejecuta primero las pruebas de guardado.py")
