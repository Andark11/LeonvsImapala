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



## 🧠 Sistema de Aprendizaje

### ¿Qué es Q-Learning?

**Q-Learning** es un algoritmo de **Aprendizaje por Refuerzo** (Reinforcement Learning) que permite a un agente aprender la mejor acción a tomar en cada situación mediante prueba y error, sin necesidad de un modelo explícito del entorno.

#### Concepto Fundamental

El león aprende construyendo una **tabla Q** que mapea cada combinación de estado-acción a un valor que representa "qué tan buena" es esa acción en ese estado. A través de miles de cacerías, el león descubre qué acciones maximizan su probabilidad de éxito.

#### Proceso de Aprendizaje

1. **Exploración**: Al inicio, el león prueba acciones aleatorias para descubrir el entorno
2. **Experiencia**: Cada cacería genera experiencias (estado → acción → recompensa → nuevo estado)
3. **Actualización**: Los valores Q se actualizan basándose en las recompensas obtenidas
4. **Explotación**: Con el tiempo, el león prefiere acciones que históricamente funcionaron mejor
5. **Convergencia**: Después de muchos episodios, el león desarrolla una estrategia óptima

### La Ecuación de Bellman

El león aprende mediante la **ecuación de Bellman** para actualización de valores Q:

```
Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',a') - Q(s,a)]
```

**Componentes de la ecuación:**

- **`Q(s,a)`**: Valor Q actual para el estado `s` y acción `a`
- **`α`** (alpha): **Tasa de aprendizaje** = 0.05
  - Controla qué tan rápido se actualizan los valores
  - Valor bajo (0.05) = aprendizaje gradual y estable
  
- **`γ`** (gamma): **Factor de descuento** = 0.9
  - Importancia de recompensas futuras vs inmediatas
  - 0.9 = el león valora mucho las consecuencias futuras
  
- **`r`**: **Recompensa inmediata** obtenida
  - +100 por captura exitosa
  - -50 por fracaso
  - +1 por acercarse
  
- **`s'`**: **Nuevo estado** después de la acción
- **`max Q(s',a')`**: Mejor valor Q posible en el nuevo estado
  - Estimación del valor futuro óptimo

#### Interpretación Intuitiva

La ecuación dice: *"El valor de tomar la acción A en el estado S es la recompensa inmediata más el mejor valor que puedo obtener en el futuro, ajustado por lo que ya sabía"*.

### Política Epsilon-Greedy

El león balancea **exploración** vs **explotación** mediante epsilon (ε):

```python
if random() < epsilon:
    acción = aleatoria()  # EXPLORAR: probar algo nuevo
else:
    acción = mejor_conocida()  # EXPLOTAR: usar lo aprendido
```

**Decaimiento de Epsilon:**
- Inicio: ε = 1.0 (100% exploración)
- Decremento: ε -= 0.9/episodios_totales
- Final: ε = 0.1 (10% exploración, 90% explotación)

Esto significa que el león empieza probando todo aleatoriamente, y gradualmente confía más en su experiencia.

### Representación de Estados

Cada estado captura la situación completa del mundo:

```python
Estado = {
    'posicion_leon': int,           # 1-8 (posición discreta)
    'distancia_impala': float,      # Redondeada a 0.5 unidades
    'accion_impala': str,           # 'ver_izq', 'ver_der', 'beber', etc.
    'leon_escondido': bool,         # ¿León oculto?
    'impala_puede_ver': bool        # ¿Impala puede ver al león?
}
```

La tabla Q almacena valores para cada combinación posible de (Estado, Acción).

### Ejemplo de Aprendizaje

**Episodio 1** (sin experiencia):
```
Estado: León en pos 1, distancia 9.5, impala bebiendo
Q(estado, atacar) = 0 (valor inicial)
Acción: Atacar (aleatorio)
Resultado: Impala detecta y escapa (-50)
Actualización: Q(estado, atacar) = -2.5 (ahora sabe que atacar lejos es malo)
```

**Episodio 1000** (con experiencia):
```
Estado: León en pos 1, distancia 9.5, impala bebiendo
Q(estado, esconderse) = 45 (mejor opción conocida)
Q(estado, avanzar) = 30
Q(estado, atacar) = -2.5 (ya aprendió que es mala idea)
Acción: Esconderse (explota conocimiento)
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

## 🧪 Tests Unitarios

El proyecto incluye una suite completa de tests que valida todas las funciones críticas del sistema.

### Ejecutar Tests

```bash
# Ejecutar suite completa de tests
python tests/test_basico.py
```

### Tests Incluidos

#### 1. **Test de Abrevadero** ✅
- Validación de coordenadas de las 8 posiciones
- Cálculo correcto de distancias
- Verificación del RADIO = 9.5 unidades

#### 2. **Test de Acciones del León** ✅
- Avanzar: Movimiento de 1 cuadro/turno
- Esconderse: Cambio de estado de visibilidad
- Atacar: Velocidad de 2 cuadros/turno

#### 3. **Test de Acciones del Impala** ✅
- Ver (izquierda, derecha, frente)
- Beber agua
- Huir con aceleración progresiva

#### 4. **Test de Base de Conocimientos** ✅
- Almacenamiento de estados y valores Q
- Recuperación de mejores acciones
- Actualización de tabla Q

#### 5. **Test de Q-Learning** ✅
- Selección de acciones (exploración vs explotación)
- Política epsilon-greedy
- Validación de tipos de decisión

#### 6. **Test de Sistema de Recompensas** ✅
- Recompensa por éxito: +100
- Penalización por fracaso: -50
- Recompensas por acercamiento

#### 7. **Test de Cacería Completa** ✅
- Ejecución completa de una cacería
- Validación de resultados (éxito/fracaso)
- Estrategia simple de prueba

#### 8. **Test de Cacería Turno a Turno** ✅
- Ejecución de turnos individuales
- Registro de eventos en el tiempo
- Verificación de historial

### Resultados Esperados

```
Ejecutando tests básicos...

✓ Abrevadero - Coordenadas
✓ Abrevadero - Distancia
✓ León - Acciones
✓ Impala - Acciones
✓ Base Conocimientos
✓ Q-Learning - Selección
✓ Sistema Recompensas
✓ Cacería Completa
✓ Cacería Turno a Turno

==================================================
Resultados: 9 exitosos, 0 fallidos
==================================================
```

### Cobertura

Los tests cubren:
- ✅ **Entorno**: Coordenadas, distancias, geometría
- ✅ **Agentes**: Todas las acciones de león e impala
- ✅ **Aprendizaje**: Q-Learning, recompensas, estados
- ✅ **Simulación**: Cacerías completas y por turnos
- ✅ **Conocimiento**: Almacenamiento y recuperación

### Generalización

El sistema abstrae estados específicos en **patrones generales**:

- Distancias se redondean a 0.5 cuadros
- Estados similares comparten conocimiento
- Tabla Q más compacta y eficiente

## 🌍 Entorno de Simulación

### Sistema de Coordenadas Polares

El proyecto utiliza **coordenadas polares** para representar las posiciones del león alrededor del abrevadero, lo cual es más natural para este escenario circular.

#### ¿Por qué Coordenadas Polares?

En lugar de usar coordenadas cartesianas tradicionales (x, y), usamos **coordenadas polares (r, θ)**:

- **`r`** (radio): Distancia desde el centro del abrevadero
- **`θ`** (theta): Ángulo en grados (0° = Norte)

**Ventajas para este problema:**

1. **Naturalidad del escenario**: El abrevadero es circular, el león rodea al impala
2. **Simplificación de cálculos**: Las 8 posiciones iniciales están a la misma distancia (r = 9.5)
3. **Movimiento intuitivo**: Avanzar = reducir r (acercarse al centro)
4. **Representación compacta**: Solo necesitamos ángulo y distancia

#### Las 8 Posiciones Iniciales

El león puede empezar en 8 posiciones equidistantes alrededor del abrevadero:

```
                    Posición 1
                      θ = 0°
                      Norte
                        🦁
                        |
                        |
    Pos 8              |              Pos 2
    θ=315°             |              θ=45°
    Noroeste -------(CENTRO)------- Noreste
                    IMPALA🦌
                        |
    Pos 7              |              Pos 3
    θ=270°             |              θ=90°
    Oeste ----------(CENTRO)--------- Este
                        |
                        |
                    Posición 5
                      θ=180°
                       Sur
                    Pos 4  Pos 6
                   θ=135° θ=225°
```

**Fórmula de conversión:**
```python
θ = (posicion - 1) × 45°

Posición 1: θ = 0°    (Norte)
Posición 2: θ = 45°   (Noreste)
Posición 3: θ = 90°   (Este)
...
Posición 8: θ = 315°  (Noroeste)
```

#### Conversión Polar → Cartesiana

Para la visualización en el grid 19×19, convertimos coordenadas polares a cartesianas:

```python
x = r × sin(θ)
y = r × cos(θ)

# Ejemplo Posición 1 (Norte):
r = 9.5, θ = 0°
x = 9.5 × sin(0°) = 0
y = 9.5 × cos(0°) = 9.5
Coordenadas: (0, 9.5)

# Ejemplo Posición 3 (Este):
r = 9.5, θ = 90°
x = 9.5 × sin(90°) = 9.5
y = 9.5 × cos(90°) = 0
Coordenadas: (9.5, 0)
```

#### Movimiento del León

Cuando el león **avanza** o **ataca**, se mueve en línea recta hacia el centro:

```python
# Avanzar 1 cuadro:
nueva_r = r - 1
nueva_θ = θ  # El ángulo se mantiene

# Ejemplo: León en pos 1, avanza 3 turnos
Turno 0: r=9.5, θ=0° → (0, 9.5)
Turno 1: r=8.5, θ=0° → (0, 8.5)  # Avanzó 1
Turno 2: r=7.5, θ=0° → (0, 7.5)  # Avanzó 1
Turno 3: r=6.5, θ=0° → (0, 6.5)  # Avanzó 1
```

#### Visualización en Grid 19×19

El grid usa coordenadas cartesianas para facilitar la visualización:

- **Centro del grid**: (9.5, 9.5)
- **Escala**: 1.9 (factor de conversión polar → grid)
- **Origen polar** (0, 0) → **Centro grid** (9.5, 9.5)

```
Grid Cartesiano 19×19:
┌─────────────────────┐
│ · · · · · 🦁 · · · · │  ← León en (9.5, 18.05)
│ · · · · · · · · · · │     Polar: r=9.5, θ=0°
│ · · · · · · · · · · │
│ · · · · · · · · · · │
│ · · · · ▓▓▓ · · · · │  ← Abrevadero
│ · · · · ▓🦌▓ · · · · │     Centro (9.5, 9.5)
│ · · · · ▓▓▓ · · · · │
│ · · · · · · · · · · │
└─────────────────────┘
```

### Abrevadero

- **Grid**: 19×19 cuadros
- **Centro**: (9.5, 9.5) - Posición del abrevadero
- **RADIO**: 9.5 cuadros - Distancia inicial león-impala
- **Coordenadas**: Polares (r, θ) para el león, Cartesianas (x, y) para visualización

### Cálculo de Distancias

La distancia león-impala se calcula con la **fórmula euclidiana**:

```python
# Si león está en (x_leon, y_leon) e impala en centro (0, 0)
distancia = √(x_leon² + y_leon²)

# En coordenadas polares es simplemente:
distancia = r  (el radio actual del león)
```

**Umbral de captura:** distancia ≤ 0.5 unidades

## 📋 Reglas del Sistema



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
