"""Módulo de almacenamiento: Persistencia de conocimiento"""

from .guardado import guardar_conocimiento, guardar_estado_completo
from .carga import cargar_conocimiento, cargar_estado_completo

__all__ = [
    'guardar_conocimiento',
    'guardar_estado_completo',
    'cargar_conocimiento',
    'cargar_estado_completo'
]
