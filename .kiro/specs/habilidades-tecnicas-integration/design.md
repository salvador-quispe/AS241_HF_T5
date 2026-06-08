# Design Document — Habilidades Técnicas Integration

## Overview

Este documento describe el diseño técnico para integrar el módulo de **Habilidades Técnicas** al proyecto AS241_HF_T5, siguiendo la arquitectura en capas ya establecida por el módulo de Habilidades Blandas.

El script standalone `app/models/habilidades_tecnicas_model.py` ya realiza el análisis completo (descarga CSV, clasifica respuestas con 7 patrones regex, calcula métricas y renderiza un gráfico de dona). Este diseño refactoriza esa lógica en las capas del sistema: **ETL → Repository → Service → Controller + CLI**, sin modificar el script original ni el módulo de Habilidades Blandas.

La fuente de datos es una pestaña distinta de Google Sheets (`gid=1157215314`), accedida mediante el `GoogleSheetsConnector` existente que ya acepta URL arbitraria como parámetro de constructor.

---

## Architecture

```
                        ┌──────────────────────────────┐
                        │   Google Sheets (CSV export) │
                        │   gid=1157215314             │
                        └──────────────┬───────────────┘
                                       │  HTTP GET (pandas read_csv)
                        ┌──────────────▼───────────────┐
                        │   app/utils/                 │
                        │   GoogleSheetsConnector      │  ← sin modificar
                        └──────────────┬───────────────┘
                                       │  pd.DataFrame (todas las columnas)
                        ┌──────────────▼───────────────┐
                        │   app/etl/                   │
                        │   HabilidadesTecnicasETL     │
                        └──────────────┬───────────────┘
                                       │  dataclasses tipadas
                        ┌──────────────▼───────────────┐
                        │   app/repositories/          │
                        │   HabilidadesTecnicasRepo    │  ← caché en memoria
                        └──────────────┬───────────────┘
                                       │  Dict / ETL instance
                        ┌──────────────▼───────────────┐
                        │   app/services/              │
                        │   habilidades_tecnicas       │  ← singleton
                        │   _service.py                │
                        └──────────┬────────┬──────────┘
                                   │        │
              ┌────────────────────▼──┐  ┌──▼──────────────────────┐
              │  app/api/controllers/ │  │  cli.py                 │
              │  Habilidades          │  │  tecnicas               │
              │  TecnicasController   │  │  tecnicas-kpi           │
              │  (FastAPI APIRouter)  │  │  tecnicas-matriz        │
              └───────────────────────┘  │  tecnicas-refresh       │
                                         └─────────────────────────┘
```

**Módulos sin modificar:** `app/utils/google_sheets_connector.py`, `app/models/habilidades_tecnicas_model.py`, toda la pila de Habilidades Blandas.

**Módulos a crear:** `app/etl/habilidades_tecnicas_etl.py`, `app/repositories/habilidades_tecnicas_repository.py`, `app/schemas/habilidades_tecnicas_schema.py`, `app/services/habilidades_tecnicas_service.py`, `app/api/controllers/habilidades_tecnicas_controller.py`.

**Módulos a modificar:** `app/config/database.py`, `app/api/routes/__init__.py`, `main.py`, `cli.py`.

---

## Components and Interfaces

### 1. `app/config/database.py` (modificación)

Añadir `SHEET_URL_TECNICAS = os.getenv("GOOGLE_SHEET_TECNICAS_URL", "")` junto a las constantes existentes.

---

### 2. `app/etl/habilidades_tecnicas_etl.py` (nuevo)

**Constante módulo-nivel `PATRONES_TECNICOS`** (7 entradas, mismo orden que el script original):
1. `"Lógica y Algoritmia (Seudocódigo/Flujograma)"` → `r"logica|lógica|seudocó|pseudocó|flujograma|algorit"`
2. `"Bases de Datos y Análisis (SQL/Sheets)"` → `r"base de datos|bases de datos|sql|mysql|sheets|excel|herramientas avanzadas"`
3. `"Refuerzo General y Práctica Constante"` → `r"seguir practicando|todo de la carrera|practica constante|practca constante|carrera"`
4. `"Desarrollo Frontend (HTML/CSS)"` → `r"html|css|sitios web|frontend|oaginas|paginas"`
5. `"Arquitectura, Backend y DevOps (Docker)"` → `r"arquitectura|backend|docker|kubernetes|distribuid|proyectos backend"`
6. `"Infraestructura, Redes y AWS"` → `r"aws|visual estudio|redes|ciberseguridad"`
7. `"Programación y Código General"` → `r"programac|cód|cod|lenguaje|memoriz|versiones|implementar|tecnic|digital|programas"`

**Las dataclasses se definen directamente en el ETL** (no se importan del script standalone, para evitar sus side-effects: network request, file write, matplotlib). Las clases `ResumenGlobalTecnico`, `SubcategoriaTecnica` y `HabilidadesTecnicasDashboard` se declaran aquí.

**Métodos públicos de `HabilidadesTecnicasETL`:**

| Método | Retorno |
|--------|---------|
| `get_resumen_global()` | `ResumenGlobalTecnico` |
| `get_subcategorias_tecnicas()` | `List[SubcategoriaTecnica]` ordenada desc por votos, solo votos > 0 |
| `get_matriz_operacional()` | `List[SubcategoriaTecnica]` — delega a `get_subcategorias_tecnicas()` |
| `get_complete_dashboard_data()` | `Dict` con claves `resumen_global`, `subcategorias_tecnicas`, `last_updated` |
| `generate_insights()` | `str` con ≥2 observaciones que incluyen valores numéricos |

**Lógica clave:**
- Accede a la columna técnicas con `df.iloc[:, 27]`.
- Si `len(df.columns) < 28` → loguea error, `total_mapeados = 0`, sin excepción.
- Si `total_encuestados == 0` → `porcentaje_impacto_global = 0.0`.
- Si `total_mapeados == 0` → `porcentaje_del_subtotal = 0.0` para todas las categorías.

---

### 3. `app/repositories/habilidades_tecnicas_repository.py` (nuevo)

```python
class HabilidadesTecnicasRepository:
    def __init__(self, google_sheets_url: str):
        self.connector = GoogleSheetsConnector(google_sheets_url)  # instancia propia
        self.etl: Optional[HabilidadesTecnicasETL] = None
        self._cache_valid: bool = False
```

**Diferencia crítica con Blandas:** NO llama `connector.clean_data()`. Pasa el `raw_data` directamente al ETL, que usa `iloc[:, 27]`.

---

### 4. `app/schemas/habilidades_tecnicas_schema.py` (nuevo)

Todos los schemas usan `model_config = ConfigDict(from_attributes=True)` (Pydantic v2).

| Schema | Campos |
|--------|--------|
| `ResumenGlobalTecnicoSchema` | `total_encuestados: int`, `total_mapeados: int`, `porcentaje_impacto_global: float` |
| `SubcategoriaTecnicaSchema` | `categoria: str`, `votos: int`, `porcentaje_del_subtotal: float` |
| `DashboardHabilidadesTecnicasSchema` | `resumen_global`, `subcategorias_tecnicas: List[...]`, `last_updated: str`, `analisis_insights: str` |
| `MatrizOperacionalSchema` | `subcategorias: List[SubcategoriaTecnicaSchema]` |
| `KPITecnicasSchema` | `total_encuestados: int`, `total_mapeados: int`, `porcentaje_impacto_global: float`, `categoria_lider: str` |

---

### 5. `app/services/habilidades_tecnicas_service.py` (nuevo)

Singleton módulo-nivel: `repository = HabilidadesTecnicasRepository(SHEET_URL_TECNICAS)`.

**Lógica de `categoria_lider`:** La subcategoría con mayor `votos`; en empate, la que aparece primero en `PATRONES_TECNICOS`.

**Defaults si repository retorna None:**
- `build_dashboard` → resumen_global zeros, listas vacías, `last_updated=""`, `analisis_insights=""`
- `get_kpi_metrics` → todos 0/0.0, `categoria_lider=""`
- `get_matriz_operacional` → `subcategorias=[]`

---

### 6. `app/api/controllers/habilidades_tecnicas_controller.py` (nuevo)

`router = APIRouter(prefix="/api/habilidades-tecnicas", tags=["Habilidades Técnicas"])`

| Método | Path | Response Model |
|--------|------|----------------|
| `GET` | `/dashboard` | `DashboardHabilidadesTecnicasSchema` |
| `GET` | `/matriz` | `MatrizOperacionalSchema` |
| `GET` | `/kpi` | `KPITecnicasSchema` |
| `POST` | `/reload` | `{"message": str}` |

Cada GET captura excepciones inesperadas → HTTP 500 `{"detail": str(e)}`.

---

### 7. Modificaciones a `app/api/routes/__init__.py`, `main.py`, `cli.py`

- **routes**: `api_router.include_router(tecnicas_router)` junto al blandas_router existente.
- **main.py**: Añadir clave `"habilidades_tecnicas"` con los 4 endpoints en `GET /`.
- **cli.py**: Importar service técnicas con alias; añadir 4 comandos (`tecnicas`, `tecnicas-kpi`, `tecnicas-matriz`, `tecnicas-refresh`); actualizar `show_list()`.

---

## Data Models

Las dataclasses se definen en `app/etl/habilidades_tecnicas_etl.py` para evitar los side-effects del script standalone:

```python
@dataclass
class ResumenGlobalTecnico:
    total_encuestados: int
    total_mapeados: int
    porcentaje_impacto_global: float

    def to_dict(self) -> dict:
        return {
            "total_encuestados": self.total_encuestados,
            "total_mapeados": self.total_mapeados,
            "porcentaje_impacto_global": round(self.porcentaje_impacto_global, 1)
        }

@dataclass
class SubcategoriaTecnica:
    categoria: str
    votos: int
    porcentaje_del_subtotal: float

    def to_dict(self) -> dict:
        return {
            "categoria": self.categoria,
            "votos": self.votos,
            "porcentaje_del_subtotal": round(self.porcentaje_del_subtotal, 1)
        }

@dataclass
class HabilidadesTecnicasDashboard:
    resumen_global: ResumenGlobalTecnico
    subcategorias_tecnicas: List[SubcategoriaTecnica]
    last_updated: str
    analisis_insights: str

    def to_dict(self) -> dict:
        return {
            "resumen_global": self.resumen_global.to_dict(),
            "subcategorias_tecnicas": [s.to_dict() for s in self.subcategorias_tecnicas],
            "last_updated": self.last_updated,
            "analisis_insights": self.analisis_insights
        }
```

---

## Correctness Properties

1. **Independencia de instancias del conector** — Dos `GoogleSheetsConnector` con URLs distintas no comparten estado.
2. **clean_data() preserva exactamente las 8 columnas de blandas** — No afectado por la nueva integración.
3. **Exclusividad mutua del clasificador** — `_clasificador(texto)` retorna exactamente una categoría o `None`.
4. **Invariante: sum(votos) == total_mapeados** — Para cualquier DataFrame con registros mapeados.
5. **Invariante: sum(porcentajes) ≈ 100.0 (±0.5)** — Para cualquier DataFrame con registros mapeados.
6. **Sin excepciones en casos borde** — DataFrame vacío o sin columna 27 → 0.0, sin crash.
7. **Subcategorías ordenadas descendente** — `votos` en orden desc, todos > 0.
8. **get_matriz_operacional ≡ get_subcategorias_tecnicas** — Misma lista, mismo orden.
9. **generate_insights contiene ≥2 valores numéricos**.
10. **to_dict() redondea a 1 decimal** — Para todos los campos float de porcentaje.
11. **categoria_lider respeta orden en empate** — Primera en `PATRONES_TECNICOS`.

---

## Error Handling

| Escenario | Capa | Comportamiento |
|-----------|------|----------------|
| `connect()` falla | Repository | `None`, loguea, `_cache_valid = False` |
| DataFrame vacío | Repository | `None`, loguea, `_cache_valid = False` |
| < 28 columnas | ETL | Loguea, `total_mapeados = 0`, sin excepción |
| `total_encuestados == 0` | ETL | `porcentaje_impacto_global = 0.0` |
| `total_mapeados == 0` | ETL | `porcentaje_del_subtotal = 0.0` para todas |
| Repository retorna `None` | Service | Objetos default (zeros, listas vacías) |
| Exception en GET | Controller | HTTP 500 `{"detail": str(e)}` |
| `ImportError` service | CLI | Print error + `sys.exit(1)` |
