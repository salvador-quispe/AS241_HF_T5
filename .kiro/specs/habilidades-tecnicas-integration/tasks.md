## Implementation Plan: Habilidades Técnicas Integration
## Overview

Integra el módulo de Habilidades Técnicas siguiendo la arquitectura en capas del módulo Blandas (ETL → Repository → Service → Controller + CLI). Se crean 5 archivos nuevos y se modifican 4 existentes. El orden respeta las dependencias entre capas.

## Tasks

- [x] 1. Añadir `SHEET_URL_TECNICAS` a `app/config/database.py`
  - _Requirements: 1.3, 1.4_

- [x] 2. Crear `app/etl/habilidades_tecnicas_etl.py`
  - [x] 2.1 Definir las tres dataclasses: `ResumenGlobalTecnico`, `SubcategoriaTecnica` y `HabilidadesTecnicasDashboard` con sus métodos `to_dict()` que redondean floats a 1 decimal
  - [x] 2.2 Declarar la constante módulo-nivel `PATRONES_TECNICOS` con exactamente los 7 patrones regex
  - [x] 2.3 Implementar la clase `HabilidadesTecnicasETL` con `__init__`, `_clasificador` y manejo de `IndexError`
  - [x] 2.4 Implementar `get_resumen_global()`, `get_subcategorias_tecnicas()`, `get_matriz_operacional()`, `get_complete_dashboard_data()` y `generate_insights()`

- [x] 3. Crear `app/repositories/habilidades_tecnicas_repository.py`
  - [x] 3.1 `__init__` con GoogleSheetsConnector propio, `etl = None`, `_cache_valid = False`
  - [x] 3.2 `load_data()` con caché, raw_data directo al ETL (sin `clean_data()`)
  - [x] 3.3 `invalidate_cache()` y `get_dashboard_data()`

- [x] 4. Crear `app/schemas/habilidades_tecnicas_schema.py`
  - 5 schemas Pydantic v2 con `ConfigDict(from_attributes=True)`

- [x] 5. Crear `app/services/habilidades_tecnicas_service.py`
  - [x] 5.1 Singleton `repository`
  - [x] 5.2 `build_dashboard()` con defaults ante None
  - [x] 5.3 `get_kpi_metrics()` con `categoria_lider` y tie-breaking
  - [x] 5.4 `get_matriz_operacional()` e `invalidate_cache()`

- [x] 6. Crear `app/api/controllers/habilidades_tecnicas_controller.py`
  - 4 endpoints: GET /dashboard, GET /matriz, GET /kpi, POST /reload

- [x] 7. Registrar `tecnicas_router` en `app/api/routes/__init__.py`

- [x] 8. Actualizar `main.py` con clave `habilidades_tecnicas` en `GET /`

- [x] 9. Extender `cli.py` con los 4 comandos de habilidades técnicas
  - [x] 9.1 Imports con aliases y `try/except ImportError`
  - [x] 9.2 Handlers: `tecnicas`, `tecnicas-kpi`, `tecnicas-matriz`, `tecnicas-refresh`
  - [x] 9.3 `show_list()` actualizado con sección "MÓDULO TÉCNICAS"
