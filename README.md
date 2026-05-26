# AS241_HF_T5 — Backend de Encuestas (Brechas + Empleabilidad)

Backend para analizar encuestas de brechas académicas y empleabilidad. Los datos se obtienen en vivo desde Google Sheets (sin base de datos), se procesan con pandas y numpy, y se exponen vía API REST y CLI.

## Requisitos previos

- Python 3.10+

## Instalación

```bash
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

## Cómo ejecutar

### API REST

```bash
.\venv\Scripts\Activate
uvicorn main:app --reload --port 8000
```

### Endpoints (Postman / navegador)

| URL | Descripción |
|-----|-------------|
| `http://127.0.0.1:8000/` | Información del proyecto |
| `http://127.0.0.1:8000/api/brechas/dashboard` | Dashboard completo de Brechas |
| `http://127.0.0.1:8000/api/empleabilidad/dashboard` | Dashboard completo de Empleabilidad |
| `http://127.0.0.1:8000/api/etl/load` | Recarga forzada desde Google Sheets |

### CLI

```bash
python cli.py                    # Todos los módulos
python cli.py list               # Lista de comandos disponibles
python cli.py raw                # Datos crudos
```

## Explicación de funcionamiento

```
Google Sheets (CSV) → caché 30s → DataFrame → API REST + CLI
```

- No usa base de datos. Todo vive en memoria.
- Cada consulta trae datos frescos del Google Sheets (caché de 30s).
- Agregar datos nuevos en la sheet → aparecen automáticamente.
- Recarga forzada: `GET /api/etl/load`.

## Comandos CLI

### Módulo Brechas

```bash
python cli.py brechas                          # Dashboard completo
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
python cli.py brechas.tecnica                  # Brecha técnica promedio
python cli.py brechas.digital                  # Brecha digital promedio
python cli.py brechas.blandas                  # Brecha de habilidades blandas
python cli.py brechas.sin_formacion            # Estudiantes sin formación digital
python cli.py brechas.bajo_dominio             # Estudiantes con bajo dominio tecnológico
python cli.py brechas.uso_carrera              # % estudiantes que usan herramientas de su carrera
```

### Módulo Empleabilidad

```bash
python cli.py empleabilidad                          # Dashboard completo
python cli.py empleabilidad.indicador                # Indicador general de empleabilidad
python cli.py empleabilidad.preparacion              # Preparación para ingresar al mercado laboral
python cli.py empleabilidad.institucional            # Preparación institucional percibida
python cli.py empleabilidad.dificultad               # Dificultad percibida para conseguir trabajo
python cli.py empleabilidad.practicas                # Porcentaje con prácticas preprofesionales
python cli.py empleabilidad.interes                  # Interés en recibir más formación profesional
python cli.py empleabilidad.comunicacion             # Importancia de comunicación efectiva
python cli.py empleabilidad.equipo                   # Importancia del trabajo en equipo
python cli.py empleabilidad.problemas                # Importancia de resolución de problemas
python cli.py empleabilidad.adaptabilidad            # Importancia de la adaptabilidad
python cli.py empleabilidad.organizacion             # Importancia de organización y manejo del tiempo
python cli.py empleabilidad.centro                   # Importancia del centro de evaluación
python cli.py empleabilidad.carrera                  # Comparación de empleabilidad por carrera
python cli.py empleabilidad.semestre                 # Comparación de empleabilidad por semestre
python cli.py empleabilidad.valoradas                # Ranking de habilidades más valoradas
python cli.py empleabilidad.debiles                  # Ranking de habilidades más débiles
python cli.py empleabilidad.listos                   # Estudiantes listos para el mercado laboral
python cli.py empleabilidad.insuficientes            # Estudiantes que consideran insuficiente la preparación
```
