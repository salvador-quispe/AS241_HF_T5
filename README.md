# AS241_HF_T5 — Backend de Encuestas (Brechas + Empleabilidad)

Backend para analizar encuestas de brechas académicas y empleabilidad. Los datos se obtienen en vivo desde Google Sheets (sin base de datos), se procesan con pandas y numpy, y se exponen vía API REST y CLI.

## Requisitos

- Python 3.10+
- pip

## Instalación

```bash
pip install numpy==1.26.4 pandas==2.2.3
```

Dependencias adicionales (uvicorn, pydantic, etc.):

```bash
pip install "fastapi[standard]" python-dotenv
```

## Ejecutar API

```bash
uvicorn main:app --reload --port 8000
```

### Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Información del proyecto |
| GET | `/api/brechas/dashboard` | Dashboard completo de Brechas (16 indicadores) |
| GET | `/api/empleabilidad/dashboard` | Dashboard completo de Empleabilidad (18 indicadores) |
| GET/POST | `/api/etl/load` | Recarga forzada desde Google Sheets |

### Probar con curl

```bash
curl http://127.0.0.1:8000/api/brechas/dashboard
curl http://127.0.0.1:8000/api/empleabilidad/dashboard
```

## CLI

```bash
python cli.py                    # Ver todos los módulos completos
python cli.py list               # Lista de comandos disponibles
python cli.py raw                # Datos crudos + distribuciones
```

### Módulo Brechas

```bash
python cli.py brechas                          # Dashboard completo de brechas
python cli.py brechas.conocimientos            # Nivel de conocimientos técnicos
python cli.py brechas.dominio                  # Nivel de dominio de herramientas digitales
python cli.py brechas.frecuencia               # Frecuencia de uso de herramientas digitales
python cli.py brechas.formacion                # Formación en herramientas digitales
python cli.py brechas.herramientas             # Herramientas digitales más utilizadas
python cli.py brechas.preparacion              # Nivel de preparación para aplicar conocimientos
python cli.py brechas.habilidades              # Habilidades que necesitan mejorar
python cli.py brechas.carrera                  # Comparación por carrera profesional
python cli.py brechas.semestre                 # Comparación por semestre académico
python cli.py brechas.edad                     # Comparación por edad
python cli.py brechas.brecha_tecnica           # Brecha técnica promedio
python cli.py brechas.brecha_digital           # Brecha digital promedio
python cli.py brechas.blandas                  # Brecha de habilidades blandas
python cli.py brechas.sin_formacion            # Estudiantes sin formación digital
python cli.py brechas.bajo_dominio             # Estudiantes con bajo dominio tecnológico
python cli.py brechas.uso_herramientas         # % que usan herramientas de su carrera
```

### Módulo Empleabilidad

```bash
python cli.py empleabilidad                          # Dashboard completo de empleabilidad
python cli.py empleabilidad.indicador                # Indicador general de empleabilidad
python cli.py empleabilidad.preparacion              # Preparación para ingresar al mercado laboral
python cli.py empleabilidad.preparacion_institucional # Preparación institucional percibida
python cli.py empleabilidad.dificultad               # Dificultad percibida para conseguir trabajo
python cli.py empleabilidad.practicas                # Porcentaje con prácticas preprofesionales
python cli.py empleabilidad.formacion                # Interés en recibir más formación profesional
python cli.py empleabilidad.comunicacion             # Importancia de comunicación efectiva
python cli.py empleabilidad.equipo                   # Importancia del trabajo en equipo
python cli.py empleabilidad.problemas                # Importancia de resolución de problemas
python cli.py empleabilidad.adaptabilidad            # Importancia de la adaptabilidad
python cli.py empleabilidad.organizacion             # Importancia de organización y manejo del tiempo
python cli.py empleabilidad.centro_evaluacion        # Importancia del centro de evaluación
python cli.py empleabilidad.carrera                  # Comparación de empleabilidad por carrera
python cli.py empleabilidad.semestre                 # Comparación de empleabilidad por semestre
python cli.py empleabilidad.valoradas                # Ranking de habilidades más valoradas
python cli.py empleabilidad.debiles                  # Ranking de habilidades más débiles
python cli.py empleabilidad.listos                   # Estudiantes listos para el mercado laboral
python cli.py empleabilidad.insuficiente             # Estudiantes que consideran insuficiente la preparación
```

## Cómo funciona

```
Google Sheets (CSV en vivo)
        │
        ▼
config/database.py  ← caché de 30 segundos
        │
        ▼
    pd.DataFrame
        │
        ├──► services/brechas.py      ← cálculos con pandas/numpy
        └──► services/empleabilidad.py ← cálculos con pandas/numpy
                    │
                    ▼
        api/controllers/  +  cli.py  (API REST + línea de comandos)
```

- No usa base de datos. Todo vive en memoria.
- Cada consulta trae datos frescos del Google Sheets (caché de 30s).
- Agregar una fila nueva en la sheet → aparece automáticamente en la próxima consulta.
- Para recarga forzada inmediata: `GET /api/etl/load` o `python cli.py --reload`.

## Estructura del proyecto

```
main.py                    ← FastAPI (punto de entrada)
cli.py                     ← CLI con todos los comandos
.env                       ← GOOGLE_SHEET_URL
requirements.txt           ← dependencias
.gitignore
app/
├── config/database.py     ← fetch + caché desde Google Sheets
├── etl/loader.py          ← transformación de columnas
├── schemas/
│   ├── brechas.py         ← modelos Pydantic
│   └── empleabilidad.py
├── services/
│   ├── brechas.py         ← análisis de brechas
│   └── empleabilidad.py   ← análisis de empleabilidad
└── api/controllers/
    ├── brechas.py         ← endpoint /api/brechas/dashboard
    ├── empleabilidad.py   ← endpoint /api/empleabilidad/dashboard
    └── etl.py             ← endpoint /api/etl/load
```
