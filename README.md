# León vs Impala - Sistema de Aprendizaje por Refuerzo

Sistema de aprendizaje automático donde un león joven aprende a cazar un impala en un abrevadero mediante aprendizaje por refuerzo (Q-Learning).

## 🚀 Inicio Rápido

```bash
# Ejecutar el programa principal
python main.py

# Ejecutar tests
python tests/test_basico.py
```

## 📋 Requisitos

- Python 3.8 o superior
- Solo librerías estándar (sin dependencias externas)

## 📁 Estructura del Proyecto

```
LeonvsImapala/
├── .github/
│   └── copilot-instructions.md    # Instrucciones para GitHub Copilot
│
├── agents/                         # Agentes del sistema
│   ├── __init__.py
│   ├── impala.py                  # Comportamiento del impala
│   └── leon.py                    # Comportamiento del león
│
├── simulation/                     # Motor de simulación
│   ├── __init__.py
│   ├── caceria.py                 # Lógica de incursión de cacería
│   ├── tiempo.py                  # Gestión de unidades de tiempo T
│   └── verificador.py             # Verificación de condiciones
│
├── knowledge/                      # ✅ Sistema de conocimiento
│   ├── __init__.py
│   ├── base_conocimientos.py     # Almacenamiento de experiencias
│   └── generalizacion.py         # Abstracción de patrones
│
├── learning/                       # ✅ Aprendizaje por refuerzo
│   ├── __init__.py
│   ├── q_learning.py             # Algoritmo Q-Learning
│   ├── entrenamiento.py          # Ciclos de entrenamiento
│   └── recompensas.py            # Sistema de recompensas
│
├── ui/                            # ✅ Interfaz de usuario
│   ├── __init__.py
│   ├── entrenamiento_ui.py       # UI para entrenamiento
│   ├── paso_a_paso.py            # Visualización detallada
│   └── explicador.py             # Explicación de decisiones
│
├── storage/                       # ✅ Persistencia
│   ├── __init__.py
│   ├── guardado.py               # Guardar conocimiento
│   └── carga.py                  # Cargar conocimiento
│
├── tests/                         # ✅ Pruebas unitarias
│   └── test_basico.py            # Suite de tests
│
├── datos/                         # Directorio para guardados
│   └── (archivos .json generados)
│   └── conocimiento_guardado.json
│
├── environment.py                 # Entorno del abrevadero ✅
├── main.py                        # Punto de entrada (próximo)
├── requirements.txt               # Dependencias (próximo)
└── README.md                      # Este archivo
```

## ✅ Módulos Implementados

### 1. **environment.py** - Entorno del Abrevadero
- Gestión de 8 posiciones + centro
- Cálculo de distancias y ángulos
- Verificación de línea de visión
- Sistema de coordenadas cartesianas

### 2. **agents/impala.py** - Agente Impala
- Acciones: ver izq/der/frente, beber agua, huir
- Ángulo de visión limitado (120°)
- Sistema de huida con aceleración progresiva
- Generación de secuencias aleatorias

### 3. **agents/leon.py** - Agente León
- Acciones: avanzar, esconderse, atacar, situarse
- Velocidad de avance: 1 cuadro/T
- Velocidad de ataque: 2 cuadros/T
- Control de visibilidad (escondido/visible)

### 4. **simulation/tiempo.py** - Gestión de Tiempo
- Registro de eventos por unidad de tiempo T
- Historia completa de la simulación
- Generación de resúmenes

### 5. **simulation/verificador.py** - Verificador de Condiciones
- Verificación de condiciones de huida
- Detección de éxito/fracaso de cacería
- Cálculo de estado del mundo

## 🎯 Siguiente Fase de Desarrollo

### Próximos módulos a implementar:

1. **simulation/caceria.py** - Orquestador principal
   - Coordina acciones de impala y león
   - Ejecuta una incursión completa
   - Determina resultado final

2. **knowledge/** - Sistema de conocimiento
   - Representación de estados
   - Almacenamiento de experiencias
   - Generalización de patrones

3. **learning/** - Aprendizaje por refuerzo
   - Algoritmo Q-Learning
   - Sistema de recompensas
   - Ciclos de entrenamiento

4. **ui/** - Interfaces de usuario
   - Modo entrenamiento
   - Modo paso a paso
   - Explicador de decisiones

## 🎮 Uso del Sistema

### Menú Principal

```bash
python main.py
```

El programa ofrece 5 opciones:

1. **Sistema de Entrenamiento** - Entrenar al león con miles de episodios
2. **Visualización Paso a Paso** - Ver cacerías sin entrenamiento (decisiones aleatorias)
3. **Visualización con León Entrenado** - Ver cacerías con león que usa conocimiento aprendido
4. **Acerca del Proyecto** - Información detallada
5. **Salir**

### Ejemplo: Entrenamiento

```bash
python main.py
# Seleccionar opción 1
# Configurar número de episodios (ej: 1000)
# Seleccionar posiciones iniciales (Enter para todas)
# Esperar a que termine el entrenamiento
# Guardar el conocimiento aprendido
```

### Ejemplo: Visualización con León Entrenado

```bash
python main.py
# Seleccionar opción 3
# Elegir un entrenamiento guardado
# Seleccionar posición inicial
# Ver cómo el león aplica lo aprendido
```

## 🧪 Tests

```bash
# Ejecutar suite de tests
python tests/test_basico.py

# O probar módulos individuales
python environment.py
python agents/leon.py
python knowledge/base_conocimientos.py
python learning/q_learning.py
```

## 📋 Reglas del Sistema

### Acciones por Turno (Tiempo T)
1. Impala actúa primero
2. León reacciona
3. Sistema verifica estado del mundo

### Condiciones de Huida del Impala
- Ve al león (dentro de ángulo de visión Y NO escondido)
- León inicia ataque
- Distancia < 3 cuadros

### Fin de Incursión
- **Éxito**: León alcanza al impala
- **Fracaso**: León no puede alcanzar al impala

## 🎓 Aprendizaje

El león debe aprender:
- ✅ Cuándo avanzar vs esconderse
- ✅ Desde qué distancia atacar
- ✅ Cómo aprovechar el comportamiento del impala
- ❌ NO se programa explícitamente la estrategia

## 📊 Modos de Operación

### 1. Fase de Entrenamiento
- Ciclos automáticos (100, 1000, 10000+ incursiones)
- Posiciones iniciales configurables
- Comportamiento impala: aleatorio o programado

### 2. Cacería Paso a Paso
- Visualización T1, T2, T3... Tn
- Explicación de decisiones del león
- Exportar base de conocimientos

## 🛠️ Tecnologías

- **Python 3.8+**
- Type hints
- Docstrings formato Google
- PEP 8

## 📝 Estado del Proyecto

- [x] Arquitectura modular definida
- [x] Instrucciones para Copilot
- [x] Módulo de entorno
- [x] Agentes básicos (león e impala)
- [x] Sistema de tiempo
- [x] Verificador de condiciones
- [ ] Módulo de cacería completo
- [ ] Sistema de conocimiento
- [ ] Aprendizaje Q-Learning
- [ ] Interfaz de usuario
- [ ] Persistencia
- [ ] Pruebas unitarias
- [ ] Documentación completa

---

**Próximo paso**: Implementar `simulation/caceria.py` para orquestar una incursión completa.
