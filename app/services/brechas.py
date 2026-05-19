import pandas as pd
import numpy as np
from app.schemas.brechas import DashboardBrechas

FREQ_ORDER = ["Nunca", "A veces", "Frecuentemente", "Siempre"]


def _distribucion(series: pd.Series) -> dict:
    counts = series.value_counts(dropna=False).sort_index().to_dict()
    return {str(k): int(v) for k, v in counts.items()}


def build_dashboard(df: pd.DataFrame) -> DashboardBrechas:
    if df.empty:
        return DashboardBrechas(
            nivel_conocimientos_tecnicos={"promedio": 0, "distribucion": {}},
            nivel_dominio_digital={"promedio": 0, "distribucion": {}},
            frecuencia_uso_digital={"frecuencia": {"Nunca": 0, "A veces": 0, "Frecuentemente": 0, "Siempre": 0}},
            formacion_digital={"con_formacion": 0, "sin_formacion": 0, "porcentaje_con_formacion": 0},
            herramientas_mas_usadas={"items": []},
            preparacion_laboral={"promedio": 0, "distribucion": {}},
            habilidades_mejorar={"items": []},
            brecha_tecnica_promedio={"promedio": 0, "maximo": 0, "minimo": 0},
            brecha_digital_promedio={"promedio": 0, "maximo": 0, "minimo": 0},
            brecha_habilidades_blandas={"promedio_comunicacion": 0, "promedio_trabajo_equipo": 0, "promedio_resolucion_problemas": 0, "promedio_adaptabilidad": 0, "promedio_organizacion": 0},
            estudiantes_sin_formacion_digital={"cantidad": 0, "porcentaje": 0},
            estudiantes_bajo_dominio_tecnologico={"cantidad": 0, "porcentaje": 0},
            uso_herramientas_carrera={"porcentaje_uso_frecuente": 0, "distribucion": {}},
            comparacion_carrera={"items": []},
            comparacion_semestre={"items": []},
            comparacion_edad={"items": []},
        )

    # 1. Nivel de conocimientos técnicos
    tec = df["nivel_conocimientos_tecnicos"].dropna()
    nivel_tec = {
        "promedio": round(float(tec.mean()), 2),
        "distribucion": _distribucion(tec),
    }

    # 2. Nivel de dominio de herramientas digitales
    dom = df["nivel_dominio_herramientas_digitales"].dropna()
    nivel_dom = {
        "promedio": round(float(dom.mean()), 2),
        "distribucion": _distribucion(dom),
    }

    # 3. Frecuencia de uso de herramientas digitales
    freq = df["frecuencia_uso_herramientas_digitales"].dropna()
    freq_counts = freq.value_counts().to_dict()
    freq_dict = {}
    for f in FREQ_ORDER:
        freq_dict[f] = int(freq_counts.get(f, 0))

    # 4. Formación en herramientas digitales
    form = df["formacion_herramientas_digitales"].dropna()
    con_form = int((form == "Si").sum())
    sin_form = int((form == "No").sum())
    total_f = con_form + sin_form
    formacion = {
        "con_formacion": con_form,
        "sin_formacion": sin_form,
        "porcentaje_con_formacion": round(con_form / total_f * 100, 1) if total_f else 0,
    }

    # 5. Herramientas digitales más utilizadas
    all_tools = df["herramientas_digitales"].dropna().str.split(",")
    tool_series = all_tools.explode().str.strip()
    tool_counts = tool_series.value_counts().head(10).reset_index()
    tool_counts.columns = ["herramienta", "conteo"]
    herramientas = [
        {"herramienta": row["herramienta"], "conteo": int(row["conteo"])}
        for _, row in tool_counts.iterrows()
    ]

    # 6. Nivel de preparación para aplicar conocimientos
    prep = df["preparado_aplicar_conocimientos"].dropna()
    prep_lab = {
        "promedio": round(float(prep.mean()), 2),
        "distribucion": _distribucion(prep),
    }

    # 7. Habilidades que necesitan mejorar
    all_skills = df["habilidades_a_mejorar"].dropna().str.lower()
    skill_keywords = {
        "comunicación": ["comunicación", "comunicacion", "comunicativo", "hablar", "social"],
        "trabajo en equipo": ["trabajo en equipo", "equipo", "colaboración"],
        "programación": ["programación", "programacion", "códigos", "código", "codigo", "desarrollar"],
        "lógica": ["lógica", "logica", "algoritmo"],
        "gestión del tiempo": ["tiempo", "organización", "organizacion", "planificación"],
        "adaptabilidad": ["adaptabilidad", "adaptación", "adaptacion", "cambio"],
        "disciplina": ["disciplina", "constancia", "práctica", "practica"],
        "herramientas digitales": ["herramientas digitales", "herramientas", "digitales"],
        "liderazgo": ["liderazgo"],
        "retención": ["retención", "retencion", "memoria", "memorizar"],
    }
    skill_hits = {}
    for skill, keywords in skill_keywords.items():
        for kw in keywords:
            count = all_skills.str.contains(kw, na=False).sum()
            skill_hits[skill] = skill_hits.get(skill, 0) + count
    sorted_skills = sorted(skill_hits.items(), key=lambda x: -x[1])
    habilidades = [{"habilidad": s, "conteo": int(c)} for s, c in sorted_skills if c > 0]

    # 8. Brecha técnica promedio
    brecha_tec = {
        "promedio": round(float(tec.mean()), 2),
        "maximo": int(tec.max()) if not tec.empty else 0,
        "minimo": int(tec.min()) if not tec.empty else 0,
    }

    # 9. Brecha digital promedio
    brecha_dig = {
        "promedio": round(float(dom.mean()), 2),
        "maximo": int(dom.max()) if not dom.empty else 0,
        "minimo": int(dom.min()) if not dom.empty else 0,
    }

    # 10. Brecha de habilidades blandas
    soft_cols = {
        "promedio_comunicacion": "importancia_comunicacion_efectiva",
        "promedio_trabajo_equipo": "importancia_trabajo_equipo",
        "promedio_resolucion_problemas": "importancia_resolucion_problemas",
        "promedio_adaptabilidad": "importancia_adaptabilidad",
        "promedio_organizacion": "importancia_organizacion_tiempo",
    }
    soft = {}
    for k, col in soft_cols.items():
        vals = df[col].dropna()
        soft[k] = round(float(vals.mean()), 2) if not vals.empty else 0

    # 11. Estudiantes sin formación digital
    sin_formacion = {
        "cantidad": sin_form,
        "porcentaje": round(sin_form / total_f * 100, 1) if total_f else 0,
    }

    # 12. Estudiantes con bajo dominio tecnológico (<=2)
    bajo_dom = int((dom <= 2).sum()) if not dom.empty else 0
    total_dom = int(dom.count()) if not dom.empty else 1
    bajo_dominio = {
        "cantidad": bajo_dom,
        "porcentaje": round(bajo_dom / total_dom * 100, 1),
    }

    # 13. Porcentaje que usa herramientas de su carrera frecuentemente+
    freq_carrera = df["frecuencia_uso_herramientas_carrera"].dropna()
    uso_frec = int((freq_carrera.isin(["Frecuentemente", "Siempre"])).sum())
    total_fc = int(freq_carrera.count())
    uso_carrera = {
        "porcentaje_uso_frecuente": round(uso_frec / total_fc * 100, 1) if total_fc else 0,
        "distribucion": _distribucion(freq_carrera),
    }

    # 14. Comparación por carrera
    carrera_grp = df.groupby("carrera")["nivel_conocimientos_tecnicos"].mean().dropna()
    comp_carrera = [
        {"carrera": k, "promedio": round(float(v), 2)}
        for k, v in carrera_grp.items()
    ]

    # 15. Comparación por semestre
    sem_grp = df.groupby("semestre")["nivel_conocimientos_tecnicos"].mean().dropna()
    comp_sem = [
        {"semestre": k, "promedio": round(float(v), 2)}
        for k, v in sem_grp.items()
    ]

    # 16. Comparación por edad
    df_edad = df.copy()
    bins = [0, 18, 22, 26, 100]
    labels = ["17-18", "19-22", "23-26", "27+"]
    df_edad["grupo_edad"] = pd.cut(df_edad["edad"], bins=bins, labels=labels)
    edad_grp = df_edad.groupby("grupo_edad", observed=True)["nivel_conocimientos_tecnicos"].mean().dropna()
    comp_edad = [
        {"grupo_edad": k, "promedio": round(float(v), 2)}
        for k, v in edad_grp.items()
    ]

    return DashboardBrechas(
        nivel_conocimientos_tecnicos=nivel_tec,
        nivel_dominio_digital=nivel_dom,
        frecuencia_uso_digital={"frecuencia": freq_dict},
        formacion_digital=formacion,
        herramientas_mas_usadas={"items": herramientas},
        preparacion_laboral=prep_lab,
        habilidades_mejorar={"items": habilidades},
        brecha_tecnica_promedio=brecha_tec,
        brecha_digital_promedio=brecha_dig,
        brecha_habilidades_blandas=soft,
        estudiantes_sin_formacion_digital=sin_formacion,
        estudiantes_bajo_dominio_tecnologico=bajo_dominio,
        uso_herramientas_carrera=uso_carrera,
        comparacion_carrera={"items": comp_carrera},
        comparacion_semestre={"items": comp_sem},
        comparacion_edad={"items": comp_edad},
    )
