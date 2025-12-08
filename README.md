# 🦁 León vs Impala - Q-Learning

Sistema de aprendizaje por refuerzo donde un león aprende a cazar un impala mediante **Q-Learning**. El león no tiene estrategia programada, sino que aprende por experiencia tras miles de cacerías simuladas.

[![Python3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License:MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Características

- ✅ **Q-Learning** con exploración epsilon-greedy
- ✅ **Visualización ASCII** en terminal (Grid 19×19)
- ✅ **Coordenadas polares** para movimiento natural
- ✅ **Persistencia** de modelos entrenados
- ✅ **Tests unitarios** completos (9/9 pasando)

## 🚀 Inicio Rápido

\`\`\`bash
# Clonar repositorio
git clone https://github.com/Andark11/LeonvsImapala.git
cd LeonvsImapala

# Ejecutar
python main.py
\`\`\`

**Requisitos:** Python 3.8+ (sin dependencias externas)

## 📖 Uso

### 1. Entrenar un León

\`\`\`bash
python main.py
# Seleccionar: 1 (Sistema de Entrenamiento)
# Episodios recomendados: 100,000
# Guardar modelo con nombre descriptivo
\`\`\`

**Resultados típicos:**
- 10,000 episodios → 6-8% éxito
- 100,000 episodios → 10-12% éxito

### 2. Visualizar Cacería

\`\`\`bash
python main.py
# Seleccionar: 2 (Simulación Visual)
# Elegir modelo entrenado
# Ver cacería en grid 19×19
\`\`\`

### 3. Ejecutar Tests

\`\`\`bash
python tests/test_basico.py
# Resultado: 9/9 tests pasando ✓
\`\`\`

## 🧠 Q-Learning Explicado

### ¿Qué es el Modelo Q-Learning?

**Q-Learning** es un algoritmo de **Aprendizaje por Refuerzo** (Reinforcement Learning) que permite a un agente (el león) aprender la mejor acción a tomar en cada situación sin necesidad de un modelo explícito del entorno.

#### Concepto del Modelo

El modelo consiste en una **Tabla Q** que almacena valores Q(s,a) para cada combinación de:
- **Estado (s)**: Situación actual del mundo (posición león, distancia impala, visibilidad, etc.)
- **Acción (a)**: Movimiento posible (avanzar, esconderse, atacar)

**Valor Q(s,a)**: Representa "qué tan bueno" es tomar la acción `a` en el estado `s`. Un valor alto indica que históricamente esa acción ha llevado a buenos resultados.

#### Tabla Q - Estructura

\`\`\`python
# Ejemplo de Tabla Q después de 1000 episodios
Q = {
    Estado(pos=1, dist=9.5, impala_bebe=True, escondido=False): {
        'avanzar': 45.2,      # Buena opción
        'esconderse': 58.7,   # Mejor opción (valor más alto)
        'atacar': -15.3       # Mala opción (demasiado lejos)
    },
    Estado(pos=1, dist=2.0, impala_bebe=True, escondido=True): {
        'avanzar': 35.8,
        'esconderse': 12.1,
        'atacar': 78.5        # Mejor opción (cerca y escondido)
    }
}
\`\`\`

### La Ecuación de Bellman

El león aprende actualizando los valores Q mediante la **ecuación de Bellman**:

\`\`\`
Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',a') - Q(s,a)]
\`\`\`

**Desglose de la ecuación:**

1. **Q(s,a)**: Valor Q actual que queremos actualizar
2. **α (alpha)** = 0.05: **Tasa de aprendizaje**
   - Controla qué tan rápido se actualizan los valores
   - Valor bajo (0.05) = aprendizaje gradual y estable
   - Evita cambios bruscos por experiencias aisladas

3. **r**: **Recompensa inmediata** obtenida
   - +100 puntos: Cacería exitosa (capturó al impala)
   - -50 puntos: Fracaso (impala escapó)
   - +1 punto: Por cada cuadro que se acercó
   - -10 puntos: Si el impala detecta al león prematuramente

4. **γ (gamma)** = 0.9: **Factor de descuento**
   - Importancia de recompensas futuras vs inmediatas
   - 0.9 = valora mucho las consecuencias a largo plazo
   - Más cercano a 1 = más "visionario"

5. **max Q(s',a')**: **Mejor valor Q futuro**
   - Mejor acción posible en el nuevo estado s'
   - Estimación del valor futuro óptimo
   - Guía hacia decisiones que maximizan recompensa total

6. **[r + γ·max Q(s',a') - Q(s,a)]**: **Error de predicción**
   - Diferencia entre lo esperado y lo obtenido
   - Si es positivo: la acción fue mejor de lo esperado
   - Si es negativo: fue peor de lo esperado

#### Interpretación Intuitiva

La ecuación dice: *"El valor de tomar la acción A en el estado S es mi estimación actual más un ajuste basado en lo que realmente pasó (recompensa inmediata + mejor futuro posible)"*

### Ejemplo de Aprendizaje

**Episodio 1** (sin experiencia):
\`\`\`
Estado: León en pos 1, distancia 9.5, impala bebiendo
Q inicial: Q(estado, atacar) = 0

León toma acción: ATACAR (aleatorio, no sabe que es malo)
Resultado: Impala detecta el sonido y escapa
Recompensa: r = -50

Actualización:
Q(estado, atacar) = 0 + 0.05[-50 + 0 - 0]
Q(estado, atacar) = -2.5

🧠 Aprendió: "Atacar desde lejos es muy mala idea"
\`\`\`

**Episodio 100** (con experiencia):
\`\`\`
Mismo estado: León en pos 1, distancia 9.5, impala bebiendo
Q actual: Q(estado, esconderse) = 45.0 (mejor opción conocida)

León toma acción: ESCONDERSE (explota conocimiento)
Resultado: No es detectado, puede acercarse después
Recompensa: r = +5 (bono por estrategia)

Actualización:
Q(estado, esconderse) = 45 + 0.05[5 + 0.9(50) - 45]
Q(estado, esconderse) = 45 + 0.05[5 + 45 - 45]
Q(estado, esconderse) = 45.25

🧠 Reforzó: "Esconderse desde lejos funciona bien"
\`\`\`

### Proceso de Aprendizaje

1. **Exploración** → Prueba acciones aleatorias para descubrir
2. **Experiencia** → Acumula resultados (estado → acción → recompensa → nuevo estado)
3. **Actualización** → Mejora valores Q con la ecuación de Bellman
4. **Explotación** → Usa conocimiento aprendido (elige acciones con Q alto)
5. **Convergencia** → Después de miles de episodios, desarrolla estrategia óptima

### Política Epsilon-Greedy

Balancea **exploración** (descubrir) vs **explotación** (usar lo aprendido):

\`\`\`python
if random() < epsilon:
    acción = aleatoria()      # EXPLORAR: probar algo nuevo
else:
    acción = argmax(Q[estado])  # EXPLOTAR: mejor acción conocida
\`\`\`

**Decaimiento de epsilon:**
- Inicio: ε = 1.0 (100% exploración - el león no sabe nada)
- Decremento: ε -= 0.9/episodios_totales (decrece gradualmente)
- Final: ε = 0.1 (90% explotación, 10% exploración - el león usa su experiencia pero sigue probando cosas nuevas ocasionalmente)

## 🌍 Coordenadas Polares

### ¿Qué son las Coordenadas Polares?

En lugar de usar coordenadas cartesianas (x, y), las coordenadas polares definen un punto mediante:
- **r (radio)**: Distancia desde el centro (el abrevadero)
- **θ (theta)**: Ángulo desde el norte (0° = Norte, aumenta en sentido horario)

### Diagrama del Sistema

\`\`\`
        N (0°)
         |
    8    1    2
     \   |   /
315° \  0°  / 45°
      \ | /
  W -- AB -- E
      / | \
270° /  |  \ 90°
    /   |   \
    7   6   5
        |
       S (180°)
        
Posiciones:
1 = Norte (N)      - 0°
2 = Noreste (NE)   - 45°
3 = Este (E)       - 90°
4 = Sureste (SE)   - 135°
5 = Sur (S)        - 180°
6 = Suroeste (SO)  - 225°
7 = Oeste (O)      - 270°
8 = Noroeste (NO)  - 315°
AB = Abrevadero    - Centro (0, 0)
\`\`\`

### Cálculo de Ángulo desde Posición

**Fórmula:**
\`\`\`python
θ = (posición - 1) × 45°
\`\`\`

**Ejemplos:**
\`\`\`
posición 1 (Norte):     θ = (1-1) × 45° = 0°
posición 2 (Noreste):   θ = (2-1) × 45° = 45°
posición 3 (Este):      θ = (3-1) × 45° = 90°
posición 5 (Sur):       θ = (5-1) × 45° = 180°
posición 7 (Oeste):     θ = (7-1) × 45° = 270°
posición 8 (Noroeste):  θ = (8-1) × 45° = 315°
\`\`\`

### Conversión Polar → Cartesiano

Para convertir coordenadas polares (r, θ) a coordenadas cartesianas (x, y):

**Fórmulas:**
\`\`\`python
x = r × sin(θ)
y = r × cos(θ)
\`\`\`

**Ejemplos con RADIO = 9.5:**

#### Posición 1 (Norte, θ=0°):
\`\`\`python
x = 9.5 × sin(0°) = 9.5 × 0 = 0.0
y = 9.5 × cos(0°) = 9.5 × 1 = 9.5
→ Coordenadas: (0.0, 9.5)
\`\`\`

#### Posición 2 (Noreste, θ=45°):
\`\`\`python
x = 9.5 × sin(45°) = 9.5 × 0.707 = 6.72
y = 9.5 × cos(45°) = 9.5 × 0.707 = 6.72
→ Coordenadas: (6.72, 6.72)
\`\`\`

#### Posición 3 (Este, θ=90°):
\`\`\`python
x = 9.5 × sin(90°) = 9.5 × 1 = 9.5
y = 9.5 × cos(90°) = 9.5 × 0 = 0.0
→ Coordenadas: (9.5, 0.0)
\`\`\`

#### Posición 5 (Sur, θ=180°):
\`\`\`python
x = 9.5 × sin(180°) = 9.5 × 0 = 0.0
y = 9.5 × cos(180°) = 9.5 × (-1) = -9.5
→ Coordenadas: (0.0, -9.5)
\`\`\`

#### Posición 7 (Oeste, θ=270°):
\`\`\`python
x = 9.5 × sin(270°) = 9.5 × (-1) = -9.5
y = 9.5 × cos(270°) = 9.5 × 0 = 0.0
→ Coordenadas: (-9.5, 0.0)
\`\`\`

### Cálculo de Distancia

Para calcular la distancia entre dos puntos en coordenadas cartesianas:

**Fórmula de distancia euclidiana:**
\`\`\`python
d = √[(x₂ - x₁)² + (y₂ - y₁)²]
\`\`\`

#### Ejemplo: Distancia desde León (pos 1) hasta Abrevadero

\`\`\`python
# León en posición 1 (Norte)
león_x = 0.0
león_y = 9.5

# Abrevadero en el centro
abrevadero_x = 0.0
abrevadero_y = 0.0

# Distancia
d = √[(0.0 - 0.0)² + (0.0 - 9.5)²]
d = √[0 + 90.25]
d = √90.25
d = 9.5 unidades ✓
\`\`\`

#### Ejemplo: Distancia entre León (pos 1) e Impala (pos 5)

\`\`\`python
# León en posición 1 (Norte): (0.0, 9.5)
# Impala en posición 5 (Sur): (0.0, -9.5)

d = √[(0.0 - 0.0)² + (-9.5 - 9.5)²]
d = √[0 + (-19)²]
d = √361
d = 19.0 unidades (diámetro completo)
\`\`\`

### Conversión a Grid ASCII

Para visualización en terminal, se convierte a un grid 19×19:

**Fórmula:**
\`\`\`python
ESCALA = 1.9
grid_x = int(x_cartesiano * ESCALA) + 9  # +9 para centrar (grid 0-18)
grid_y = int(y_cartesiano * ESCALA) + 9
\`\`\`

**Ejemplo - León en posición 1:**
\`\`\`python
# Coordenadas cartesianas: (0.0, 9.5)
grid_x = int(0.0 × 1.9) + 9 = 0 + 9 = 9
grid_y = int(9.5 × 1.9) + 9 = 18 + 9 = 27 → ajustado a 18 (límite grid)

# En el grid ASCII, el león aparece en columna 9, fila superior
\`\`\`

### Ventajas del Sistema Polar

- **Natural para escenario circular**: El abrevadero es el centro natural
- **Simplifica cálculos de distancia**: Solo necesitamos el radio
- **Movimiento intuitivo**: Avanzar = reducir r (acercarse al centro)
- **8 direcciones claras**: Posiciones cardinales fáciles de entender

### Parámetros del Sistema

- **RADIO** = 9.5 unidades (distancia inicial león-impala desde el abrevadero)
- **ESCALA** = 1.9 (factor de conversión a grid ASCII 19×19)
- **Posiciones**: 8 puntos cardinales + 1 centro (abrevadero)
- **Rango ángulos**: 0° a 315° (incrementos de 45°)

## 📁 Estructura

\`\`\`
LeonvsImapala/
├── agents/          # León e Impala
├── simulation/      # Motor de cacería
├── knowledge/       # Base de conocimientos
├── learning/        # Q-Learning y entrenamiento
├── storage/         # Persistencia JSON
├── ui/              # Interfaces (terminal + matplotlib)
├── tests/           # Tests unitarios
├── modelos/         # Modelos entrenados (generados)
├── environment.py   # Abrevadero y coordenadas
└── main.py          # Punto de entrada
\`\`\`

## 🎮 Reglas del Sistema

### Entorno
- **Grid:** 19×19 cuadros
- **RADIO:** 9.5 unidades (distancia inicial león-impala)
- **Captura:** Distancia ≤ 0.5 unidades

### Acciones del León
| Acción | Velocidad | Descripción |
|--------|-----------|-------------|
| Avanzar | 1 cuadro/T | Acercarse sigilosamente |
| Esconderse | 0 cuadros/T | Ocultarse (invisible) |
| Atacar | 2 cuadros/T | Sprint final |

### Comportamiento del Impala
- **Visión:** Cono de 120° (puede rotar)
- **Huida:** Aceleración progresiva (1→2→3→4... cuadros/T)
- **Condiciones de huida:**
  1. Ve al león (no escondido)
  2. León ataca
  3. Distancia < 3 cuadros

## 🧪 Tests Unitarios

\`\`\`bash
✓ Abrevadero - Coordenadas (RADIO=9.5)
✓ Abrevadero - Distancias
✓ León - Acciones (avanzar, esconderse, atacar)
✓ Impala - Acciones (ver, beber, huir)
✓ Base Conocimientos - Tabla Q
✓ Q-Learning - Selección epsilon-greedy
✓ Sistema Recompensas
✓ Cacería Completa - End-to-end
✓ Cacería Turno a Turno
\`\`\`

**Cobertura:** Entorno, agentes, aprendizaje, simulación, conocimiento

## 📊 Resultados

### Modelo EM4 (100,000 episodios)
\`\`\`
Total de cacerías: 100,000
Cacerías exitosas: 10,450
Tasa de éxito: 10.45%
Experiencias únicas: 145,135
Tiempo: ~15 minutos
\`\`\`

### Progresión Típica
| Episodios | Tasa Éxito |
|-----------|------------|
| 1,000 | 3-4% |
| 10,000 | 6-8% |
| 50,000 | 9-10% |
| 100,000 | 10-12% |

## 🔧 Tecnología

- **Python 3.8+** con type hints
- **Q-Learning** (Reinforcement Learning)
- **Sin dependencias** (solo stdlib)
- **JSON** para persistencia
- **ASCII art** para visualización

## 🐛 Troubleshooting

**Error: "El RADIO del modelo no coincide"**
→ Re-entrenar con RADIO=9.5

**El impala siempre escapa**
→ Normal con pocos episodios. Entrenar 100K+

**No se ven colores en terminal**
→ Terminal no soporta ANSI, pero funciona igual

## 📚 Referencias

- Watkins, C.J.C.H. (1989). *Learning from Delayed Rewards*
- Sutton & Barto (2018). *Reinforcement Learning: An Introduction*

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles

## 👨‍💻 Autor

**Proyecto Final - Sistemas Inteligentes**  
Implementación educativa de Q-Learning aplicado a caza predador-presa

---

**Estado:** ✅ Sistema completo y funcional  
**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025
