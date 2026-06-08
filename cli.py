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

W = 76
IW = W - 4

def bar(valor, max_val=5, ancho=22):
    pct = valor / max_val
    lleno = int(pct * ancho)
    vacio = ancho - lleno
    return "▓" * lleno + "░" * vacio

def bar_pct(pct, ancho=22):
    lleno = int(pct / 100 * ancho)
    vacio = ancho - lleno
    return "▓" * lleno + "░" * vacio

def level(valor):
    if valor >= 4.5:
        return "ALTO"
    elif valor >= 3.5:
        return "MEDIO"
    else:
        return "BAJO"

def box_header(title):
    print(f"  ╔{'═' * IW}╗")
    print(f"  ║ {title}{' ' * (IW - len(title) - 1)}║")
    print(f"  ╠{'═' * IW}╣")

def box_footer():
    print(f"  ╚{'═' * IW}╝")
    print()

def box_section(title):
    print(f"  ┌─ {title} {'─' * (IW - len(title) - 3)}┐")

def show_dashboard():
    kpi = get_kpi_metrics().model_dump()
    promedios = get_promedios_habilidades()
    mejorar = get_habilidades_a_mejorar()
    satisfaccion = get_satisfaccion_institucion()
    interes = get_interes_formacion()
    insights_text = get_insights()

    print()
    box_header("HABILIDADES BLANDAS")

    total = f"{kpi['total_estudiantes']} estudiantes"
    prom = f"Promedio: {kpi['promedio_general']}/5"
    sat = f"Satisfechos: {kpi['satisfaccion_institucion_pct']}%"
    inte = f"Interes: {kpi['interes_formacion_pct']}%"
    gap1 = IW - len(total) - len(prom) - 4
    gap2 = IW - len(sat) - len(inte) - 4
    print(f"  ║  {total}{' ' * gap1}{prom}  ║")
    print(f"  ║  {sat}{' ' * gap2}{inte}  ║")
    print(f"  ╠{'═' * IW}╣")

    box_section("PROMEDIOS POR HABILIDAD")
    print(f"  ║  {'Habilidad':30s} {'Barras':26s} {'Punt.':6s} {'Nivel':5s} ║")
    print(f"  ║  {'─' * 30} {'─' * 26} {'─' * 6} {'─' * 5} ║")
    for item in promedios:
        d = item.model_dump()
        b = bar(d['promedio'], ancho=22)
        print(f"  ║  {d['habilidad']:30s} {b:26s} {d['promedio']:<6.2f} {level(d['promedio']):5s} ║")
    print(f"  ╠{'═' * IW}╣")

    box_section("HABILIDADES A MEJORAR")
    print(f"  ║  {'Categoria':38s} {'Barras':26s} {'%':6s} {'#':3s} ║")
    print(f"  ║  {'─' * 38} {'─' * 26} {'─' * 6} {'─' * 3} ║")
    for item in mejorar:
        d = item.model_dump()
        b = bar_pct(d['porcentaje'], ancho=22)
        print(f"  ║  {d['categoria']:38s} {b:26s} {d['porcentaje']:<6.1f} {d['cantidad_estudiantes']:<3d} ║")
    print(f"  ╠{'═' * IW}╣")

    box_section("SATISFACCION INSTITUCIONAL")
    print(f"  ║  {'Respuesta':15s} {'Barras':26s} {'%':6s} {'#':3s} ║")
    print(f"  ║  {'─' * 15} {'─' * 26} {'─' * 6} {'─' * 3} ║")
    for item in satisfaccion:
        d = item.model_dump()
        b = bar_pct(d['porcentaje'], ancho=22)
        print(f"  ║  {d['respuesta']:15s} {b:26s} {d['porcentaje']:<6.1f} {d['cantidad']:<3d} ║")
    print(f"  ╠{'═' * IW}╣")

    box_section("INTERES EN FORMACION")
    print(f"  ║  {'Respuesta':15s} {'Barras':26s} {'%':6s} {'#':3s} ║")
    print(f"  ║  {'─' * 15} {'─' * 26} {'─' * 6} {'─' * 3} ║")
    for item in interes:
        d = item.model_dump()
        b = bar_pct(d['porcentaje'], ancho=22)
        print(f"  ║  {d['respuesta']:15s} {b:26s} {d['porcentaje']:<6.1f} {d['cantidad']:<3d} ║")
    print(f"  ╠{'═' * IW}╣")

    box_section("INSIGHTS")
    words = insights_text.split()
    lines = []
    cur = ""
    for w in words:
        if len(cur) + len(w) + 1 > IW - 4:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    for l in lines:
        print(f"  ║  {l:<{IW-4}s} ║")
    box_footer()


def show_kpi():
    data = get_kpi_metrics().model_dump()
    print()
    box_header("INDICADORES KPI")
    print(f"  ║  {'Total estudiantes':30s} {data['total_estudiantes']:<6d} {'':32s} ║")
    print(f"  ║  {'Promedio general':30s} {data['promedio_general']:<6.2f} {'/ 5':32s} ║")
    print(f"  ║  {'':30s} {bar(data['promedio_general'], ancho=30):30s} ║")
    print(f"  ║  {'Satisfaccion institucion':30s} {data['satisfaccion_institucion_pct']:<6.1f} {'%':32s} ║")
    print(f"  ║  {'':30s} {bar_pct(data['satisfaccion_institucion_pct'], ancho=30):30s} ║")
    print(f"  ║  {'Interes en formacion':30s} {data['interes_formacion_pct']:<6.1f} {'%':32s} ║")
    print(f"  ║  {'':30s} {bar_pct(data['interes_formacion_pct'], ancho=30):30s} ║")
    box_footer()


def show_promedios():
    data = get_promedios_habilidades()
    print()
    box_header("PROMEDIOS POR HABILIDAD")
    print(f"  ║  {'Habilidad':35s} {'Barras':30s} {'Punt.':5s} {'Nivel':5s} ║")
    print(f"  ║  {'─' * 35} {'─' * 30} {'─' * 5} {'─' * 5} ║")
    for item in data:
        d = item.model_dump()
        b = bar(d['promedio'], ancho=26)
        print(f"  ║  {d['habilidad']:35s} {b:30s} {d['promedio']:<5.2f} {level(d['promedio']):5s} ║")
    box_footer()


def show_mejorar():
    data = get_habilidades_a_mejorar()
    print()
    box_header("HABILIDADES A MEJORAR")
    print(f"  ║  {'Categoria':42s} {'Barras':23s} {'%':6s} {'#':3s} ║")
    print(f"  ║  {'─' * 42} {'─' * 23} {'─' * 6} {'─' * 3} ║")
    for item in data:
        d = item.model_dump()
        b = bar_pct(d['porcentaje'], ancho=20)
        print(f"  ║  {d['categoria']:42s} {b:23s} {d['porcentaje']:<6.1f} {d['cantidad_estudiantes']:<3d} ║")
    box_footer()


def show_satisfaccion():
    data = get_satisfaccion_institucion()
    print()
    box_header("SATISFACCION INSTITUCIONAL")
    print(f"  ║  {'Respuesta':15s} {'Barras':23s} {'%':6s} {'#':3s} ║")
    print(f"  ║  {'─' * 15} {'─' * 23} {'─' * 6} {'─' * 3} ║")
    for item in data:
        d = item.model_dump()
        b = bar_pct(d['porcentaje'], ancho=20)
        print(f"  ║  {d['respuesta']:15s} {b:23s} {d['porcentaje']:<6.1f} {d['cantidad']:<3d} ║")
    box_footer()


def show_interes():
    data = get_interes_formacion()
    print()
    box_header("INTERES EN FORMACION")
    print(f"  ║  {'Respuesta':15s} {'Barras':23s} {'%':6s} {'#':3s} ║")
    print(f"  ║  {'─' * 15} {'─' * 23} {'─' * 6} {'─' * 3} ║")
    for item in data:
        d = item.model_dump()
        b = bar_pct(d['porcentaje'], ancho=20)
        print(f"  ║  {d['respuesta']:15s} {b:23s} {d['porcentaje']:<6.1f} {d['cantidad']:<3d} ║")
    box_footer()


def show_insights_view():
    text = get_insights()
    print()
    box_header("INSIGHTS")
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        if len(cur) + len(w) + 1 > IW - 4:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    for l in lines:
        print(f"  ║  {l:<{IW-4}s} ║")
    box_footer()


def show_list():
    print()
    box_header("COMANDOS DISPONIBLES")
    cmds = [
        ("cli.py", "Dashboard completo con todas las metricas"),
        ("cli.py kpi", "Indicadores KPI con barras"),
        ("cli.py promedios", "Promedios por habilidad blanda"),
        ("cli.py mejorar", "Habilidades a mejorar"),
        ("cli.py satisfaccion", "Satisfaccion institucional"),
        ("cli.py interes", "Interes en formacion"),
        ("cli.py insights", "Analisis narrativo"),
        ("cli.py refresh", "Recargar datos del dashboard"),
        ("cli.py list", "Mostrar esta ayuda"),
    ]
    for cmd, desc in cmds:
        gap = IW - len(cmd) - len(desc) - 6
        print(f"  ║    python {cmd}{' ' * gap}{desc}  ║")
    box_footer()


def main():
    args = sys.argv[1:]

    if not args:
        show_dashboard()
        return

    cmd = args[0].lower()

    if cmd == "kpi":
        show_kpi()
    elif cmd == "promedios":
        show_promedios()
    elif cmd == "mejorar":
        show_mejorar()
    elif cmd == "satisfaccion":
        show_satisfaccion()
    elif cmd == "interes":
        show_interes()
    elif cmd == "insights":
        show_insights_view()
    elif cmd == "refresh":
        invalidate_cache()
        build_dashboard(force_refresh=True)
        show_dashboard()
    elif cmd in ("list", "help", "-h", "--help"):
        show_list()
    else:
        print(f"\n  Comando '{cmd}' no reconocido.\n")
        print("  Usa 'python cli.py list' para ver los comandos disponibles.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
