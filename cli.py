"""
CLI - Perfil del Estudiante

Uso:
  python cli.py                         Dashboard completo
  python cli.py kpi                     Solo KPI
  python cli.py genero                  Distribución por género
  python cli.py carreras                Distribución por carreras
  python cli.py distritos [N]           Distribución por distritos (top N)
  python cli.py semestres               Distribución por semestres
  python cli.py edades                  Distribución por edades
  python cli.py riesgo                  Riesgo académico por semestre
  python cli.py insights                Insights del análisis
  python cli.py raw                     Datos crudos
  python cli.py refresh                 Forzar actualización de caché
  python cli.py list                    Listar comandos disponibles
"""

import sys
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)
pd.set_option("display.max_colwidth", 50)

from app.services.student_profile_service import (
    build_dashboard,
    get_kpi_metrics,
    get_gender_distribution,
    get_career_distribution,
    get_district_distribution,
    get_semester_distribution,
    get_age_distribution,
    get_risk_by_semester,
    get_insights
)
from app.config.database import get_data, reload_data

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
    print("    python cli.py genero                  → Distribución por género")
    print("    python cli.py carreras                → Distribución por carrera")
    print("    python cli.py distritos [N]           → Distribución por distrito (top N)")
    print("    python cli.py semestres               → Distribución por semestre")
    print("    python cli.py edades                  → Distribución por rango de edad")
    print("    python cli.py riesgo                  → Riesgo académico por semestre")
    print("    python cli.py insights                → Insights del análisis")
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
    
    elif cmd == "genero":
        show("PERFIL DEL ESTUDIANTE - Distribución por Género", get_gender_distribution())
    
    elif cmd == "carreras":
        show("PERFIL DEL ESTUDIANTE - Distribución por Carrera", get_career_distribution())
    
    elif cmd == "distritos":
        top_n = int(args[1]) if len(args) > 1 and args[1].isdigit() else 6
        show(f"PERFIL DEL ESTUDIANTE - Distribución por Distrito (Top {top_n})", get_district_distribution(top_n))
    
    elif cmd == "semestres":
        show("PERFIL DEL ESTUDIANTE - Distribución por Semestre", get_semester_distribution())
    
    elif cmd == "edades":
        show("PERFIL DEL ESTUDIANTE - Distribución por Edad", get_age_distribution())
    
    elif cmd == "riesgo":
        show("PERFIL DEL ESTUDIANTE - Riesgo Académico por Semestre", get_risk_by_semester())
    
    elif cmd == "insights":
        show("PERFIL DEL ESTUDIANTE - Insights y Recomendaciones", get_insights())
    
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