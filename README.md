# AS241_HF_T5 - Habilidades Blandas

Backend de análisis de encuestas para el módulo de **Habilidades Blandas**.

## Módulo

Analiza las respuestas del formulario Google relacionadas a:

- Importancia de la comunicación efectiva
- Importancia del trabajo en equipo
- Importancia de la resolución de problemas
- Importancia de la adaptabilidad
- Importancia de la organización y manejo del tiempo
- Satisfacción con la preparación institucional
- Interés en recibir más formación
- Habilidades que los estudiantes consideran necesitar mejorar

## Ejecutar

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## CLI

```bash
python cli.py            # Dashboard completo
python cli.py kpi        # Indicadores KPI
python cli.py promedios  # Promedios por habilidad
python cli.py mejorar    # Habilidades a mejorar
python cli.py satisfaccion
python cli.py interes
python cli.py insights
python cli.py list       # Ver todos los comandos
```

## Endpoints

- `GET /api/habilidades-blandas/dashboard`
- `GET /api/habilidades-blandas/kpi`
- `GET /api/habilidades-blandas/promedios`
- `GET /api/habilidades-blandas/mejorar`
- `GET /api/habilidades-blandas/satisfaccion`
- `GET /api/habilidades-blandas/interes`
- `GET /api/habilidades-blandas/insights`
- `POST /api/habilidades-blandas/reload`
