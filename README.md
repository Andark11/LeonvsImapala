# 🦁 León vs Impala - Sistema de Aprendizaje por Refuerzo# León vs Impala - Sistema de Aprendizaje por Refuerzo



Sistema de aprendizaje automático donde un león joven aprende a cazar un impala en un abrevadero mediante **Q-Learning**. El león no tiene estrategia programada, sino que aprende por experiencia tras miles de cacerías simuladas.Sistema de aprendizaje automático donde un león joven aprende a cazar un impala en un abrevadero mediante aprendizaje por refuerzo (Q-Learning).



## 🎯 Características Principales## 🚀 Inicio Rápido



- ✅ **Aprendizaje por Refuerzo**: Q-Learning con exploración epsilon-greedy```bash

- ✅ **Visualización en Terminal**: Grid ASCII 19×19 con colores ANSI# Ejecutar el programa principal

- ✅ **Persistencia de Modelos**: Guarda y carga conocimientos aprendidospython main.py

- ✅ **Sistema de Generalización**: Abstrae experiencias en patrones reutilables

- ✅ **Métricas de Rendimiento**: Seguimiento de tasa de éxito durante entrenamiento# Ejecutar tests

- ✅ **Simulación Realista**: Coordenadas polares, línea de visión, física de movimientopython tests/test_basico.py

```

## 🚀 Inicio Rápido

## 📋 Requisitos

### Requisitos

- Python 3.8 o superior- Python 3.8 o superior

- Sin dependencias externas (solo librerías estándar)- Solo librerías estándar (sin dependencias externas)



### Instalación## 📁 Estructura del Proyecto



```bash```

# Clonar el repositorioLeonvsImapala/

cd /home/holly/Proyectos/LeonvsImapala├── .github/

│   └── copilot-instructions.md    # Instrucciones para GitHub Copilot

# El proyecto está listo para ejecutarse│

python main.py├── agents/                         # Agentes del sistema

```│   ├── __init__.py

│   ├── impala.py                  # Comportamiento del impala

### Uso Básico│   └── leon.py                    # Comportamiento del león

│

```bash├── simulation/                     # Motor de simulación

python main.py│   ├── __init__.py

```│   ├── caceria.py                 # Lógica de incursión de cacería

│   ├── tiempo.py                  # Gestión de unidades de tiempo T

**Menú Principal:**│   └── verificador.py             # Verificación de condiciones

1. **Sistema de Entrenamiento** - Entrenar al león (recomendado: 10,000-100,000 episodios)│

2. **Simulación Visual** - Ver cacerías con visualización ASCII en tiempo real├── knowledge/                      # ✅ Sistema de conocimiento

3. **Acerca del Proyecto** - Información técnica detallada│   ├── __init__.py

4. **Salir**│   ├── base_conocimientos.py     # Almacenamiento de experiencias

│   └── generalizacion.py         # Abstracción de patrones

## 📁 Estructura del Proyecto│

├── learning/                       # ✅ Aprendizaje por refuerzo

```│   ├── __init__.py

LeonvsImapala/│   ├── q_learning.py             # Algoritmo Q-Learning

├── agents/                     # Agentes del sistema│   ├── entrenamiento.py          # Ciclos de entrenamiento

│   ├── impala.py              # Comportamiento del impala│   └── recompensas.py            # Sistema de recompensas

│   └── leon.py                # Comportamiento del león (aprendizaje)│

│├── ui/                            # ✅ Interfaz de usuario

├── knowledge/                  # Sistema de conocimiento│   ├── __init__.py

│   ├── base_conocimientos.py # Tabla Q y almacenamiento│   ├── entrenamiento_ui.py       # UI para entrenamiento

│   └── generalizacion.py     # Generalización de patrones│   ├── paso_a_paso.py            # Visualización detallada

││   └── explicador.py             # Explicación de decisiones

├── learning/                   # Aprendizaje por refuerzo│

│   ├── q_learning.py         # Algoritmo Q-Learning├── storage/                       # ✅ Persistencia

│   ├── entrenamiento.py      # Ciclos de entrenamiento│   ├── __init__.py

│   └── recompensas.py        # Sistema de recompensas│   ├── guardado.py               # Guardar conocimiento

││   └── carga.py                  # Cargar conocimiento

├── simulation/                 # Motor de simulación│

│   ├── caceria.py            # Orquestador de incursiones├── tests/                         # ✅ Pruebas unitarias

│   ├── tiempo.py             # Gestión de turnos│   └── test_basico.py            # Suite de tests

│   └── verificador.py        # Condiciones de éxito/fracaso│

│├── datos/                         # Directorio para guardados

├── storage/                    # Persistencia│   └── (archivos .json generados)

│   ├── guardado.py           # Guardar modelos│   └── conocimiento_guardado.json

│   └── carga.py              # Cargar modelos│

│├── environment.py                 # Entorno del abrevadero ✅

├── ui/                        # Interfaces de usuario├── main.py                        # Punto de entrada (próximo)

│   ├── entrenamiento_ui.py   # UI de entrenamiento├── requirements.txt               # Dependencias (próximo)

│   ├── interfaz_terminal_grid.py  # Visualización ASCII└── README.md                      # Este archivo

│   ├── paso_a_paso.py        # Modo paso a paso (texto)```

│   └── explicador.py         # Explicador de decisiones

│## ✅ Módulos Implementados

├── modelos/                   # Modelos entrenados (generados)

│   └── *.json                # Conocimientos guardados### 1. **environment.py** - Entorno del Abrevadero

│- Gestión de 8 posiciones + centro

├── environment.py             # Configuración del abrevadero- Cálculo de distancias y ángulos

├── main.py                    # Punto de entrada- Verificación de línea de visión

└── requirements.txt           # Dependencias- Sistema de coordenadas cartesianas

```

### 2. **agents/impala.py** - Agente Impala

## 🎮 Guía de Uso- Acciones: ver izq/der/frente, beber agua, huir

- Ángulo de visión limitado (120°)

### 1. Entrenar un Nuevo León- Sistema de huida con aceleración progresiva

- Generación de secuencias aleatorias

```bash

python main.py### 3. **agents/leon.py** - Agente León

# Seleccionar: 1 (Sistema de Entrenamiento)- Acciones: avanzar, esconderse, atacar, situarse

# Elegir: 1 (Nuevo entrenamiento)- Velocidad de avance: 1 cuadro/T

# Configurar episodios: 100000 (recomendado)- Velocidad de ataque: 2 cuadros/T

# Seleccionar posición inicial: 0 (todas)- Control de visibilidad (escondido/visible)

# Esperar... (muestra progreso en tiempo real)

# Guardar modelo con nombre descriptivo### 4. **simulation/tiempo.py** - Gestión de Tiempo

```- Registro de eventos por unidad de tiempo T

- Historia completa de la simulación

**Parámetros de entrenamiento:**- Generación de resúmenes

- **alpha (α)**: 0.05 - Tasa de aprendizaje

- **gamma (γ)**: 0.9 - Factor de descuento### 5. **simulation/verificador.py** - Verificador de Condiciones

- **epsilon (ε)**: 0.01 - Tasa de exploración final- Verificación de condiciones de huida

- Detección de éxito/fracaso de cacería

**Resultados típicos:**- Cálculo de estado del mundo

- **10,000 episodios**: ~6-8% de éxito

- **100,000 episodios**: ~10-12% de éxito## 🎯 Siguiente Fase de Desarrollo

- **500,000+ episodios**: ~12-15% de éxito

### Próximos módulos a implementar:

### 2. Visualizar Cacería con León Entrenado

1. **simulation/caceria.py** - Orquestador principal

```bash   - Coordina acciones de impala y león

python main.py   - Ejecuta una incursión completa

# Seleccionar: 2 (Simulación Visual)   - Determina resultado final

# Elegir modelo entrenado de la lista

# Seleccionar posición inicial del león2. **knowledge/** - Sistema de conocimiento

# Observar la cacería en el grid 19×19   - Representación de estados

# Presionar Enter para avanzar cada turno   - Almacenamiento de experiencias

```   - Generalización de patrones



**Leyenda de visualización:**3. **learning/** - Aprendizaje por refuerzo

- 🦁 León   - Algoritmo Q-Learning

- 🦌 Impala   - Sistema de recompensas

- ▓ Abrevadero (centro)   - Ciclos de entrenamiento

- ░ Área de visión del impala

- ○ Trayectoria del león4. **ui/** - Interfaces de usuario

   - Modo entrenamiento

### 3. Continuar Entrenamiento Existente   - Modo paso a paso

   - Explicador de decisiones

```bash

python main.py## 🎮 Uso del Sistema

# Seleccionar: 1 (Sistema de Entrenamiento)

# Elegir: 2 (Continuar entrenamiento)### Menú Principal

# Seleccionar modelo a continuar

# Agregar más episodios```bash

# Guardar progresopython main.py

``````



## 🧠 Sistema de AprendizajeEl programa ofrece 5 opciones:



### Q-Learning1. **Sistema de Entrenamiento** - Entrenar al león con miles de episodios

2. **Visualización Paso a Paso** - Ver cacerías sin entrenamiento (decisiones aleatorias)

El león aprende mediante la ecuación de Bellman:3. **Visualización con León Entrenado** - Ver cacerías con león que usa conocimiento aprendido

4. **Acerca del Proyecto** - Información detallada

```5. **Salir**

Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',a') - Q(s,a)]

```### Ejemplo: Entrenamiento



**Donde:**```bash

- `s`: Estado actual (posición león, distancia impala, acción impala, visibilidad)python main.py

- `a`: Acción tomada (avanzar, esconderse, atacar)# Seleccionar opción 1

- `r`: Recompensa obtenida# Configurar número de episodios (ej: 1000)

- `s'`: Estado siguiente# Seleccionar posiciones iniciales (Enter para todas)

- `α`: Tasa de aprendizaje (0.05)# Esperar a que termine el entrenamiento

- `γ`: Factor de descuento (0.9)# Guardar el conocimiento aprendido

```

### Sistema de Recompensas

### Ejemplo: Visualización con León Entrenado

| Evento | Recompensa |

|--------|-----------|```bash

| ✅ Cacería exitosa | +100 |python main.py

| ❌ Impala escapa | -50 |# Seleccionar opción 3

| ⚠️ Impala detecta al león | -10 |# Elegir un entrenamiento guardado

| 📍 Reducción de distancia | +1 |# Seleccionar posición inicial

| 🏃 Impala huye | -5 |# Ver cómo el león aplica lo aprendido

```

### Generalización

## 🧪 Tests

El sistema abstrae estados específicos en **patrones generales**:

- Distancias se redondean a 0.5 cuadros```bash

- Estados similares comparten conocimiento# Ejecutar suite de tests

- Tabla Q más compacta y eficientepython tests/test_basico.py



## 🌍 Entorno de Simulación# O probar módulos individuales

python environment.py

### Abrevaderopython agents/leon.py

python knowledge/base_conocimientos.py

- **Grid**: 19×19 cuadrospython learning/q_learning.py

- **Centro**: (9.5, 9.5) - Posición del abrevadero```

- **RADIO**: 9.5 cuadros - Distancia inicial león-impala

- **Coordenadas**: Polares (r, θ) para el león, Cartesianas (x, y) para visualización## 📋 Reglas del Sistema



### Posiciones Iniciales del León### Acciones por Turno (Tiempo T)

1. Impala actúa primero

El león puede iniciar en 8 posiciones alrededor del abrevadero:2. León reacciona

- **Posición 1**: Norte (0°)3. Sistema verifica estado del mundo

- **Posición 2**: Noreste (45°)

- **Posición 3**: Este (90°)### Condiciones de Huida del Impala

- **Posición 4**: Sureste (135°)- Ve al león (dentro de ángulo de visión Y NO escondido)

- **Posición 5**: Sur (180°)- León inicia ataque

- **Posición 6**: Suroeste (225°)- Distancia < 3 cuadros

- **Posición 7**: Oeste (270°)

- **Posición 8**: Noroeste (315°)### Fin de Incursión

- **Éxito**: León alcanza al impala

### Comportamiento del Impala- **Fracaso**: León no puede alcanzar al impala



**Secuencia programada:**## 🎓 Aprendizaje

1. Ver izquierda

2. Ver derechaEl león debe aprender:

3. Ver al frente- ✅ Cuándo avanzar vs esconderse

4. Beber agua (vulnerable - no ve)- ✅ Desde qué distancia atacar

5. Ver izquierda- ✅ Cómo aprovechar el comportamiento del impala

6. Ver al frente- ❌ NO se programa explícitamente la estrategia

7. Beber agua

## 📊 Modos de Operación

**Ángulo de visión:** 120° (puede ver en un cono frontal)

### 1. Fase de Entrenamiento

**Condiciones de huida:**- Ciclos automáticos (100, 1000, 10000+ incursiones)

- Detecta al león visible dentro de su ángulo de visión- Posiciones iniciales configurables

- León inicia ataque- Comportamiento impala: aleatorio o programado

- Distancia < 3 cuadros (DISTANCIA_MINIMA_HUIDA)

### 2. Cacería Paso a Paso

**Velocidad de huida:** 1.5 cuadros/turno (más rápido que el león)- Visualización T1, T2, T3... Tn

- Explicación de decisiones del león

### Acciones del León- Exportar base de conocimientos



| Acción | Velocidad | Descripción |## 🛠️ Tecnologías

|--------|-----------|-------------|

| **Avanzar** | 1 cuadro/T | Se acerca al abrevadero (visible) |- **Python 3.8+**

| **Esconderse** | 0 cuadros/T | Se oculta en su posición (invisible) |- Type hints

| **Atacar** | 2 cuadros/T | Sprint final hacia el impala |- Docstrings formato Google

- PEP 8

## 📊 Archivos Guardados

## 📝 Estado del Proyecto

Cada modelo entrenado genera 3 archivos en `modelos/`:

- [x] Arquitectura modular definida

1. **`nombre_conocimiento.json`**: Tabla Q completa- [x] Instrucciones para Copilot

2. **`nombre_config.json`**: Configuración (RADIO, parámetros de aprendizaje)- [x] Módulo de entorno

3. **`nombre_reporte.txt`**: Métricas y estadísticas del entrenamiento- [x] Agentes básicos (león e impala)

- [x] Sistema de tiempo

### Formato de Configuración- [x] Verificador de condiciones

- [ ] Módulo de cacería completo

```json- [ ] Sistema de conocimiento

{- [ ] Aprendizaje Q-Learning

  "radio": 9.5,- [ ] Interfaz de usuario

  "angulo_vision": 120,- [ ] Persistencia

  "distancia_minima_huida": 3,- [ ] Pruebas unitarias

  "cacerias_exitosas": 10450,- [ ] Documentación completa

  "total_cacerias": 100000,

  "experiencias_unicas": 145135---

}

```**Próximo paso**: Implementar `simulation/caceria.py` para orquestar una incursión completa.


### Verificación de Compatibilidad

El sistema verifica que el **RADIO** del modelo coincida con el entorno actual:
- ✅ RADIO = 9.5 → Compatible
- ❌ RADIO = 5.0 → Incompatible (muestra advertencia)

## 🔬 Detalles Técnicos

### Estados del Mundo

Un estado se define por:
- **posicion_leon**: (r, θ) - Coordenadas polares
- **distancia_impala**: Distancia león-impala (redondeada)
- **accion_impala**: Acción actual del impala
- **leon_escondido**: Boolean (visible/invisible)
- **impala_puede_ver**: Boolean (dentro/fuera de visión)

### Tabla Q

Estructura: `Dict[Estado, Dict[Accion, float]]`
- **Claves**: Estados del mundo (dataclass hashable)
- **Valores**: Diccionario de valores Q por acción
- **Tamaño típico**: 145,000-675,000 experiencias únicas

### Política de Exploración

**Epsilon-greedy decreciente:**
- Inicio: ε = 1.0 (100% exploración)
- Decremento: ε -= 0.9/num_episodios por episodio
- Final: ε = 0.1 (10% exploración, 90% explotación)

## 🏆 Resultados de Ejemplo

### Entrenamiento EM4 (100,000 episodios)

```
Total de cacerías: 100,000
Cacerías exitosas: 10,450
Tasa de éxito: 10.45%
Experiencias únicas: 145,135
Tiempo de entrenamiento: ~15 minutos
```

### Progresión Típica

| Episodios | Tasa de Éxito |
|-----------|---------------|
| 1,000 | 3-4% |
| 10,000 | 6-8% |
| 50,000 | 9-10% |
| 100,000 | 10-12% |
| 500,000 | 12-15% |

## 🐛 Solución de Problemas

### Error: "El RADIO del modelo no coincide"

El modelo fue entrenado con RADIO=5.0 (obsoleto). Entrenar nuevo modelo con RADIO=9.5.

### El impala siempre escapa

Normal con pocos episodios de entrenamiento. Entrenar con 100,000+ episodios.

### Visualización no muestra colores

Terminal no soporta ANSI. Los emojis y ASCII seguirán funcionando.

### Error de importación

Verificar que estás ejecutando desde el directorio raíz del proyecto.

## 📚 Referencias

- **Q-Learning**: Watkins, C.J.C.H. (1989). Learning from Delayed Rewards
- **Aprendizaje por Refuerzo**: Sutton & Barto (2018). Reinforcement Learning: An Introduction

## 👨‍💻 Desarrollo

### Próximas Mejoras

- [ ] Interfaz gráfica con pygame/tkinter
- [ ] Múltiples impalas en el abrevadero
- [ ] Terreno con obstáculos
- [ ] Deep Q-Networks (DQN)
- [ ] Algoritmos alternativos (SARSA, Actor-Critic)

### Contribuir

El proyecto fue desarrollado como trabajo final de Sistemas Inteligentes. Las contribuciones son bienvenidas.

## 📄 Licencia

Este proyecto es de código abierto para fines educativos.

---

**Desarrollado con:** Python 3.13 | Q-Learning | Aprendizaje por Refuerzo

**Estado:** ✅ Funcional - 10.45% tasa de éxito con 100K episodios
