"""
Módulo de guardado.
Serializa y guarda el conocimiento del león.
"""

import json
import os
from datetime import datetime
from typing import Optional

from knowledge.base_conocimientos import BaseConocimientos
from knowledge.generalizacion import Generalizador
from learning.q_learning import QLearning


def guardar_conocimiento(base_conocimientos: BaseConocimientos,
                        ruta_archivo: str,
                        incluir_experiencias: bool = True) -> bool:
    """
    Guarda la base de conocimientos en un archivo JSON.
    
    Args:
        base_conocimientos: Base de conocimientos a guardar
        ruta_archivo: Ruta del archivo de destino
        incluir_experiencias: Si incluir experiencias detalladas
        
    Returns:
        True si se guardó exitosamente
    """
    try:
        # Crear directorio si no existe
        directorio = os.path.dirname(ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        # Generar JSON
        json_data = base_conocimientos.exportar_a_json()
        
        # Agregar metadatos
        data = json.loads(json_data)
        data['metadata'] = {
            'fecha_guardado': datetime.now().isoformat(),
            'version': '1.0'
        }
        
        # Guardar archivo
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    
    except Exception as e:
        print(f"Error al guardar conocimiento: {e}")
        return False


def guardar_estado_completo(base_conocimientos: BaseConocimientos,
                           q_learning: QLearning,
                           generalizador: Generalizador,
                           ruta_directorio: str,
                           nombre_base: Optional[str] = None) -> dict:
    """
    Guarda el estado completo del sistema de aprendizaje.
    
    Args:
        base_conocimientos: Base de conocimientos
        q_learning: Instancia de Q-Learning
        generalizador: Generalizador
        ruta_directorio: Directorio donde guardar
        nombre_base: Nombre base para los archivos (default: timestamp)
        
    Returns:
        Diccionario con rutas de archivos guardados
    """
    try:
        # Crear directorio si no existe
        if not os.path.exists(ruta_directorio):
            os.makedirs(ruta_directorio)
        
        # Generar nombre base si no se proporciona
        if nombre_base is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_base = f"entrenamiento_{timestamp}"
        
        # Rutas de archivos
        ruta_bc = os.path.join(ruta_directorio, f"{nombre_base}_conocimiento.json")
        ruta_config = os.path.join(ruta_directorio, f"{nombre_base}_config.json")
        ruta_reporte = os.path.join(ruta_directorio, f"{nombre_base}_reporte.txt")
        
        # Guardar base de conocimientos
        guardar_conocimiento(base_conocimientos, ruta_bc)
        
        # Guardar configuración de Q-Learning
        config = {
            'q_learning': q_learning.obtener_estadisticas(),
            'estadisticas_bc': base_conocimientos.obtener_estadisticas(),
            'metadata': {
                'fecha_guardado': datetime.now().isoformat(),
                'version': '1.0'
            }
        }
        
        with open(ruta_config, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        # Guardar reporte legible
        reporte = base_conocimientos.generar_reporte_legible()
        reporte += "\n\n" + "=" * 70 + "\n"
        reporte += "PARÁMETROS DE Q-LEARNING\n"
        reporte += "=" * 70 + "\n"
        for key, value in q_learning.obtener_estadisticas().items():
            reporte += f"{key}: {value}\n"
        
        with open(ruta_reporte, 'w', encoding='utf-8') as f:
            f.write(reporte)
        
        return {
            'conocimiento': ruta_bc,
            'config': ruta_config,
            'reporte': ruta_reporte,
            'exito': True
        }
    
    except Exception as e:
        print(f"Error al guardar estado completo: {e}")
        return {'exito': False, 'error': str(e)}


def crear_backup(ruta_archivo: str) -> Optional[str]:
    """
    Crea una copia de respaldo de un archivo.
    
    Args:
        ruta_archivo: Ruta del archivo a respaldar
        
    Returns:
        Ruta del backup o None si falló
    """
    try:
        if not os.path.exists(ruta_archivo):
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = os.path.basename(ruta_archivo)
        nombre_sin_ext, ext = os.path.splitext(nombre_archivo)
        
        directorio = os.path.dirname(ruta_archivo)
        ruta_backup = os.path.join(directorio, f"{nombre_sin_ext}_backup_{timestamp}{ext}")
        
        # Copiar archivo
        with open(ruta_archivo, 'r', encoding='utf-8') as f_origen:
            contenido = f_origen.read()
        
        with open(ruta_backup, 'w', encoding='utf-8') as f_destino:
            f_destino.write(contenido)
        
        return ruta_backup
    
    except Exception as e:
        print(f"Error al crear backup: {e}")
        return None


def listar_guardados(ruta_directorio: str) -> list:
    """
    Lista todos los guardados disponibles en un directorio.
    
    Args:
        ruta_directorio: Directorio a explorar
        
    Returns:
        Lista de diccionarios con información de guardados
    """
    try:
        if not os.path.exists(ruta_directorio):
            return []
        
        guardados = []
        archivos = os.listdir(ruta_directorio)
        
        # Buscar archivos de conocimiento
        for archivo in archivos:
            if archivo.endswith('_conocimiento.json'):
                ruta_completa = os.path.join(ruta_directorio, archivo)
                
                # Leer metadata
                try:
                    with open(ruta_completa, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    metadata = data.get('metadata', {})
                    stats = data.get('estadisticas', {})
                    
                    guardados.append({
                        'archivo': archivo,
                        'ruta': ruta_completa,
                        'fecha': metadata.get('fecha_guardado', 'Desconocida'),
                        'estados': stats.get('estados_unicos', 0),
                        'tasa_exito': stats.get('tasa_exito', 0)
                    })
                
                except Exception:
                    pass
        
        # Ordenar por fecha (más reciente primero)
        guardados.sort(key=lambda x: x['fecha'], reverse=True)
        
        return guardados
    
    except Exception as e:
        print(f"Error al listar guardados: {e}")
        return []


if __name__ == "__main__":
    # Pruebas básicas
    from knowledge.base_conocimientos import BaseConocimientos, Estado, Experiencia
    
    print("=== Pruebas de Guardado ===\n")
    
    # Crear base de conocimientos de prueba
    bc = BaseConocimientos()
    
    estado1 = Estado(1, 5.0, "ver_frente", False, True)
    estado2 = Estado(1, 4.0, "beber_agua", False, False)
    
    bc.actualizar_valor_q(estado1, "avanzar", 10.5)
    bc.actualizar_valor_q(estado1, "esconderse", 5.2)
    bc.agregar_experiencia(Experiencia(estado1, "avanzar", 5.0, estado2, False))
    
    print(f"Base de conocimientos: {bc}\n")
    
    # Guardar en archivo temporal
    ruta_test = "datos/test_conocimiento.json"
    print(f"Guardando en {ruta_test}...")
    exito = guardar_conocimiento(bc, ruta_test)
    print(f"Resultado: {'Éxito' if exito else 'Fracaso'}\n")
    
    if exito and os.path.exists(ruta_test):
        # Verificar contenido
        with open(ruta_test, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("Contenido guardado:")
        print(f"  Estadísticas: {data.get('estadisticas', {})}")
        print(f"  Metadata: {data.get('metadata', {})}")
        print(f"  Pares Q-table: {len(data.get('q_table', []))}")
