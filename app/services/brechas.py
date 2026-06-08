import pandas as pd
import numpy as np
import io
import csv
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


def build_looker_flat(df: pd.DataFrame) -> list:
    dashboard = build_dashboard(df)
    d = dashboard.model_dump()
    row = {}

    row["conocimiento_tecnico_promedio"] = d["nivel_conocimientos_tecnicos"]["promedio"]
    row["dominio_digital_promedio"] = d["nivel_dominio_digital"]["promedio"]
    row["formacion_digital_porcentaje"] = d["formacion_digital"]["porcentaje_con_formacion"]
    row["brecha_tecnica_promedio"] = d["brecha_tecnica_promedio"]["promedio"]
    row["brecha_digital_promedio"] = d["brecha_digital_promedio"]["promedio"]
    row["uso_herramientas_frecuente_porcentaje"] = d["uso_herramientas_carrera"]["porcentaje_uso_frecuente"]

    for k, v in d["nivel_conocimientos_tecnicos"]["distribucion"].items():
        row[f"conocimiento_tecnico_n{k}"] = v
    for k, v in d["nivel_dominio_digital"]["distribucion"].items():
        row[f"dominio_digital_n{k}"] = v

    row["preparacion_laboral_promedio"] = d["preparacion_laboral"]["promedio"]
    for k, v in d["preparacion_laboral"]["distribucion"].items():
        row[f"preparacion_laboral_n{k}"] = v

    row["con_formacion"] = d["formacion_digital"]["con_formacion"]
    row["sin_formacion"] = d["formacion_digital"]["sin_formacion"]
    row["sin_formacion_porcentaje"] = d["estudiantes_sin_formacion_digital"]["porcentaje"]

    row["bajo_dominio_cantidad"] = d["estudiantes_bajo_dominio_tecnologico"]["cantidad"]
    row["bajo_dominio_porcentaje"] = d["estudiantes_bajo_dominio_tecnologico"]["porcentaje"]

    for item in d["habilidades_mejorar"]["items"]:
        key = "habilidad_" + item["habilidad"].replace(" ", "_").replace("í", "i").replace("ó", "o").replace("é", "e")
        row[key] = item["conteo"]

    tool_map = {}
    for item in d["herramientas_mas_usadas"]["items"]:
        h = item["herramienta"].lower()
        if "word" in h:
            tool_map["herramienta_word"] = item["conteo"]
        elif "vscode" in h or "visual studio" in h or "editor" in h:
            tool_map["herramienta_vscode"] = item["conteo"]
        elif "intellij" in h:
            tool_map["herramienta_intellij"] = item["conteo"]
        elif "chatgpt" in h or "ia" in h:
            tool_map["herramienta_chatgpt"] = item["conteo"]
        elif "gemini" in h:
            tool_map["herramienta_gemini"] = item["conteo"]
        elif "excel" in h or "sheets" in h:
            tool_map["herramienta_excel"] = item["conteo"]
        elif "git" in h:
            tool_map["herramienta_git"] = item["conteo"]
        elif "mysql" in h or "base" in h:
            tool_map["herramienta_mysql"] = item["conteo"]
        elif "postgres" in h:
            tool_map["herramienta_postgresql"] = item["conteo"]
    row.update(tool_map)

    row["frecuencia_nunca"] = d["frecuencia_uso_digital"]["frecuencia"].get("Nunca", 0)
    row["frecuencia_aveces"] = d["frecuencia_uso_digital"]["frecuencia"].get("A veces", 0)
    row["frecuencia_frecuentemente"] = d["frecuencia_uso_digital"]["frecuencia"].get("Frecuentemente", 0)
    row["frecuencia_siempre"] = d["frecuencia_uso_digital"]["frecuencia"].get("Siempre", 0)

    for item in d["comparacion_semestre"]["items"]:
        sem = str(item["semestre"])[0]
        row[f"semestre_{sem}"] = item["promedio"]

    for item in d["comparacion_edad"]["items"]:
        edad = item["grupo_edad"].replace("-", "_").replace("+", "_mas")
        row[f"edad_{edad}"] = item["promedio"]

    return [row]



def build_looker_csv(df: pd.DataFrame) -> str:
    dashboard = build_dashboard(df)
    data = dashboard.model_dump()
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    writer.writerow(["indicador", "categoria", "etiqueta", "valor"])

    def write(key, cat, label, val):
        writer.writerow([key, cat, label, val])

    # 1-2. Conocimientos técnicos y dominio digital
    for key in ["nivel_conocimientos_tecnicos", "nivel_dominio_digital"]:
        d = data[key]
        write(key, "promedio", "", d["promedio"])
        for k, v in d["distribucion"].items():
            write(key, "distribucion", k, v)

    # 3. Frecuencia uso digital
    for k, v in data["frecuencia_uso_digital"]["frecuencia"].items():
        write("frecuencia_uso_digital", "frecuencia", k, v)

    # 4. Formación digital
    f = data["formacion_digital"]
    write("formacion_digital", "conteo", "con_formacion", f["con_formacion"])
    write("formacion_digital", "conteo", "sin_formacion", f["sin_formacion"])
    write("formacion_digital", "porcentaje", "porcentaje_con_formacion", f["porcentaje_con_formacion"])

    # 5. Herramientas más usadas
    for item in data["herramientas_mas_usadas"]["items"]:
        write("herramientas_mas_usadas", item["herramienta"], "conteo", item["conteo"])

    # 6. Preparación laboral
    p = data["preparacion_laboral"]
    write("preparacion_laboral", "promedio", "", p["promedio"])
    for k, v in p["distribucion"].items():
        write("preparacion_laboral", "distribucion", k, v)

    # 7. Habilidades a mejorar
    for item in data["habilidades_mejorar"]["items"]:
        write("habilidades_mejorar", item["habilidad"], "conteo", item["conteo"])

    # 8-9. Brecha técnica y digital
    for key in ["brecha_tecnica_promedio", "brecha_digital_promedio"]:
        b = data[key]
        write(key, "promedio", "", b["promedio"])
        write(key, "maximo", "", b["maximo"])
        write(key, "minimo", "", b["minimo"])

    # 10. Brecha habilidades blandas
    for k, v in data["brecha_habilidades_blandas"].items():
        write("brecha_habilidades_blandas", k, "", v)

    # 11-12. Sin formación / bajo dominio
    for key in ["estudiantes_sin_formacion_digital", "estudiantes_bajo_dominio_tecnologico"]:
        s = data[key]
        write(key, "cantidad", "", s["cantidad"])
        write(key, "porcentaje", "", s["porcentaje"])

    # 13. Uso herramientas carrera
    u = data["uso_herramientas_carrera"]
    write("uso_herramientas_carrera", "porcentaje_uso_frecuente", "", u["porcentaje_uso_frecuente"])
    for k, v in u["distribucion"].items():
        write("uso_herramientas_carrera", "distribucion", k, v)

    # 14. Comparación carrera
    for item in data["comparacion_carrera"]["items"]:
        write("comparacion_carrera", item["carrera"], "promedio", item["promedio"])

    # 15. Comparación semestre
    for item in data["comparacion_semestre"]["items"]:
        write("comparacion_semestre", item["semestre"], "promedio", item["promedio"])

    # 16. Comparación edad
    for item in data["comparacion_edad"]["items"]:
        write("comparacion_edad", item["grupo_edad"], "promedio", item["promedio"])

    return output.getvalue()


def build_looker_json(df: pd.DataFrame) -> list:
    dashboard = build_dashboard(df)
    d = dashboard.model_dump()
    rows = []

    def add(seccion, nombre, valor=None, cantidad=None, porcentaje=None):
        row = {"seccion": seccion, "nombre": nombre}
        if valor is not None:
            row["valor"] = valor
        if cantidad is not None:
            row["cantidad"] = cantidad
        if porcentaje is not None:
            row["porcentaje"] = porcentaje
        rows.append(row)

    add("kpi", "Conocimiento técnico", d["nivel_conocimientos_tecnicos"]["promedio"])
    add("kpi", "Dominio digital", d["nivel_dominio_digital"]["promedio"])
    add("kpi", "Formación digital", d["formacion_digital"]["porcentaje_con_formacion"])
    add("kpi", "Brecha técnica", d["brecha_tecnica_promedio"]["promedio"])
    add("kpi", "Brecha digital", d["brecha_digital_promedio"]["promedio"])
    add("kpi", "Uso frecuente", d["uso_herramientas_carrera"]["porcentaje_uso_frecuente"])

    for k, v in d["nivel_conocimientos_tecnicos"]["distribucion"].items():
        add("distribucion_tecnica", f"N{k}", v)
    for k, v in d["nivel_dominio_digital"]["distribucion"].items():
        add("distribucion_digital", f"N{k}", v)

    add("formacion", "Con formación", d["formacion_digital"]["con_formacion"])
    add("formacion", "Sin formación", d["formacion_digital"]["sin_formacion"])

    add("alerta", "Sin formación digital",
        cantidad=d["estudiantes_sin_formacion_digital"]["cantidad"],
        porcentaje=d["estudiantes_sin_formacion_digital"]["porcentaje"])
    add("alerta", "Bajo dominio tecnológico",
        cantidad=d["estudiantes_bajo_dominio_tecnologico"]["cantidad"],
        porcentaje=d["estudiantes_bajo_dominio_tecnologico"]["porcentaje"])

    add("preparacion_laboral", "Promedio", d["preparacion_laboral"]["promedio"])
    for k, v in d["preparacion_laboral"]["distribucion"].items():
        add("preparacion_laboral_distribucion", f"N{k}", v)

    for item in d["habilidades_mejorar"]["items"]:
        add("habilidades", item["habilidad"], item["conteo"])

    for item in d["herramientas_mas_usadas"]["items"]:
        add("herramientas", item["herramienta"], item["conteo"])

    for k, v in d["frecuencia_uso_digital"]["frecuencia"].items():
        add("frecuencia", k, v)

    for item in d["comparacion_carrera"]["items"]:
        add("comparacion_carrera", item["carrera"], item["promedio"])
    for item in d["comparacion_semestre"]["items"]:
        add("comparacion_semestre", str(item["semestre"]), item["promedio"])
    for item in d["comparacion_edad"]["items"]:
        add("comparacion_edad", item["grupo_edad"], item["promedio"])

    return rows
