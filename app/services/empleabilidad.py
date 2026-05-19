import pandas as pd
import numpy as np
from app.schemas.empleabilidad import DashboardEmpleabilidad

DIFICULTAD_ORDER = ["Facil", "Moderado", "Dificil"]


def _distribucion(series: pd.Series) -> dict:
    counts = series.value_counts(dropna=False).sort_index().to_dict()
    return {str(k): int(v) for k, v in counts.items()}


def build_dashboard(df: pd.DataFrame) -> DashboardEmpleabilidad:
    if df.empty:
        return DashboardEmpleabilidad(
            nivel_preparacion_mercado={"promedio": 0, "distribucion": {}},
            preparacion_institucional={"promedio": 0, "distribucion": {}},
            dificultad_conseguir_trabajo={"items": []},
            practicas_preprofesionales={"con_practicas": 0, "sin_practicas": 0, "porcentaje_con_practicas": 0},
            interes_formacion={"si": 0, "no": 0, "porcentaje_interes": 0},
            importancia_comunicacion={"promedio": 0, "distribucion": {}},
            importancia_trabajo_equipo={"promedio": 0, "distribucion": {}},
            importancia_resolucion_problemas={"promedio": 0, "distribucion": {}},
            importancia_adaptabilidad={"promedio": 0, "distribucion": {}},
            importancia_organizacion_tiempo={"promedio": 0, "distribucion": {}},
            importancia_centro_evaluacion={"promedio": 0, "distribucion": {}},
            comparacion_carrera={"items": []},
            comparacion_semestre={"items": []},
            ranking_habilidades_valoradas={"items": []},
            ranking_habilidades_debiles={"items": []},
            indicador_general_empleabilidad={"promedio_general": 0, "nivel": "Sin datos"},
            estudiantes_listos_mercado={"cantidad": 0, "porcentaje": 0},
            estudiantes_insuficiente_preparacion={"cantidad": 0, "porcentaje": 0},
        )

    # 1. Nivel de preparación para ingresar al mercado laboral
    prep = df["preparado_ingresar_mercado_laboral"].dropna()
    nivel_prep = {
        "promedio": round(float(prep.mean()), 2),
        "distribucion": _distribucion(prep),
    }

    # 2. Nivel de preparación institucional percibida
    inst = df["institucion_preparo_adecuadamente"].dropna()
    inst_map = {"Si": 3, "Parcialmente": 2, "No": 1}
    inst_num = inst.map(inst_map).dropna()
    inst_prom = round(float(inst_num.mean()), 2) if not inst_num.empty else 0
    prep_inst = {
        "promedio": inst_prom,
        "distribucion": _distribucion(inst),
    }

    # 3. Dificultad percibida para conseguir trabajo
    dif = df["dificultad_conseguir_trabajo"].dropna()
    dif_counts = dif.value_counts().to_dict()
    dif_items = []
    for d in DIFICULTAD_ORDER:
        dif_items.append({
            "dificultad": d,
            "conteo": int(dif_counts.get(d, 0)),
            "porcentaje": round(dif_counts.get(d, 0) / len(dif) * 100, 1) if len(dif) else 0,
        })

    # 4. Porcentaje con prácticas preprofesionales
    prac = df["realizo_practicas_preprofesionales"].dropna()
    con_prac = int((prac == "Si").sum())
    sin_prac = int((prac == "No").sum())
    total_p = con_prac + sin_prac
    practicas = {
        "con_practicas": con_prac,
        "sin_practicas": sin_prac,
        "porcentaje_con_practicas": round(con_prac / total_p * 100, 1) if total_p else 0,
    }

    # 5. Interés en recibir más formación profesional
    form = df["recibir_mas_formacion"].dropna()
    si_form = int((form == "Si").sum())
    no_form = int((form == "No").sum())
    total_f = si_form + no_form
    interes = {
        "si": si_form,
        "no": no_form,
        "porcentaje_interes": round(si_form / total_f * 100, 1) if total_f else 0,
    }

    # 6-11. Importancia de cada habilidad blanda
    imp_cols = {
        "importancia_comunicacion": "importancia_comunicacion_efectiva",
        "importancia_trabajo_equipo": "importancia_trabajo_equipo",
        "importancia_resolucion_problemas": "importancia_resolucion_problemas",
        "importancia_adaptabilidad": "importancia_adaptabilidad",
        "importancia_organizacion_tiempo": "importancia_organizacion_tiempo",
        "importancia_centro_evaluacion": "importancia_centro_evaluacion",
    }

    importancias = {}
    for k, col in imp_cols.items():
        vals = df[col].dropna()
        importancias[k] = {
            "promedio": round(float(vals.mean()), 2),
            "distribucion": _distribucion(vals),
        }

    # 12. Comparación de empleabilidad por carrera
    carrera_prep = df.groupby("carrera")["preparado_ingresar_mercado_laboral"].mean().dropna()
    comp_carrera = [
        {"carrera": k, "promedio": round(float(v), 2)}
        for k, v in carrera_prep.items()
    ]

    # 13. Comparación por semestre
    sem_prep = df.groupby("semestre")["preparado_ingresar_mercado_laboral"].mean().dropna()
    comp_sem = [
        {"semestre": k, "promedio": round(float(v), 2)}
        for k, v in sem_prep.items()
    ]

    # 14. Ranking de habilidades más valoradas
    ranking = sorted(
        [
            ("Comunicación efectiva", float(df["importancia_comunicacion_efectiva"].dropna().mean())),
            ("Trabajo en equipo", float(df["importancia_trabajo_equipo"].dropna().mean())),
            ("Resolución de problemas", float(df["importancia_resolucion_problemas"].dropna().mean())),
            ("Adaptabilidad", float(df["importancia_adaptabilidad"].dropna().mean())),
            ("Organización y tiempo", float(df["importancia_organizacion_tiempo"].dropna().mean())),
        ],
        key=lambda x: -x[1],
    )
    ranking_val = [{"habilidad": h, "promedio": round(v, 2)} for h, v in ranking]

    # 15. Ranking de habilidades más débiles (inverso)
    ranking_deb = [
        {"habilidad": h, "promedio": round(v, 2)} for h, v in reversed(ranking)
    ]

    # 16. Indicador general de empleabilidad
    prep_lab = float(df["preparado_ingresar_mercado_laboral"].dropna().mean())
    prep_inst_val = inst_prom / 3 * 5 if inst_prom else 0
    ind_gral = round((prep_lab + prep_inst_val) / 2, 2)
    nivel = (
        "Alto" if ind_gral >= 4 else
        "Medio" if ind_gral >= 2.5 else
        "Bajo"
    )
    indicador_gral = {
        "promedio_general": ind_gral,
        "nivel": nivel,
    }

    # 17. Estudiantes listos para el mercado laboral (preparación >= 4)
    listos = int((prep >= 4).sum()) if not prep.empty else 0
    total_prep = int(prep.count())
    listos_mercado = {
        "cantidad": listos,
        "porcentaje": round(listos / total_prep * 100, 1) if total_prep else 0,
    }

    # 18. Estudiantes que consideran insuficiente la preparación institucional
    insuf = int((inst == "No").sum())
    total_inst = int(inst.count())
    insuf_prep = {
        "cantidad": insuf,
        "porcentaje": round(insuf / total_inst * 100, 1) if total_inst else 0,
    }

    return DashboardEmpleabilidad(
        nivel_preparacion_mercado=nivel_prep,
        preparacion_institucional=prep_inst,
        dificultad_conseguir_trabajo={"items": dif_items},
        practicas_preprofesionales=practicas,
        interes_formacion=interes,
        importancia_comunicacion=importancias["importancia_comunicacion"],
        importancia_trabajo_equipo=importancias["importancia_trabajo_equipo"],
        importancia_resolucion_problemas=importancias["importancia_resolucion_problemas"],
        importancia_adaptabilidad=importancias["importancia_adaptabilidad"],
        importancia_organizacion_tiempo=importancias["importancia_organizacion_tiempo"],
        importancia_centro_evaluacion=importancias["importancia_centro_evaluacion"],
        comparacion_carrera={"items": comp_carrera},
        comparacion_semestre={"items": comp_sem},
        ranking_habilidades_valoradas={"items": ranking_val},
        ranking_habilidades_debiles={"items": ranking_deb},
        indicador_general_empleabilidad=indicador_gral,
        estudiantes_listos_mercado=listos_mercado,
        estudiantes_insuficiente_preparacion=insuf_prep,
    )
