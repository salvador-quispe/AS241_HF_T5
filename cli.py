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

try:
    from app.services.habilidades_tecnicas_service import (
        build_dashboard as build_dashboard_tecnicas,
        get_kpi_metrics as get_kpi_tecnicas,
        get_matriz_operacional,
        get_nivel_tecnico,
        invalidate_cache as invalidate_cache_tecnicas,
    )
    _tecnicas_available = True
except ImportError:
    _tecnicas_available = False

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
    print(f"  ║  {'HABILIDADES BLANDAS':72s} ║")
    cmds_b = [
        ("cli.py", "Dashboard completo"),
        ("cli.py kpi", "Indicadores KPI"),
        ("cli.py promedios", "Promedios por habilidad"),
        ("cli.py mejorar", "Habilidades a mejorar"),
        ("cli.py satisfaccion", "Satisfaccion institucional"),
        ("cli.py interes", "Interes en formacion"),
        ("cli.py insights", "Analisis narrativo"),
        ("cli.py refresh", "Recargar datos"),
    ]
    for cmd, desc in cmds_b:
        gap = IW - len(cmd) - len(desc) - 6
        print(f"  ║    python {cmd}{' ' * gap}{desc}  ║")
    if _tecnicas_available:
        print(f"  ║  {'':72s} ║")
        print(f"  ║  {'HABILIDADES TECNICAS':72s} ║")
        cmds_t = [
            ("cli.py tecnicas", "Dashboard completo tecnicas"),
            ("cli.py tecnicas-kpi", "KPI tecnicas"),
            ("cli.py tecnicas-nivel", "Nivel tecnico"),
            ("cli.py tecnicas-matriz", "Matriz Operacional"),
            ("cli.py tecnicas-refresh", "Recargar datos tecnicas"),
        ]
        for cmd, desc in cmds_t:
            gap = IW - len(cmd) - len(desc) - 6
            print(f"  ║    python {cmd}{' ' * gap}{desc}  ║")
    print(f"  ║  {'':72s} ║")
    print(f"  ║  {'AYUDA':72s} ║")
    print(f"  ║    python cli.py list{' ' * (IW - 23)}║")
    box_footer()


def _tecnicas_not_available():
    print(f"\n  ║  Modulo de Habilidades Tecnicas no disponible  ║\n")


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
    elif cmd == "tecnicas":
        if _tecnicas_available:
            show_dashboard_tecnicas()
        else:
            _tecnicas_not_available()
    elif cmd == "tecnicas-kpi":
        if _tecnicas_available:
            show_kpi_tecnicas()
        else:
            _tecnicas_not_available()
    elif cmd == "tecnicas-nivel":
        if _tecnicas_available:
            show_nivel_tecnico()
        else:
            _tecnicas_not_available()
    elif cmd == "tecnicas-matriz":
        if _tecnicas_available:
            show_matriz()
        else:
            _tecnicas_not_available()
    elif cmd == "tecnicas-refresh":
        if _tecnicas_available:
            invalidate_cache_tecnicas()
            build_dashboard_tecnicas(force_refresh=True)
            show_dashboard_tecnicas()
        else:
            _tecnicas_not_available()
    elif cmd in ("list", "help", "-h", "--help"):
        show_list()
    else:
        print(f"\n  Comando '{cmd}' no reconocido.\n")
        print("  Usa 'python cli.py list' para ver los comandos disponibles.\n")
        sys.exit(1)


def show_dashboard_tecnicas():
    data = build_dashboard_tecnicas()
    print()
    box_header("HABILIDADES TECNICAS")
    if hasattr(data, 'model_dump'):
        data = data.model_dump()
    for k, v in data.items():
        k_show = k.replace("_", " ").title()
        print(f"  ║  {k_show:35s} {str(v):<37s} ║")
    box_footer()


def show_kpi_tecnicas():
    data = get_kpi_tecnicas().model_dump()
    print()
    box_header("INDICADORES KPI - TECNICAS")
    for k, v in data.items():
        k_show = k.replace("_", " ").title()
        print(f"  ║  {k_show:35s} {str(v):<35s} ║")
    box_footer()


def show_matriz():
    data = get_matriz_operacional()
    print()
    box_header("MATRIZ OPERACIONAL DE REQUERIMIENTOS")
    subcats = data.subcategorias if hasattr(data, 'subcategorias') else []
    for item in subcats:
        d = item.model_dump() if hasattr(item, 'model_dump') else item
        cat = d.get('categoria', '')
        votos = d.get('votos', 0)
        pct = d.get('porcentaje_del_subtotal', 0)
        b = bar_pct(pct, ancho=30)
        print(f"  ║  {cat:42s} {b:32s} {pct:<5.1f}% ({votos} votos) ║")
    box_footer()


def show_nivel_tecnico():
    data = get_nivel_tecnico()
    d = data.model_dump() if hasattr(data, 'model_dump') else data
    print()
    box_header("NIVEL TECNICO - CONOCIMIENTO Y APLICACION")
    for k, v in d.items():
        k_show = k.replace("_", " ").title()
        print(f"  ║  {k_show:40s} {str(v):<32s} ║")
    box_footer()


if __name__ == "__main__":
    main()
