"""Módulo de conocimiento: Base de conocimientos y generalización"""

from .base_conocimientos import BaseConocimientos, Estado, Experiencia
from .generalizacion import Generalizador

__all__ = ['BaseConocimientos', 'Estado', 'Experiencia', 'Generalizador']
