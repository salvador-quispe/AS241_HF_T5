# Guía de Conexión Frontend — Módulo Habilidades Digitales

## URL base de la API

```
http://localhost:8000
```

> Para producción reemplaza `localhost:8000` por la URL del servidor desplegado.

---

## Endpoints disponibles

### Dashboard completo
```
GET /api/habilidades-digitales/dashboard
```
Retorna todo en una sola llamada. Ideal para cargar la página inicial.

```json
{
  "indicadores_kpi": { ... },
  "herramientas_ofimaticas": [ ... ],
  "plataformas_lenguajes": [ ... ],
  "estudiantes_habilidades": [ ... ],
  "conclusiones_modulo": "...",
  "acciones_recomendadas": [ ... ],
  "proxima_evaluacion": "15 OCT 2026"
}
```

---

### KPI — Tarjetas superiores del dashboard
```
GET /api/habilidades-digitales/kpi
```
```json
{
  "dominio_promedio": 3.5,
  "capacitacion_completada": 87.0,
  "uso_diario_promedio": 6.8,
  "alertas_nivel_bajo": 4,
  "total_estudiantes": 65
}
```
| Campo | Tarjeta en el dashboard |
|-------|------------------------|
| `dominio_promedio` | Dominio Promedio X.X/5.0 |
| `capacitacion_completada` | Capacitación Completada XX% |
| `uso_diario_promedio` | Uso Diario Promedio X.X hrs |
| `alertas_nivel_bajo` | Alertas de Nivel Bajo XX |

---

### Herramientas ofimáticas — Barras de progreso
```
GET /api/habilidades-digitales/herramientas-ofimaticas
```
```json
[
  {
    "herramienta": "Excel o Google Sheets",
    "categoria": "Ofimática",
    "porcentaje_dominio": 78.0,
    "nivel_promedio": 3.9,
    "estudiantes_usan": 53
  }
]
```
Usar `porcentaje_dominio` para el ancho de las barras de progreso.

---

### Plataformas y lenguajes — Tabla con dominio
```
GET /api/habilidades-digitales/plataformas-lenguajes
```
```json
[
  {
    "categoria": "Git / GitHub",
    "dominio": 3,
    "capacitacion": "Si",
    "nivel_texto": "Intermedio",
    "estudiantes": 45
  }
]
```
Usar `dominio` (1-5) para los puntos de nivel visual y `capacitacion` para el badge Si/No.

---

### Estudiantes — Tabla de desglose
```
GET /api/habilidades-digitales/estudiantes?limit=10
```
Parámetro opcional: `limit` (1-50, default 10)

```json
[
  {
    "expediente": "VG-2024-001",
    "estudiante": "ALVARADO, CARLOS",
    "ofimatica": 4.8,
    "programacion": 3.2,
    "frecuencia_hrs": 8.5,
    "estado": "COMPETENTE"
  }
]
```

---

### Conclusiones y acciones
```
GET /api/habilidades-digitales/conclusiones
GET /api/habilidades-digitales/acciones-recomendadas
GET /api/habilidades-digitales/proxima-evaluacion
```

---

## Cómo conectarse desde el frontend

### JavaScript / Fetch
```javascript
const API = "http://localhost:8000/api/habilidades-digitales";

// Cargar KPIs
const kpi = await fetch(`${API}/kpi`).then(r => r.json());

// Cargar dashboard completo
const dashboard = await fetch(`${API}/dashboard`).then(r => r.json());
```

### Axios
```javascript
import axios from "axios";

const api = axios.create({ baseURL: "http://localhost:8000/api/habilidades-digitales" });

const { data: kpi }         = await api.get("/kpi");
const { data: herramientas } = await api.get("/herramientas-ofimaticas");
const { data: estudiantes }  = await api.get("/estudiantes?limit=20");
```

### React — ejemplo de hook
```javascript
import { useEffect, useState } from "react";

export function useDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/habilidades-digitales/dashboard")
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false); });
  }, []);

  return { data, loading };
}
```

---

## Estados y colores

| Estado | Color hex | Criterio |
|--------|-----------|----------|
| EXCELENTE | `#2ecc71` | promedio >= 4.5 |
| COMPETENTE | `#3498db` | promedio >= 3.5 |
| REGULAR | `#f39c12` | promedio >= 2.5 |
| EN FORMACIÓN | `#e74c3c` | promedio < 2.5 |

---

## Paleta de colores Valle Grande

```
Primario:   #1a3a6b   (azul oscuro — headers, sidebar)
Secundario: #f0a500   (amarillo — botones, alertas)
Fondo:      #f4f6f9   (gris claro — background)
Texto:      #2c3e50   (gris oscuro — texto general)
```

---

## CORS

El backend ya tiene CORS habilitado para `*`.
No necesitas configuración adicional en el frontend para desarrollo local.

---

## Documentación interactiva

```
http://localhost:8000/docs    → Swagger UI (probar endpoints)
http://localhost:8000/redoc   → ReDoc (lectura)
```
