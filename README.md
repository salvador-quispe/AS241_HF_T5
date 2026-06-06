# AS241_HF_T5 — Perfil del Estudiante (Dashboard BI)

Backend para analizar el perfil demográfico y académico de estudiantes. Los datos se obtienen en vivo desde Google Sheets, se procesan con pandas y numpy, y se exponen vía API REST.

---

## Requisitos previos

- Python 3.10+
- Google Sheets URL configurada en `.env`

---

## Instalación y ejecución

```bash
# 1. Entrar a la carpeta del proyecto
cd C:\Users\USUARIO\Proyectos-5to\AS241_HF_T5

# 2. Crear entorno virtual (solo primera vez)
python -m venv venv

# 3. Activar entorno virtual
.\venv\Scripts\Activate

# 4. Instalar dependencias (solo primera vez)
pip install -r requirements.txt

# 5. Ejecutar la API
uvicorn main:app --reload --port 8000
```

---

## Configuración

Crear archivo `.env` en la raíz del proyecto:

```env
GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/ID_DEL_SPREADSHEET/export?format=csv
CACHE_TTL_SECONDS=30
```

---

## Endpoints disponibles

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/api/perfil-estudiante/dashboard` | Dashboard completo |
| GET | `/api/perfil-estudiante/kpi` | Indicadores KPI |
| GET | `/api/perfil-estudiante/job-readiness-distribution` | Distribución por preparación laboral |
| GET | `/api/perfil-estudiante/semestres` | Distribución por semestre |
| GET | `/api/perfil-estudiante/edades` | Distribución por rangos de edad |
| GET | `/api/perfil-estudiante/distritos` | Distribución por distrito |
| GET | `/api/perfil-estudiante/riesgo` | Riesgo académico por semestre |
| GET | `/api/perfil-estudiante/insights` | Insights descriptivos |

> Base URL local: `http://127.0.0.1:8000`

---

## Probar un endpoint

Abre tu navegador o Postman y visita:

```
http://127.0.0.1:8000/api/perfil-estudiante/kpi
```

---

## Proceso BI - Perfil del Estudiante

El módulo de perfil del estudiante resume los datos obtenidos desde la encuesta de Google Forms publicada en Google Sheets.

### 1. Extracción de datos

La API lee la hoja publicada en formato CSV usando la variable `GOOGLE_SHEET_URL` definida en `.env`.

```python
df = pd.read_csv(SHEET_URL, header=None, skiprows=1, encoding="utf-8")
```

### 2. Limpieza y preparación

Los nombres de columnas se normalizan para trabajar con campos más simples como `edad`, `distrito`, `semestre` y `preparado_ingresar_mercado_laboral`.

Luego se convierten a valores numéricos las columnas necesarias para calcular promedios, rangos y niveles de preparación.

### 3. Resúmenes generados con Python

El archivo `app/etl/student_profile_etl.py` contiene las consultas principales:

| Resumen | Interpretación |
|---------|----------------|
| KPI generales | Total de estudiantes, edad promedio, edad mínima, edad máxima, riesgo y logro institucional |
| Preparación laboral | Clasifica respuestas en baja, media y alta preparación |
| Distribución por distrito | Identifica los distritos con mayor participación |
| Distribución por semestre | Muestra la concentración de estudiantes por ciclo académico |
| Distribución por edad | Agrupa estudiantes por rangos de edad |
| Riesgo por semestre | Detecta estudiantes con baja preparación laboral por semestre |
| Insights | Genera una interpretación breve de los resultados principales |

### 4. Interpretación actual de resultados

Con los datos cargados desde la encuesta, el perfil del estudiante muestra una población mayoritaria de primeros y quintos semestres. El distrito con mayor concentración es San Vicente de Cañete. Además, una parte de los estudiantes reporta baja preparación para ingresar al mercado laboral, lo que permite identificar un grupo de riesgo para acciones de refuerzo académico o laboral.

---

## Detener la API

Presiona `Ctrl + C` en la terminal.

---

## Estructura del proyecto

```
AS241_HF_T5/
├── app/
│   ├── api/controllers/     # Endpoints de la API
│   ├── config/              # Configuración y conexión a Google Sheets
│   ├── etl/                 # Transformación de datos
│   ├── models/              # Modelos de datos
│   ├── repositories/        # Acceso a datos
│   ├── schemas/             # Validación Pydantic
│   ├── services/            # Lógica de negocio
│   └── utils/               # Utilidades
├── main.py                  # Punto de entrada
├── requirements.txt         # Dependencias
└── .env                     # Variables de entorno
```
