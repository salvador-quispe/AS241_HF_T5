"""
CLI - Habilidades Blandas

Uso:
  python cli.py                         Dashboard completo
  python cli.py kpi                     Solo KPI
  python cli.py promedios               Promedios por habilidad blanda
  python cli.py mejorar                 Habilidades a mejorar (respuestas abiertas)
  python cli.py satisfaccion            Satisfacción institucional
  python cli.py interes                 Interés en más formación
  python cli.py insights                Insights del análisis
  python cli.py refresh                 Forzar actualización de caché
  python cli.py list                    Listar comandos disponibles
"""

import sys
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)
pd.set_option("display.max_colwidth", 60)

from app.services.habilidades_blandas_service import (
    build_dashboard,
    get_kpi_metrics,
    get_promedios_habilidades,
    get_habilidades_a_mejorar,
    get_satisfaccion_institucion,
    get_interes_formacion,
    get_insights,
    invalidate_cache
)

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


def show_list():
    """Display available commands"""
    print(HEADER)
    print("  COMANDOS DISPONIBLES - Habilidades Blandas")
    print(FOOTER)

    print("\n  📊 DASHBOARD COMPLETO:")
    print("    python cli.py                         → Dashboard completo")
    print()
    print("  📈 MÉTRICAS PRINCIPALES:")
    print("    python cli.py kpi                     → Indicadores KPI")
    print("    python cli.py promedios               → Promedios por habilidad blanda")
    print("    python cli.py mejorar                 → Habilidades a mejorar (texto libre)")
    print("    python cli.py satisfaccion            → Satisfacción institucional")
    print("    python cli.py interes                 → Interés en más formación")
    print("    python cli.py insights                → Insights del análisis")
    print()
    print("  🔧 UTILIDADES:")
    print("    python cli.py refresh                 → Forzar actualización de caché")
    print("    python cli.py list                    → Mostrar esta ayuda")
    print()


def main():
    args = sys.argv[1:]

    # Sin argumentos → dashboard completo
    if not args:
        show("HABILIDADES BLANDAS - Dashboard completo", build_dashboard())
        return

    cmd = args[0].lower()

    if cmd == "kpi":
        show("HABILIDADES BLANDAS - Indicadores KPI", get_kpi_metrics())

    elif cmd == "promedios":
        data = get_promedios_habilidades()
        print(HEADER)
        print("  HABILIDADES BLANDAS - Promedios por habilidad")
        print(FOOTER)
        for item in data:
            d = item.model_dump() if hasattr(item, 'model_dump') else item
            print(f"  • {d['habilidad']}: {d['promedio']} ({d['nivel']})")
        print()

    elif cmd == "mejorar":
        data = get_habilidades_a_mejorar()
        print(HEADER)
        print("  HABILIDADES BLANDAS - Habilidades a mejorar")
        print(FOOTER)
        for item in data:
            d = item.model_dump() if hasattr(item, 'model_dump') else item
            print(f"  • {d['categoria']}: {d['cantidad_estudiantes']} estudiantes ({d['porcentaje']}%)")
        print()

    elif cmd == "satisfaccion":
        data = get_satisfaccion_institucion()
        print(HEADER)
        print("  HABILIDADES BLANDAS - Satisfacción institucional")
        print(FOOTER)
        for item in data:
            d = item.model_dump() if hasattr(item, 'model_dump') else item
            print(f"  • {d['respuesta']}: {d['cantidad']} ({d['porcentaje']}%)")
        print()

    elif cmd == "interes":
        data = get_interes_formacion()
        print(HEADER)
        print("  HABILIDADES BLANDAS - Interés en más formación")
        print(FOOTER)
        for item in data:
            d = item.model_dump() if hasattr(item, 'model_dump') else item
            print(f"  • {d['respuesta']}: {d['cantidad']} ({d['porcentaje']}%)")
        print()

    elif cmd == "insights":
        print(HEADER)
        print("  HABILIDADES BLANDAS - Insights y análisis")
        print(FOOTER)
        print(f"  {get_insights()}")
        print()

    elif cmd == "refresh":
        print(HEADER)
        print("  FORZANDO ACTUALIZACIÓN DE CACHÉ")
        print(FOOTER)
        invalidate_cache()
        build_dashboard(force_refresh=True)
        print(f"  ✅ Caché actualizado")
        print(f"  📅 Última actualización: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

    elif cmd in ("list", "help", "-h", "--help"):
        show_list()

    else:
        print(f"\n  ❌ Comando '{cmd}' no reconocido.\n")
        print("  Usa 'python cli.py list' para ver todos los comandos disponibles.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()