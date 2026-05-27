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
| GET | `/api/perfil-estudiante/genero` | Distribución por género |
| GET | `/api/perfil-estudiante/carreras` | Distribución por carrera |
| GET | `/api/perfil-estudiante/semestres` | Distribución por semestre |
| GET | `/api/perfil-estudiante/edades` | Distribución por rangos de edad |
| GET | `/api/perfil-estudiante/distritos` | Distribución por distrito |
| GET | `/api/perfil-estudiante/riesgo` | Riesgo académico por semestre |
| GET | `/api/perfil-estudiante/insights` | Insights y recomendaciones |
| GET | `/api/perfil-estudiante/tasa-retencion` | Tasa de retención |

> Base URL local: `http://127.0.0.1:8000`

---

## Probar un endpoint

Abre tu navegador o Postman y visita:

```
http://127.0.0.1:8000/api/perfil-estudiante/kpi
```

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