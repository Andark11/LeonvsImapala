# Copilot Instructions - León vs Impala

## Contexto del Proyecto
Sistema de aprendizaje automático donde un león joven aprende a cazar un impala en un abrevadero mediante aprendizaje por refuerzo.

## Arquitectura del Sistema

### Componentes Modulares
1. **Mapa y Entorno** (`environment.py`)
   - Gestión del abrevadero con 8 posiciones + centro
   - Sistema de coordenadas y distancias
   - Verificación de línea de visión

2. **Agentes** (`agents/`)
   - `impala.py`: Comportamiento del impala (ver, beber, huir)
   - `leon.py`: Acciones del león (avanzar, esconderse, atacar)

3. **Sistema de Conocimiento** (`knowledge/`)
   - `base_conocimientos.py`: Almacenamiento y gestión del conocimiento
   - `generalizacion.py`: Abstracción y generalización de patrones
   - Formato: Estados → Acciones → Resultados

4. **Aprendizaje** (`learning/`)
   - `q_learning.py`: Algoritmo de aprendizaje por refuerzo
   - `entrenamiento.py`: Ciclos de entrenamiento automático
   - `recompensas.py`: Sistema de recompensas/penalizaciones

5. **Simulación** (`simulation/`)
   - `caceria.py`: Lógica de una incursión de cacería
   - `tiempo.py`: Gestión de unidades de tiempo T
   - `verificador.py`: Validación de condiciones (huida, éxito, fracaso)

6. **Interfaz** (`ui/`)
   - `entrenamiento_ui.py`: Configuración de ciclos de entrenamiento
   - `paso_a_paso.py`: Visualización detallada de cacerías
   - `explicador.py`: Sistema que explica decisiones del león

7. **Persistencia** (`storage/`)
   - `guardado.py`: Serialización de conocimiento
   - `carga.py`: Recuperación de conocimiento guardado

## Reglas del Sistema

### Acciones por Turno (Tiempo T)
1. Impala actúa primero
2. León reacciona
3. Sistema verifica estado del mundo

### Comportamiento del Impala
- **Acciones**: Ver izq/der/frente, Beber agua, Huir
- **Visión**: Ángulo limitado (líneas rojas en mapa)
- **Huida**: Aceleración progresiva (1, 2, 3... cuadros/T)
- **Dirección huida**: Línea recta este u oeste

### Comportamiento del León
- **Acciones**: Avanzar (1 cuadro/T), Esconderse, Atacar (2 cuadros/T)
- **Restricción**: NO programar explícitamente estrategia
- **Objetivo**: Aprender por experiencia

### Condiciones de Huida del Impala
1. Ve al león (dentro de ángulo de visión Y NO escondido)
2. León inicia ataque (independiente de posición)
3. Distancia < 3 cuadros

### Fin de Incursión
- León no puede alcanzar al impala (fracaso)
- León alcanza al impala (éxito)

## Sistema de Aprendizaje

### Representación del Estado
```python
estado = {
    'posicion_leon': int (1-8),
    'distancia_impala': float,
    'accion_impala': str ('ver_izq', 'ver_der', 'ver_frente', 'beber'),
    'leon_escondido': bool,
    'impala_puede_ver': bool
}
```

### Generalización de Conocimiento
- Agrupar estados similares
- Ejemplo: "impala mira izq" + "impala mira der" → "impala no mira frente"
- Reducir espacio de búsqueda

### Recompensas
- **Éxito**: +100 (captura exitosa)
- **Fracaso**: -50 (impala huye)
- **Parcial**: +1 por acercamiento, -5 por detección temprana

## Modos de Operación

### 1. Fase de Entrenamiento
- Ciclos automáticos (configurable: 100, 1000, 10000+ incursiones)
- Posiciones iniciales configurables: [1,2,3,4,5,6,7,8]
- Comportamiento impala: aleatorio o programado
- Sin perder conocimiento al detener

### 2. Cacería Paso a Paso
- Visualización T1, T2, T3... Tn
- Mostrar: acción impala → reacción león → estado mundo
- Explicar: "¿Por qué el león hizo X?"
- Exportar base de conocimientos legible

## Consideraciones de Diseño

### Performance
- Entrenamientos de 20,000+ incursiones deben ser rápidos
- Optimizar búsqueda en base de conocimientos
- Cachear cálculos de distancia y visión

### Modularidad
- Cada módulo debe ser independiente y testeable
- Interfaces claras entre componentes
- Facilitar cambio de algoritmos de aprendizaje

### Testing
Crear pruebas para:
- Cacería exitosa
- Cacería fallida
- Generalización de conocimiento
- Ciclos de entrenamiento
- Persistencia de datos

## Estructura de Archivos
```
LeonvsImapala/
├── agents/
│   ├── __init__.py
│   ├── impala.py
│   └── leon.py
├── knowledge/
│   ├── __init__.py
│   ├── base_conocimientos.py
│   └── generalizacion.py
├── learning/
│   ├── __init__.py
│   ├── q_learning.py
│   ├── entrenamiento.py
│   └── recompensas.py
├── simulation/
│   ├── __init__.py
│   ├── caceria.py
│   ├── tiempo.py
│   └── verificador.py
├── ui/
│   ├── __init__.py
│   ├── entrenamiento_ui.py
│   ├── paso_a_paso.py
│   └── explicador.py
├── storage/
│   ├── __init__.py
│   ├── guardado.py
│   └── carga.py
├── environment.py
├── main.py
├── tests/
│   └── test_*.py
└── datos/
    └── conocimiento_guardado.json
```

## Convenciones de Código
- Python 3.8+
- Type hints en todas las funciones
- Docstrings en formato Google
- PEP 8 para estilo
- Nombres en español para claridad del dominio

## Prioridades de Desarrollo
1. ✅ Entorno y reglas básicas
2. ✅ Agentes con acciones básicas
3. ✅ Sistema de conocimiento simple
4. ✅ Aprendizaje Q-Learning básico
5. ✅ Entrenamiento automático
6. ✅ Generalización de conocimiento
7. ✅ Persistencia
8. ✅ Interfaz paso a paso
9. ✅ Sistema de explicaciones
10. ✅ Testing completo
