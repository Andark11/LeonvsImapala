# 🦁 León vs Impala - Q-Learning

Sistema de aprendizaje por refuerzo donde un león aprende a cazar un impala mediante **Q-Learning**. El león aprende únicamente por experiencia, sin estrategias preprogramadas.

[![Python3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🎯 Características

- ✅ **Q-Learning** con exploración epsilon-greedy
- ✅ **Visualización ASCII** en terminal (Grid 19×19)
- ✅ **Coordenadas polares** para movimiento natural
- ✅ **11 constantes de recompensa** ajustables
- ✅ **Persistencia JSON** de modelos entrenados
- ✅ **9 tests unitarios** completos
- ✅ **Sin dependencias externas** (solo stdlib Python)

## 🚀 Instalación

```bash
# Clonar repositorio
git clone https://github.com/Andark11/LeonvsImapala.git
cd LeonvsImapala

# Verificar Python 3.8+
python --version

# Ejecutar
python main.py
```

## 📖 Uso

**Entrenar modelo:**
```bash
python main.py
# Opción 1: Entrenar nuevo modelo
# Episodios recomendados: 100,000
```

**Visualizar cacería:**
```bash
python main.py
# Opción 2: Simulación visual paso a paso
```

**Ejecutar tests:**
```bash
python tests/test_basico.py
```

## 🧠 Q-Learning

### Ecuación de Bellman
```
Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',a') - Q(s,a)]
```

**Parámetros:**
- α = 0.05 (tasa de aprendizaje)
- γ = 0.9 (factor de descuento)
- ε = 1.0 → 0.1 (exploración decreciente)

## 🎮 Acciones

### León (4 acciones)
- **AVANZAR**: 1 cuadro/turno (movimiento sigiloso)
- **ESCONDERSE**: Invisible para el impala
- **ATACAR**: 2 cuadros/turno (sprint final)
- **SITUARSE**: Cambiar posición inicial

### Impala (5 acciones)
- **VER_IZQUIERDA/DERECHA/FRENTE**: Cono visión 120°
- **BEBER_AGUA**: Vulnerable (no ve al león)
- **HUIR**: Aceleración 1→2→3... cuadros/turno

## ⚖️ Sistema de Recompensas

| Evento | Valor |
|--------|-------|
| Éxito cacería | +100.0 |
| Fracaso cacería | -50.0 |
| Acercamiento | +1.0/cuadro |
| Alejamiento | -2.0/cuadro |
| Detección temprana | -5.0 a -10.0 |
| Tiempo excesivo | -0.1/turno |
| Buen uso esconderse | +2.0 |
| Mal uso esconderse | -1.0 |
| Ataque cercano (≤2) | +5.0 |
| Ataque lejano (>3) | -3.0 |

## 🌍 Coordenadas Polares

```
        N (0°)
         |
    8    1    2
     \   |   /
  7 -- AB -- 3
     /   |   \
    6    5    4
         |
       S (180°)
```

- **AB**: Abrevadero (centro)
- **RADIO**: 9.5 unidades
- **Conversión**: x = r·sin(θ), y = r·cos(θ)

## 📁 Estructura

```
LeonvsImapala/
├── main.py              # Punto de entrada
├── environment.py       # Sistema de coordenadas
├── agents/             # León e impala
├── simulation/         # Motor de cacería
├── learning/           # Q-Learning y recompensas
├── knowledge/          # Base de conocimientos
├── storage/            # Persistencia JSON
├── ui/                 # Interfaces
├── tests/              # Tests unitarios
├── modelos/            # Modelos entrenados
└── docs/               # Documentación LaTeX (67 págs)
```

## 📊 Resultados

**Modelo EM4 (100,000 episodios):**
- Tasa de éxito: **10.45%**
- Tiempo: ~15 minutos
- Experiencias: 145,135 únicas

**Progresión:**
- 1K episodios → 3-4% éxito
- 10K episodios → 6-8% éxito
- 100K episodios → 10-12% éxito

## 🧪 Tests

9 tests unitarios (100% pasando):
- Coordenadas polares y distancias
- Acciones de león e impala
- Q-Learning y epsilon-greedy
- Sistema de recompensas
- Cacería completa end-to-end

## 🔧 Configuración

**Ajustar parámetros Q-Learning** (`learning/q_learning.py`):
```python
alpha = 0.05      # Tasa de aprendizaje
gamma = 0.9       # Factor de descuento
epsilon = 1.0     # Exploración inicial
```

**Ajustar recompensas** (`learning/recompensas.py`):
```python
EXITO_CACERIA = 100.0
FRACASO_CACERIA = -50.0
# ... más constantes
```

## �� Documentación

Documentación académica completa en LaTeX (67 páginas):
```bash
cd docs
xdg-open main.pdf
```

**Contenido:** 6 capítulos + 3 apéndices con código, instalación y análisis de resultados.

## 👨‍💻 Autores

**Proyecto Final - Sistemas Inteligentes**

**Integrantes:**
- Alvarado Martínez Miguel Eduardo
- García Retana Alba Sughey
- Soria Cabrera Andrés
- Sosa Pérez Dariana Montserrat

**Profesor:** Rosas Hernández Javier  
**Grupo:** 1754  
**Institución:** FES Acatlán, UNAM

## 📄 Licencia

Todos los derechos reservados.

---

**Versión:** 1.0.0 | **Fecha:** Diciembre 2025 | **Repositorio:** [github.com/Andark11/LeonvsImapala](https://github.com/Andark11/LeonvsImapala)
