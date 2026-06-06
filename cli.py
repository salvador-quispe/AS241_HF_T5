"""
CLI - Perfil del Estudiante

Uso:
  python cli.py                         Dashboard completo
  python cli.py kpi                     Solo KPI
  python cli.py preparacion             Distribución por preparación laboral
  python cli.py distritos [N]           Distribución por distritos (top N)
  python cli.py semestres               Distribución por semestres
  python cli.py edades                  Distribución por edades
  python cli.py riesgo                  Riesgo académico por semestre
  python cli.py insights                Insights del análisis
  python cli.py graficos                Gráficos de barras en terminal
  python cli.py graficos-svg            Generar gráficos SVG con Python
  python cli.py raw                     Datos crudos
  python cli.py refresh                 Forzar actualización de caché
  python cli.py list                    Listar comandos disponibles
"""

import logging
import sys
from html import escape
from pathlib import Path
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)
pd.set_option("display.max_colwidth", 50)

from app.services.student_profile_service import (
    build_dashboard,
    get_kpi_metrics,
    get_job_readiness_distribution,
    get_district_distribution,
    get_semester_distribution,
    get_age_distribution,
    get_risk_by_semester,
    get_insights
)
from app.config.database import get_data, reload_data

logging.getLogger().setLevel(logging.WARNING)

SEP = "-" * 72
HEADER = "\n" + "=" * 72
FOOTER = "=" * 72 + "\n"


def p(obj, indent=0):
    """Pretty print for dicts and lists"""
    pad = " " * indent
    if isinstance(obj, dict):
        for k, v in obj.items():
            k_show = k.replace("_", " ").title()
            if isinstance(v, dict):
                print(f"{pad}{k_show}:")
                p(v, indent + 2)
            elif isinstance(v, list):
                print(f"{pad}{k_show}:")
                for i, item in enumerate(v, 1):
                    if isinstance(item, dict):
                        parts = [f"{ik.replace('_', ' ').title()}: {iv}" for ik, iv in item.items()]
                        print(f"{pad}  {i}. {' | '.join(parts)}")
                    else:
                        print(f"{pad}  {i}. {item}")
            else:
                print(f"{pad}{k_show}: {v}")
    elif isinstance(obj, list):
        for i, item in enumerate(obj, 1):
            if hasattr(item, "model_dump"):
                item = item.model_dump()
            if isinstance(item, dict):
                parts = [f"{ik.replace('_', ' ').title()}: {iv}" for ik, iv in item.items()]
                print(f"{pad}{i}. {' | '.join(parts)}")
            else:
                print(f"{pad}{i}. {item}")
    else:
        print(f"{pad}{obj}")


def show(title: str, data):
    """Display data with formatted header"""
    print(HEADER)
    print(f"  {title}")
    print(FOOTER)
    
    if hasattr(data, 'model_dump'):
        data = data.model_dump()
    
    p(data)
    print()


def to_dict(item):
    """Convert Pydantic models to dictionaries for terminal rendering"""
    if hasattr(item, "model_dump"):
        return item.model_dump()
    return item


def draw_bar_chart(title: str, rows, label_key: str, value_key: str, percent_key: str = None, width: int = 36):
    """Draw a horizontal bar chart directly in the terminal"""
    rows = [to_dict(row) for row in rows]
    max_value = max([row[value_key] for row in rows], default=0)

    print(HEADER)
    print(f"  {title}")
    print(FOOTER)

    if not rows or max_value == 0:
        print("  Sin datos para graficar.\n")
        return

    for row in rows:
        label = str(row[label_key])
        value = row[value_key]
        percent = row.get(percent_key) if percent_key else None
        bar_length = round((value / max_value) * width) if max_value else 0
        bar = "#" * bar_length
        percentage_text = f" | {percent}%" if percent is not None else ""
        print(f"  {label:<28} | {bar:<{width}} | {value}{percentage_text}")

    print()


def write_svg_bar_chart(filepath: Path, title: str, rows, label_key: str, value_key: str, percent_key: str = None):
    """Generate a standalone SVG horizontal bar chart with Python only."""
    rows = [to_dict(row) for row in rows]
    max_value = max([row[value_key] for row in rows], default=0)

    chart_width = 920
    left_margin = 250
    bar_width = 520
    row_height = 48
    top_margin = 82
    height = top_margin + max(len(rows), 1) * row_height + 50

    svg_rows = []
    for index, row in enumerate(rows):
        y = top_margin + index * row_height
        label = escape(str(row[label_key]))
        value = row[value_key]
        percent = row.get(percent_key) if percent_key else None
        current_width = 0 if max_value == 0 else round((value / max_value) * bar_width)
        value_label = f"{value}"
        if percent is not None:
            value_label += f" ({percent}%)"

        svg_rows.append(f"""
  <text x="30" y="{y + 23}" class="label">{label}</text>
  <rect x="{left_margin}" y="{y}" width="{bar_width}" height="30" rx="8" class="bar-bg" />
  <rect x="{left_margin}" y="{y}" width="{current_width}" height="30" rx="8" class="bar" />
  <text x="{left_margin + bar_width + 18}" y="{y + 22}" class="value">{escape(value_label)}</text>""")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{chart_width}" height="{height}" viewBox="0 0 {chart_width} {height}">
  <style>
    .title {{ font: 700 24px Arial, sans-serif; fill: #111827; }}
    .label {{ font: 600 15px Arial, sans-serif; fill: #374151; }}
    .value {{ font: 700 14px Arial, sans-serif; fill: #111827; }}
    .bar-bg {{ fill: #e5e7eb; }}
    .bar {{ fill: #003F87; }}
  </style>
  <rect width="100%" height="100%" fill="#ffffff" />
  <text x="30" y="44" class="title">{escape(title)}</text>
  {''.join(svg_rows)}
</svg>
"""
    filepath.write_text(svg, encoding="utf-8")


def generate_svg_charts():
    """Generate SVG charts and an HTML gallery."""
    output_dir = Path("outputs") / "graficos_perfil_estudiante"
    output_dir.mkdir(parents=True, exist_ok=True)

    charts = [
        (
            "preparacion_laboral.svg",
            "Preparación laboral",
            format_preparacion(get_job_readiness_distribution()),
            "level",
            "student_count",
            "percentage",
        ),
        (
            "distribucion_distrito.svg",
            "Distribución por distrito",
            get_district_distribution(6),
            "distrito",
            "cantidad_estudiantes",
            "porcentaje_participacion",
        ),
        (
            "distribucion_semestre.svg",
            "Distribución por semestre",
            get_semester_distribution(),
            "semestre",
            "cantidad_estudiantes",
            "porcentaje",
        ),
        (
            "distribucion_edad.svg",
            "Distribución por edad",
            get_age_distribution(),
            "rango_edad",
            "cantidad_estudiantes",
            "porcentaje",
        ),
        (
            "riesgo_semestre.svg",
            "Riesgo por semestre",
            get_risk_by_semester(),
            "semestre",
            "estudiantes_riesgo",
            "porcentaje_riesgo",
        ),
    ]

    for filename, title, rows, label_key, value_key, percent_key in charts:
        write_svg_bar_chart(output_dir / filename, title, rows, label_key, value_key, percent_key)

    cards = "\n".join(
        f'    <section><h2>{escape(title)}</h2><img src="{filename}" alt="{escape(title)}"></section>'
        for filename, title, *_ in charts
    )
    index_path = output_dir / "index.html"
    index_path.write_text(f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Gráficos - Perfil del Estudiante</title>
  <style>
    body {{ margin: 0; padding: 32px; font-family: Arial, sans-serif; background: #f3f4f6; color: #111827; }}
    main {{ max-width: 980px; margin: 0 auto; }}
    h1 {{ margin: 0 0 20px; }}
    section {{ background: white; border: 1px solid #e5e7eb; border-radius: 10px; padding: 20px; margin-bottom: 20px; }}
    h2 {{ margin: 0 0 12px; font-size: 20px; }}
    img {{ width: 100%; height: auto; display: block; }}
  </style>
</head>
<body>
  <main>
    <h1>Gráficos generados con Python - Perfil del Estudiante</h1>
{cards}
  </main>
</body>
</html>
""", encoding="utf-8")

    print(HEADER)
    print("  GRÁFICOS SVG GENERADOS CON PYTHON")
    print(FOOTER)
    for filename, *_ in charts:
        print(f"  - {output_dir / filename}")
    print(f"\n  Abrir resumen: {index_path}\n")


def format_preparacion(preparacion):
    """Translate job readiness labels for terminal display"""
    readiness_labels = {
        "LOW": "Baja",
        "MEDIUM": "Media",
        "HIGH": "Alta",
    }

    return [
        {
            **to_dict(item),
            "level": readiness_labels.get(to_dict(item)["level"], to_dict(item)["level"]),
        }
        for item in preparacion
    ]


def show_terminal_charts():
    """Display all BI summaries as terminal bar charts"""
    preparacion = format_preparacion(get_job_readiness_distribution())

    draw_bar_chart(
        "GRÁFICO - Preparación laboral",
        preparacion,
        "level",
        "student_count",
        "percentage",
    )

    draw_bar_chart(
        "GRÁFICO - Distribución por distrito",
        get_district_distribution(6),
        "distrito",
        "cantidad_estudiantes",
        "porcentaje_participacion",
    )

    draw_bar_chart(
        "GRÁFICO - Distribución por semestre",
        get_semester_distribution(),
        "semestre",
        "cantidad_estudiantes",
        "porcentaje",
    )

    draw_bar_chart(
        "GRÁFICO - Distribución por edad",
        get_age_distribution(),
        "rango_edad",
        "cantidad_estudiantes",
        "porcentaje",
    )

    draw_bar_chart(
        "GRÁFICO - Riesgo por semestre",
        get_risk_by_semester(),
        "semestre",
        "estudiantes_riesgo",
        "porcentaje_riesgo",
    )

    show("PERFIL DEL ESTUDIANTE - Insights", get_insights())


def show_raw():
    """Display raw data from Google Sheets"""
    df = get_data(force=True)
    
    print(HEADER)
    print("  DATOS CRUDOS - Primeras 10 filas")
    print(FOOTER)
    print(df.head(10).to_string(index=False))
    print()
    
    print(SEP)
    print("  DISTRIBUCIÓN POR CARRERA")
    print(SEP)
    print(df["carrera"].value_counts().to_string())
    print()
    
    print(SEP)
    print("  DISTRIBUCIÓN POR SEMESTRE")
    print(SEP)
    print(df["semestre"].value_counts().sort_index().to_string())
    print()
    
    print(SEP)
    print("  ESTADÍSTICAS GENERALES")
    print(SEP)
    print(f"  Total de encuestados: {len(df)}")
    print(f"  Total de columnas: {len(df.columns)}")
    print(f"  Columnas disponibles: {', '.join(df.columns.tolist())}")
    print()


def show_list():
    """Display available commands"""
    print(HEADER)
    print("  COMANDOS DISPONIBLES - Perfil del Estudiante")
    print(FOOTER)
    
    print("\n  📊 DASHBOARD COMPLETO:")
    print("    python cli.py                         → Dashboard completo")
    print()
    print("  📈 MÉTRICAS PRINCIPALES:")
    print("    python cli.py kpi                     → Indicadores KPI")
    print("    python cli.py preparacion             → Distribución por preparación laboral")
    print("    python cli.py distritos [N]           → Distribución por distrito (top N)")
    print("    python cli.py semestres               → Distribución por semestre")
    print("    python cli.py edades                  → Distribución por rango de edad")
    print("    python cli.py riesgo                  → Riesgo académico por semestre")
    print("    python cli.py insights                → Insights del análisis")
    print("    python cli.py graficos                → Gráficos de barras en terminal")
    print("    python cli.py graficos-svg            → Generar gráficos SVG con Python")
    print()
    print("  🔧 UTILIDADES:")
    print("    python cli.py raw                     → Ver datos crudos")
    print("    python cli.py refresh                 → Forzar actualización de caché")
    print("    python cli.py list                    → Mostrar esta ayuda")
    print()
    print("  💡 EJEMPLOS:")
    print("    python cli.py distritos 10            → Top 10 distritos")
    print("    python cli.py refresh                 → Recargar datos desde Google Sheets")
    print()


def main():
    args = sys.argv[1:]

    # Sin argumentos → dashboard completo
    if not args:
        show("PERFIL DEL ESTUDIANTE - Dashboard completo", build_dashboard())
        return

    cmd = args[0].lower()

    # Comandos
    if cmd == "kpi":
        show("PERFIL DEL ESTUDIANTE - Indicadores KPI", get_kpi_metrics())
    
    elif cmd in ("preparacion", "job-readiness"):
        data = get_job_readiness_distribution()
        show("PERFIL DEL ESTUDIANTE - Preparación Laboral", data)
        draw_bar_chart(
            "GRÁFICO - Preparación laboral",
            format_preparacion(data),
            "level",
            "student_count",
            "percentage",
        )
    
    elif cmd == "distritos":
        top_n = int(args[1]) if len(args) > 1 and args[1].isdigit() else 6
        data = get_district_distribution(top_n)
        show(f"PERFIL DEL ESTUDIANTE - Distribución por Distrito (Top {top_n})", data)
        draw_bar_chart(
            "GRÁFICO - Distribución por distrito",
            data,
            "distrito",
            "cantidad_estudiantes",
            "porcentaje_participacion",
        )
    
    elif cmd == "semestres":
        data = get_semester_distribution()
        show("PERFIL DEL ESTUDIANTE - Distribución por Semestre", data)
        draw_bar_chart(
            "GRÁFICO - Distribución por semestre",
            data,
            "semestre",
            "cantidad_estudiantes",
            "porcentaje",
        )
    
    elif cmd == "edades":
        data = get_age_distribution()
        show("PERFIL DEL ESTUDIANTE - Distribución por Edad", data)
        draw_bar_chart(
            "GRÁFICO - Distribución por edad",
            data,
            "rango_edad",
            "cantidad_estudiantes",
            "porcentaje",
        )
    
    elif cmd == "riesgo":
        data = get_risk_by_semester()
        show("PERFIL DEL ESTUDIANTE - Riesgo Académico por Semestre", data)
        draw_bar_chart(
            "GRÁFICO - Riesgo por semestre",
            data,
            "semestre",
            "estudiantes_riesgo",
            "porcentaje_riesgo",
        )
    
    elif cmd == "insights":
        show("PERFIL DEL ESTUDIANTE - Insights y Recomendaciones", get_insights())

    elif cmd in ("graficos", "graficas", "charts"):
        show_terminal_charts()

    elif cmd in ("graficos-svg", "graficas-svg", "svg"):
        generate_svg_charts()
    
    elif cmd == "raw":
        show_raw()
    
    elif cmd == "refresh":
        print(HEADER)
        print("  FORZANDO ACTUALIZACIÓN DE CACHÉ")
        print(FOOTER)
        df = reload_data()
        print(f"  ✅ Caché actualizado con {len(df)} registros")
        print(f"  📅 Última actualización: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    elif cmd == "list" or cmd == "help" or cmd == "-h" or cmd == "--help":
        show_list()
    
    else:
        print(f"\n  ❌ Comando '{cmd}' no reconocido.\n")
        print("  Usa 'python cli.py list' para ver todos los comandos disponibles.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
