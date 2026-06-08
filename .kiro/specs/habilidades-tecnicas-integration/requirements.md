# Requirements Document

## Introduction

Este documento especifica los requisitos para integrar el módulo de **Habilidades Técnicas** al proyecto AS241_HF_T5, siguiendo la arquitectura en capas ya establecida por el módulo de Habilidades Blandas (ETL → Repository → Service → Controller + CLI).

El script standalone `app/models/habilidades_tecnicas_model.py` realiza el ETL completo, genera un JSON y muestra un gráfico de dona ("Matriz Operacional de Requerimientos"). Este módulo debe refactorizar esa lógica en capas reutilizables, exponerla vía API REST con FastAPI y extender el CLI existente.

Los datos provienen de una pestaña distinta de Google Sheets (columna 27 con índice 0-based, `gid=1157215314`), separada de la fuente de Habilidades Blandas.

---

## Glossary

- **ETL**: Extract, Transform, Load. Capa responsable de extraer datos crudos, clasificarlos y calcular métricas.
- **Repository**: Capa de acceso a datos con caché en memoria que actúa como intermediario entre el conector y el ETL.
- **Service**: Capa de lógica de negocio que orquesta el Repository y construye los objetos de respuesta.
- **Controller**: Capa de endpoints FastAPI que expone la API HTTP.
- **CLI**: Interfaz de línea de comandos (`cli.py`) para consumo desde terminal.
- **GoogleSheetsConnector**: Clase utilitaria en `app/utils/google_sheets_connector.py` que descarga CSV desde Google Sheets.
- **HabilidadesTecnicasETL**: Clase ETL específica para el módulo técnico, ubicada en `app/etl/habilidades_tecnicas_etl.py`.
- **HabilidadesTecnicasRepository**: Repositorio con caché para el módulo técnico, en `app/repositories/habilidades_tecnicas_repository.py`.
- **HabilidadesTecnicasService**: Servicio de negocio en `app/services/habilidades_tecnicas_service.py`.
- **HabilidadesTecnicasController**: Router FastAPI en `app/api/controllers/habilidades_tecnicas_controller.py`.
- **PATRONES_TECNICOS**: Diccionario de 7 patrones regex mutuamente excluyentes para clasificar respuestas de habilidades técnicas.
- **Resumen_Global**: Objeto con `total_encuestados`, `total_mapeados` y `porcentaje_impacto_global`.
- **Subcategoria_Tecnica**: Objeto con `categoria: str`, `votos: int` y `porcentaje_del_subtotal: float`.
- **Matriz_Operacional**: Nombre del análisis de distribución de habilidades técnicas (gráfico de dona en el script original).
- **SHEET_URL_TECNICAS**: Constante de configuración que contiene la URL CSV de Google Sheets para habilidades técnicas (`gid=1157215314`), cargada desde la variable de entorno `GOOGLE_SHEET_TECNICAS_URL`.
- **cache_valid**: Bandera booleana interna del repository que controla si los datos cacheados son válidos.

---

## Requirements

### Requirement 1: Conector Google Sheets para Habilidades Técnicas

**User Story:** Como desarrollador del sistema, quiero que el GoogleSheetsConnector soporte la fuente de datos de habilidades técnicas, para que el módulo pueda descargar la columna 27 del sheet `gid=1157215314` sin interferir con la fuente de habilidades blandas.

#### Acceptance Criteria

1. THE `GoogleSheetsConnector` SHALL accept an arbitrary CSV URL as a constructor parameter such that two instances initialized with different URLs maintain independent internal state (different `url_csv`, `raw_data`, and `cleaned_data` attributes).
2. WHEN `GoogleSheetsConnector.connect()` is called with the habilidades técnicas URL, THE connector SHALL download the CSV and store a `pd.DataFrame` with all original columns preserved (no column filtering or renaming) in `self.raw_data`; IF the download fails, THE connector SHALL return `False` and leave `self.raw_data` unchanged.
3. THE `app/config/database.py` SHALL expose a constant `SHEET_URL_TECNICAS` loaded from the environment variable `GOOGLE_SHEET_TECNICAS_URL`.
4. IF the environment variable `GOOGLE_SHEET_TECNICAS_URL` is not defined, THEN THE `app/config/database.py` SHALL assign an empty string `""` as the default value for `SHEET_URL_TECNICAS`.
5. THE `app/utils/google_sheets_connector.py` `clean_data()` method SHALL continue to accept zero arguments beyond `self`, apply the `habilidades_mapping` column rename, and return a `pd.DataFrame` with only the 8 renamed habilidades-blandas columns — unchanged by the addition of the técnicas module.

---

### Requirement 2: Capa ETL de Habilidades Técnicas

**User Story:** Como analista de datos, quiero una clase ETL dedicada para habilidades técnicas, para que las transformaciones y cálculos del script standalone queden encapsulados y sean reutilizables desde otras capas.

#### Acceptance Criteria

1. WHEN any `HabilidadesTecnicasETL` method that requires classification is called, THE ETL SHALL apply `PATRONES_TECNICOS` patterns in declaration order (first match wins, mutually exclusive) to each response text.
2. THE `PATRONES_TECNICOS` dictionary SHALL contain exactly the following 7 keys in this order: "Lógica y Algoritmia (Seudocódigo/Flujograma)", "Bases de Datos y Análisis (SQL/Sheets)", "Refuerzo General y Práctica Constante", "Desarrollo Frontend (HTML/CSS)", "Arquitectura, Backend y DevOps (Docker)", "Infraestructura, Redes y AWS", "Programación y Código General" — and SHALL NOT contain "Trabajo en Equipo y Habilidades Blandas".
3. WHEN a response text does not match any pattern in `PATRONES_TECNICOS`, THE ETL SHALL assign `None` to that row's category, and that row SHALL NOT be counted in `total_mapeados`.
4. THE `HabilidadesTecnicasETL` SHALL calculate `total_encuestados` as `len(self.df)` (total rows in the DataFrame, including NaN rows).
5. THE `HabilidadesTecnicasETL` SHALL calculate `total_mapeados` as the count of rows where the assigned category is not `None`.
6. THE `HabilidadesTecnicasETL` SHALL calculate `porcentaje_impacto_global` as `round((total_mapeados / total_encuestados) * 100, 1)`.
7. WHEN `total_encuestados` is zero, THE `HabilidadesTecnicasETL` SHALL return `porcentaje_impacto_global` as `0.0` without raising any exception.
8. THE `HabilidadesTecnicasETL` SHALL calculate `porcentaje_del_subtotal` for each category as `round((votos_categoria / total_mapeados) * 100, 1)`.
9. WHEN `total_mapeados` is zero, THE `HabilidadesTecnicasETL` SHALL return `porcentaje_del_subtotal` as `0.0` for all categories without raising any exception.
10. THE `HabilidadesTecnicasETL` SHALL expose a `get_resumen_global()` method that returns a `ResumenGlobalTecnico` dataclass instance with integer fields `total_encuestados`, `total_mapeados` and float field `porcentaje_impacto_global`.
11. THE `HabilidadesTecnicasETL` SHALL expose a `get_subcategorias_tecnicas()` method that returns a list of `SubcategoriaTecnica` instances — each with `categoria: str`, `votos: int`, `porcentaje_del_subtotal: float` — sorted descending by `votos`, only including categories with `votos > 0`.
12. THE `HabilidadesTecnicasETL` SHALL expose a `get_complete_dashboard_data()` method that returns a dictionary with exactly three keys: `resumen_global` (dict), `subcategorias_tecnicas` (list of dicts), and `last_updated` (string in format "YYYY-MM-DD HH:MM:SS").
13. THE `HabilidadesTecnicasETL` SHALL expose a `generate_insights()` method that returns a non-empty string containing at least 2 observations, each observation including at least one numeric value derived from the computed data (e.g., a count, percentage, or category name).
14. THE `HabilidadesTecnicasETL` SHALL expose a `get_matriz_operacional()` method that returns the same list of `SubcategoriaTecnica` instances as `get_subcategorias_tecnicas()`, maintaining identical sort order and field values.
15. FOR ALL DataFrames with at least one mapped record, THE sum of `votos` across all `SubcategoriaTecnica` instances returned by `get_subcategorias_tecnicas()` SHALL equal `total_mapeados` (invariant property).
16. FOR ALL DataFrames with at least one mapped record, THE sum of `porcentaje_del_subtotal` across all `SubcategoriaTecnica` instances SHALL equal `100.0` with a tolerance of `±0.5` (floating-point rounding).
17. IF `df.columns[27]` raises an `IndexError` (DataFrame has fewer than 28 columns), THEN THE `HabilidadesTecnicasETL` SHALL log an error and treat all rows as unmapped (`total_mapeados = 0`) without raising an exception.

---

### Requirement 3: Modelos de Datos para Habilidades Técnicas

**User Story:** Como desarrollador del sistema, quiero dataclasses tipadas para los datos de habilidades técnicas, para que el flujo de datos entre capas sea type-safe y consistente con el patrón del módulo de habilidades blandas.

#### Acceptance Criteria

1. THE `app/models/habilidades_tecnicas_model.py` SHALL define a dataclass `ResumenGlobalTecnico` with fields `total_encuestados: int`, `total_mapeados: int`, and `porcentaje_impacto_global: float`; its `to_dict()` method SHALL return `porcentaje_impacto_global` rounded to 1 decimal place.
2. THE `app/models/habilidades_tecnicas_model.py` SHALL define a dataclass `SubcategoriaTecnica` with fields `categoria: str`, `votos: int`, and `porcentaje_del_subtotal: float`; its `to_dict()` method SHALL return `porcentaje_del_subtotal` rounded to 1 decimal place.
3. THE `app/models/habilidades_tecnicas_model.py` SHALL define a dataclass `HabilidadesTecnicasDashboard` with fields `resumen_global: ResumenGlobalTecnico`, `subcategorias_tecnicas: List[SubcategoriaTecnica]`, `last_updated: str` (format "YYYY-MM-DD HH:MM:SS"), and `analisis_insights: str` (max 1000 characters); its `to_dict()` method SHALL delegate to `resumen_global.to_dict()` and `[s.to_dict() for s in subcategorias_tecnicas]`.
4. WHEN `app/models/habilidades_tecnicas_model.py` is imported, THE module SHALL not trigger any network request, file write operation, or GUI rendering — the three side effects present in the original standalone script.

---

### Requirement 4: Repository de Habilidades Técnicas con Caché

**User Story:** Como desarrollador del sistema, quiero un repository que cachee los datos de habilidades técnicas en memoria, para que las peticiones repetidas no descarguen el CSV de Google Sheets innecesariamente.

#### Acceptance Criteria

1. THE `HabilidadesTecnicasRepository` SHALL initialize with `_cache_valid = False` and `etl = None`, and SHALL maintain an internal `GoogleSheetsConnector` instance created with the provided URL.
2. WHEN `load_data()` is called and both `_cache_valid == True` and `self.etl is not None`, THE repository SHALL return the cached `HabilidadesTecnicasETL` instance without calling `connector.connect()`.
3. WHEN `load_data(force_refresh=True)` is called, THE repository SHALL call `connector.connect()` regardless of `_cache_valid`, and upon success SHALL set `_cache_valid = True`.
4. IF `connector.connect()` returns `False`, THEN THE repository SHALL set `_cache_valid = False`, log the error, and return `None`.
5. IF the raw DataFrame is empty after `connect()`, THEN THE repository SHALL set `_cache_valid = False`, log the error, and return `None`.
6. THE `HabilidadesTecnicasRepository` SHALL expose an `invalidate_cache()` method that sets `_cache_valid = False`.
7. THE `HabilidadesTecnicasRepository` SHALL expose a `get_dashboard_data()` method that calls `load_data()` and, if the result is not `None`, returns `etl.get_complete_dashboard_data()`; IF `load_data()` returns `None`, THEN `get_dashboard_data()` SHALL return `None`.
8. WHEN loading data, THE repository SHALL access the técnicas column using `df.iloc[:, 27]` (0-based positional index 27), not by column name.

---

### Requirement 5: Schemas Pydantic para la API de Habilidades Técnicas

**User Story:** Como desarrollador del API, quiero schemas Pydantic para serializar las respuestas del módulo técnico, para que los endpoints FastAPI retornen JSON bien tipado y documentado en Swagger.

#### Acceptance Criteria

1. THE `app/schemas/habilidades_tecnicas_schema.py` SHALL define a Pydantic schema `ResumenGlobalTecnicoSchema` with fields `total_encuestados: int`, `total_mapeados: int`, and `porcentaje_impacto_global: float` (value range 0.0–100.0).
2. THE `app/schemas/habilidades_tecnicas_schema.py` SHALL define a Pydantic schema `SubcategoriaTecnicaSchema` with fields `categoria: str`, `votos: int`, and `porcentaje_del_subtotal: float` (value range 0.0–100.0).
3. THE `app/schemas/habilidades_tecnicas_schema.py` SHALL define a Pydantic schema `DashboardHabilidadesTecnicasSchema` with fields `resumen_global: ResumenGlobalTecnicoSchema`, `subcategorias_tecnicas: List[SubcategoriaTecnicaSchema]`, `last_updated: str` (ISO 8601 format "YYYY-MM-DD HH:MM:SS"), and `analisis_insights: str`.
4. THE `app/schemas/habilidades_tecnicas_schema.py` SHALL define a Pydantic schema `MatrizOperacionalSchema` with field `subcategorias: List[SubcategoriaTecnicaSchema]` for the `/matriz` endpoint response.
5. THE `app/schemas/habilidades_tecnicas_schema.py` SHALL define a Pydantic schema `KPITecnicasSchema` with fields `total_encuestados: int`, `total_mapeados: int`, `porcentaje_impacto_global: float` (range 0.0–100.0), and `categoria_lider: str` (the category name with the highest `votos`; if two categories tie, the one appearing first in `PATRONES_TECNICOS` declaration order is selected).
6. THE schemas `ResumenGlobalTecnicoSchema`, `SubcategoriaTecnicaSchema`, `DashboardHabilidadesTecnicasSchema`, `MatrizOperacionalSchema`, and `KPITecnicasSchema` SHALL each be configurable with `model_config = ConfigDict(from_attributes=True)` (Pydantic v2 syntax).

---

### Requirement 6: Service de Habilidades Técnicas

**User Story:** Como desarrollador del sistema, quiero un service que encapsule la lógica de negocio del módulo técnico, para que el controller y el CLI consuman una interfaz limpia sin acoplarse directamente al repository o ETL.

#### Acceptance Criteria

1. THE `app/services/habilidades_tecnicas_service.py` SHALL declare a module-level `repository` variable as a single `HabilidadesTecnicasRepository` instance initialized with `SHEET_URL_TECNICAS` from `app/config/database.py`.
2. THE service SHALL expose a `build_dashboard(force_refresh: bool = False)` function that passes `force_refresh` to `repository.get_dashboard_data()` and returns a `DashboardHabilidadesTecnicasSchema`.
3. THE service SHALL expose a `get_kpi_metrics(force_refresh: bool = False)` function that returns a `KPITecnicasSchema` where `categoria_lider` is the `categoria` field of the `SubcategoriaTecnica` with the highest `votos`; IF two categories tie, the one first in `PATRONES_TECNICOS` order is returned.
4. THE service SHALL expose a `get_matriz_operacional(force_refresh: bool = False)` function that passes `force_refresh` to the repository and returns a `MatrizOperacionalSchema`.
5. THE service SHALL expose an `invalidate_cache()` function that calls `repository.invalidate_cache()` without raising any exception.
6. IF the repository returns `None` for any service function, THEN the service SHALL return the following default objects without raising any exception: `build_dashboard` → `DashboardHabilidadesTecnicasSchema` with `resumen_global` all zeros, empty lists, `last_updated=""`, `analisis_insights=""`; `get_kpi_metrics` → `KPITecnicasSchema` with all numeric fields `0`/`0.0` and `categoria_lider=""`; `get_matriz_operacional` → `MatrizOperacionalSchema` with `subcategorias=[]`.

---

### Requirement 7: Controller FastAPI de Habilidades Técnicas

**User Story:** Como consumidor de la API, quiero endpoints HTTP para el módulo de habilidades técnicas, para que el frontend o herramientas externas puedan consultar los datos via REST.

#### Acceptance Criteria

1. THE `HabilidadesTecnicasController` SHALL register an `APIRouter` with prefix `/api/habilidades-tecnicas` and tag `"Habilidades Técnicas"`.
2. THE controller SHALL expose `GET /api/habilidades-tecnicas/dashboard` returning `DashboardHabilidadesTecnicasSchema`, with `force_refresh: bool = False` as an optional query parameter.
3. THE controller SHALL expose `GET /api/habilidades-tecnicas/matriz` returning `MatrizOperacionalSchema`, with `force_refresh: bool = False` as an optional query parameter.
4. THE controller SHALL expose `GET /api/habilidades-tecnicas/kpi` returning `KPITecnicasSchema`, with `force_refresh: bool = False` as an optional query parameter.
5. THE controller SHALL expose `POST /api/habilidades-tecnicas/reload` that returns a JSON response with a non-empty `message` string confirming the cache was invalidated and data was reloaded.
6. WHEN `POST /api/habilidades-tecnicas/reload` is called, THE server SHALL invalidate the cache and complete a full data reload before sending the response (i.e., the response is sent only after the reload is complete).
7. IF a GET endpoint's service call raises an unhandled exception, THEN THE controller SHALL return HTTP 500 with an error detail string.
8. THE `app/api/routes/__init__.py` SHALL include both the habilidades-blandas router and the habilidades-técnicas router, preserving the existing blandas registration.

---

### Requirement 8: Extensión del CLI para Habilidades Técnicas

**User Story:** Como desarrollador o analista, quiero comandos CLI para habilidades técnicas, para poder consultar los datos desde la terminal sin levantar el servidor HTTP.

#### Acceptance Criteria

1. WHEN `python cli.py tecnicas` is executed, THE CLI SHALL call `build_dashboard()` from `app.services.habilidades_tecnicas_service` and print the full dashboard using the `show()` helper with `HEADER`/`FOOTER` separators.
2. WHEN `python cli.py tecnicas-kpi` is executed, THE CLI SHALL call `get_kpi_metrics()` from `app.services.habilidades_tecnicas_service` and display the KPI fields using the `show()` helper.
3. WHEN `python cli.py tecnicas-matriz` is executed, THE CLI SHALL call `get_matriz_operacional()` from `app.services.habilidades_tecnicas_service` and print each subcategory on its own line in the format `  • <categoria>: <votos> votos (<porcentaje_del_subtotal>%)`.
4. WHEN `python cli.py tecnicas-refresh` is executed, THE CLI SHALL call `invalidate_cache()` and then `build_dashboard(force_refresh=True)` from `app.services.habilidades_tecnicas_service`, and print a confirmation message followed by a timestamp in the format `YYYY-MM-DD HH:MM:SS`.
5. WHEN `python cli.py list` is executed, THE CLI SHALL display the 4 técnicas commands (`tecnicas`, `tecnicas-kpi`, `tecnicas-matriz`, `tecnicas-refresh`) under a section labeled "MÓDULO TÉCNICAS".
6. THE `cli.py` SHALL import `build_dashboard`, `get_kpi_metrics`, `get_matriz_operacional`, and `invalidate_cache` from `app.services.habilidades_tecnicas_service`.
7. WHEN any técnicas command produces output, THE CLI SHALL use the existing constants `HEADER = "\n" + "=" * 72`, `FOOTER = "=" * 72 + "\n"`, and `SEP = "-" * 72` for visual formatting.
8. IF importing `app.services.habilidades_tecnicas_service` fails at CLI startup, THEN THE CLI SHALL print an error message and exit with code 1 without crashing silently.

---

### Requirement 9: Registro del Módulo y Actualización de main.py

**User Story:** Como desarrollador del sistema, quiero que el módulo de habilidades técnicas quede registrado en el router principal y en la metadata de la aplicación FastAPI, para que los endpoints sean accesibles al iniciar el servidor.

#### Acceptance Criteria

1. THE `app/api/routes/__init__.py` SHALL call `api_router.include_router()` with the habilidades-técnicas router, in addition to the existing blandas router registration.
2. WHEN `GET /` is called on the running server, THE response SHALL include a key `"habilidades_tecnicas"` containing the paths for the 4 técnicas endpoints (`/api/habilidades-tecnicas/dashboard`, `/api/habilidades-tecnicas/matriz`, `/api/habilidades-tecnicas/kpi`, `/api/habilidades-tecnicas/reload`).
3. WHILE the FastAPI server is running, THE server SHALL respond with HTTP 200 to `GET /api/habilidades-tecnicas/dashboard`, `GET /api/habilidades-tecnicas/matriz`, `GET /api/habilidades-tecnicas/kpi`, and HTTP 200 to `POST /api/habilidades-tecnicas/reload`.

---

### Requirement 10: Consistencia Arquitectónica y No Regresión

**User Story:** Como mantenedor del proyecto, quiero que la integración del módulo técnico no rompa el módulo de habilidades blandas existente, para que ambos módulos coexistan correctamente.

#### Acceptance Criteria

1. THE habilidades-técnicas module SHALL mirror the habilidades-blandas module structure across exactly these 6 layers: `app/etl/`, `app/repositories/`, `app/services/`, `app/schemas/`, `app/api/controllers/`, and CLI commands in `cli.py`.
2. WHEN `app.services.habilidades_tecnicas_service` is imported, THE `repository` singleton in `app.services.habilidades_blandas_service` SHALL remain unchanged (same object identity and state).
3. THE `HabilidadesTecnicasRepository` SHALL be initialized with `SHEET_URL_TECNICAS` (declared in `app/config/database.py`) and SHALL NOT share its `GoogleSheetsConnector` instance with `HabilidadesBlandasRepository`.
4. IF `GOOGLE_SHEET_TECNICAS_URL` is not set (empty string), THEN `app.services.habilidades_blandas_service` SHALL continue to function normally and return data from its own configured sheet URL.
5. WHEN `app/models/habilidades_tecnicas_model.py` is executed as a standalone script (via `python app/models/habilidades_tecnicas_model.py`), THE script SHALL write a `datos_tecnicos_react.json` file and render a matplotlib chart — confirming the original standalone behavior is preserved.
