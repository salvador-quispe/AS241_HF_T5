# Guía de Diseño Frontend — Módulo Habilidades Digitales

## Configuración de datos

```env
# Google Sheet (fuente de datos en tiempo real)
GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/e/2PACX-1vSBNPpHFjJU7QmGpDNwIP7TfkLE8B0hgSlISuUUjKtVrbTXQhgLRFo72YypW4yf6g7s2v3K0lJgGUQK/pub?gid=1157215314&single=true&output=csv

# API Backend
API_BASE_URL=http://localhost:8000/api/v1
CACHE_TTL_SECONDS=30
```

---

## Endpoints disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/habilidades-digitales/metricas` | GET | Métricas generales del módulo |
| `/habilidades-digitales/herramientas/estadisticas` | GET | Stats por herramienta |
| `/habilidades-digitales/estudiantes/resumen` | GET | Tabla de estudiantes con estado |
| `/habilidades-digitales/estudiantes/{dni}` | GET | Detalle por DNI |
| `/habilidades-digitales/sincronizar-sheet` | POST | Sincronizar desde Google Sheet |

---

## Estructura del dashboard (referencia visual)

```
┌─────────────────────────────────────────────────────┐
│  MÓDULO: HABILIDADES DIGITALES        [Buscar DNI]  │
├──────────┬──────────────┬─────────────┬─────────────┤
│ Dominio  │ Capacitación │ Uso Diario  │  Alertas    │
│ Promedio │  Completada  │  Promedio   │ Nivel Bajo  │
│  X.X/5.0 │    XX%       │   X.X hrs   │     XX      │
├──────────┴──────────────┴─────────────┴─────────────┤
│ DOMINIO DE HERRAMIENTAS        │ PLATAFORMAS         │
│ ─────────────────────────────  │ ─────────────────── │
│ Excel / Google Sheets   [███] │ Herramienta│Dom│Cap │
│ Word / Google Docs      [███] │ Git/GitHub │ █ │ Si │
│ Editor de Código        [██ ] │ Bases Datos│ █ │ Si │
│ Git / GitHub            [██ ] │ IA Tools   │ █ │ No │
│ Herramientas de IA      [█  ] │                     │
├────────────────────────────────────────────────────-┤
│ DESGLOSE POR ESTUDIANTE              [Filtros]       │
│ DNI │ Semestre │ Dominio │ Frecuencia │ Estado       │
│ ... │   ...    │   ...   │    ...     │ [Competente] │
└─────────────────────────────────────────────────────┘
```

---

## Respuestas de la API

### GET /metricas
```json
{
  "dominio_promedio": 3.5,
  "porcentaje_con_formacion": 87.0,
  "total_estudiantes": 65,
  "alertas_nivel_bajo": 4
}
```

### GET /herramientas/estadisticas
```json
[
  { "herramienta": "Excel / Google Sheets", "porcentaje_uso": 78.0, "dominio_promedio": 3.2 },
  { "herramienta": "Editor de Código",      "porcentaje_uso": 72.0, "dominio_promedio": 3.5 },
  { "herramienta": "Herramientas de IA",    "porcentaje_uso": 65.0, "dominio_promedio": 2.8 },
  { "herramienta": "Git / GitHub",          "porcentaje_uso": 60.0, "dominio_promedio": 3.1 },
  { "herramienta": "Bases de Datos",        "porcentaje_uso": 55.0, "dominio_promedio": 3.0 },
  { "herramienta": "Word / Google Docs",    "porcentaje_uso": 50.0, "dominio_promedio": 3.8 }
]
```

### GET /estudiantes/resumen
```json
[
  {
    "dni": "61525749",
    "semestre": "1° Semestre",
    "nivel_dominio": 2,
    "frecuencia_uso": "frecuentemente",
    "tiene_formacion": true,
    "herramientas_count": 3,
    "estado": "Regular"
  }
]
```

---

## Estados y colores sugeridos

| Estado | Color | Criterio |
|--------|-------|----------|
| Excelente | `#2ecc71` verde | score >= 4.5 |
| Competente | `#3498db` azul | score >= 3.5 |
| Regular | `#f39c12` amarillo | score >= 2.5 |
| En Observación | `#e74c3c` rojo | score < 2.5 |

---

## Paleta de colores (Valle Grande)

```
Primario:    #1a3a6b  (azul oscuro)
Secundario:  #f0a500  (amarillo/dorado)
Fondo:       #f4f6f9
Texto:       #2c3e50
Éxito:       #2ecc71
Alerta:      #e74c3c
```

---

## Filtros disponibles en la tabla

- `semestre` — `1° Semestre`, `5° Semestre`, `6° Semestre`
- `nivel_dominio_min` — 1 a 5
- `tiene_formacion` — `true` / `false`
