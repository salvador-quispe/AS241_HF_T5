"""
CLI — Dashboard Brechas + Empleabilidad

Uso:
  python cli.py                         Todo (brechas + empleabilidad + raw)
  python cli.py brechas                 Solo módulo brechas
  python cli.py empleabilidad           Solo módulo empleabilidad
  python cli.py list                    Listar todos los indicadores disponibles

  # Brechas específicos
  python cli.py brechas.conocimientos
  python cli.py brechas.dominio
  python cli.py brechas.frecuencia
  python cli.py brechas.formacion
  python cli.py brechas.herramientas
  python cli.py brechas.preparacion
  python cli.py brechas.habilidades
  python cli.py brechas.tecnica
  python cli.py brechas.digital
  python cli.py brechas.blandas
  python cli.py brechas.sin_formacion
  python cli.py brechas.bajo_dominio
  python cli.py brechas.uso_carrera
  python cli.py brechas.carrera
  python cli.py brechas.semestre
  python cli.py brechas.edad

  # Empleabilidad específicos
  python cli.py empleabilidad.preparacion
  python cli.py empleabilidad.institucional
  python cli.py empleabilidad.dificultad
  python cli.py empleabilidad.practicas
  python cli.py empleabilidad.interes
  python cli.py empleabilidad.comunicacion
  python cli.py empleabilidad.equipo
  python cli.py empleabilidad.problemas
  python cli.py empleabilidad.adaptabilidad
  python cli.py empleabilidad.organizacion
  python cli.py empleabilidad.centro
  python cli.py empleabilidad.carrera
  python cli.py empleabilidad.semestre
  python cli.py empleabilidad.valoradas
  python cli.py empleabilidad.debiles
  python cli.py empleabilidad.indicador
  python cli.py empleabilidad.listos
  python cli.py empleabilidad.insuficientes

  python cli.py raw                     Solo datos crudos + distribuciones

Ejemplos:
  python cli.py brechas.herramientas    "Herramientas digitales más utilizadas"
  python cli.py empleabilidad.indicador "Indicador general de empleabilidad"
"""

import sys
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)
pd.set_option("display.max_colwidth", 50)

from app.config.database import get_data
from app.services.brechas import build_dashboard as build_brechas
from app.services.empleabilidad import build_dashboard as build_empleabilidad

SEP = "-" * 72
HEADER = "\n" + "=" * 72
FOOTER = "=" * 72 + "\n"


def p(obj, indent=0):
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
                        parts = [f"{ik.replace('_',' ').title()}: {iv}" for ik, iv in item.items()]
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
    print(HEADER)
    print(f"  {title}")
    print(FOOTER)
    p(data)
    print()


def get_brechas_df():
    df = get_data(force=True)
    b = build_brechas(df)
    return b.model_dump()


def get_empleabilidad_df():
    df = get_data(force=True)
    e = build_empleabilidad(df)
    return e.model_dump()


def show_brechas(all_data: dict):
    show("MÓDULO BRECHAS — Dashboard completo", all_data)


def show_empleabilidad(all_data: dict):
    show("MÓDULO EMPLEABILIDAD — Dashboard completo", all_data)


def show_brechas_item(all_data: dict, key: str, title: str):
    if key not in all_data:
        print(f"\n  ✗ Indicador '{key}' no encontrado en Brechas.\n")
        sys.exit(1)
    show(f"BRECHAS — {title}", all_data[key])


def show_empleabilidad_item(all_data: dict, key: str, title: str):
    if key not in all_data:
        print(f"\n  ✗ Indicador '{key}' no encontrado en Empleabilidad.\n")
        sys.exit(1)
    show(f"EMPLEABILIDAD — {title}", all_data[key])


def show_raw():
    df = get_data(force=True)
    show("DATOS CRUDOS (primeras 10 filas)", df.head(10).to_string(index=False))
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
    print(f"  TOTAL: {len(df)} encuestados, {len(df.columns)} columnas")
    print()


def show_list():
    brechas_keys = {
        "conocimientos": "Nivel de conocimientos técnicos",
        "dominio": "Nivel de dominio de herramientas digitales",
        "frecuencia": "Frecuencia de uso de herramientas digitales",
        "formacion": "Formación en herramientas digitales",
        "herramientas": "Herramientas digitales más utilizadas",
        "preparacion": "Nivel de preparación para aplicar conocimientos",
        "habilidades": "Habilidades que necesitan mejorar",
        "tecnica": "Brecha técnica promedio",
        "digital": "Brecha digital promedio",
        "blandas": "Brecha de habilidades blandas",
        "sin_formacion": "Estudiantes sin formación digital",
        "bajo_dominio": "Estudiantes con bajo dominio tecnológico",
        "uso_carrera": "% estudiantes que usan herramientas de su carrera",
        "carrera": "Comparación por carrera profesional",
        "semestre": "Comparación por semestre académico",
        "edad": "Comparación por edad",
    }
    empleabilidad_keys = {
        "preparacion": "Nivel de preparación para ingresar al mercado laboral",
        "institucional": "Nivel de preparación institucional percibida",
        "dificultad": "Dificultad percibida para conseguir trabajo",
        "practicas": "% con prácticas preprofesionales",
        "interes": "Interés en recibir más formación profesional",
        "comunicacion": "Importancia de la comunicación efectiva",
        "equipo": "Importancia del trabajo en equipo",
        "problemas": "Importancia de resolución de problemas",
        "adaptabilidad": "Importancia de la adaptabilidad",
        "organizacion": "Importancia de organización y manejo del tiempo",
        "centro": "Importancia del centro de evaluación",
        "carrera": "Comparación de empleabilidad por carrera",
        "semestre": "Comparación por semestre",
        "valoradas": "Ranking de habilidades más valoradas",
        "debiles": "Ranking de habilidades más débiles",
        "indicador": "Indicador general de empleabilidad",
        "listos": "Estudiantes listos para el mercado laboral",
        "insuficientes": "Estudiantes que consideran insuficiente la preparación",
    }

    print(HEADER)
    print("  INDICADORES DISPONIBLES")
    print(FOOTER)
    print("  python cli.py <módulo>.<indicador>\n")
    print("  BRECHAS:")
    for k, v in brechas_keys.items():
        print(f"    brechas.{k:20s}  -> {v}")
    print()
    print("  EMPLEABILIDAD:")
    for k, v in empleabilidad_keys.items():
        print(f"    empleabilidad.{k:20s}  -> {v}")
    print("    brechas              -> Dashboard completo de brechas")
    print("    empleabilidad        -> Dashboard completo de empleabilidad")
    print("    raw                  -> Datos crudos + distribuciones")
    print("    list                 -> Esta lista")
    print()


def main():
    args = sys.argv[1:]

    if not args or args[0] == "all":
        df = get_data(force=True)
        b = get_brechas_df()
        e = get_empleabilidad_df()
        show_brechas(b)
        show_empleabilidad(e)
        show_raw()
        return

    cmd = args[0]

    if cmd == "list":
        show_list()
        return

    if cmd == "raw":
        show_raw()
        return

    if cmd == "brechas":
        show_brechas(get_brechas_df())
        return

    if cmd == "empleabilidad":
        show_empleabilidad(get_empleabilidad_df())
        return

    if cmd.startswith("brechas."):
        key = cmd.split(".", 1)[1]
        key_map = {
            "conocimientos": "nivel_conocimientos_tecnicos",
            "dominio": "nivel_dominio_digital",
            "frecuencia": "frecuencia_uso_digital",
            "formacion": "formacion_digital",
            "herramientas": "herramientas_mas_usadas",
            "preparacion": "preparacion_laboral",
            "habilidades": "habilidades_mejorar",
            "tecnica": "brecha_tecnica_promedio",
            "digital": "brecha_digital_promedio",
            "blandas": "brecha_habilidades_blandas",
            "sin_formacion": "estudiantes_sin_formacion_digital",
            "bajo_dominio": "estudiantes_bajo_dominio_tecnologico",
            "uso_carrera": "uso_herramientas_carrera",
            "carrera": "comparacion_carrera",
            "semestre": "comparacion_semestre",
            "edad": "comparacion_edad",
        }
        if key not in key_map:
            print(f"\n  ✗ Indicador '{key}' no reconocido. Usa 'python cli.py list'\n")
            sys.exit(1)
        title_map = {
            "conocimientos": "Nivel de conocimientos técnicos",
            "dominio": "Nivel de dominio de herramientas digitales",
            "frecuencia": "Frecuencia de uso de herramientas digitales",
            "formacion": "Formación en herramientas digitales",
            "herramientas": "Herramientas digitales más utilizadas",
            "preparacion": "Nivel de preparación para aplicar conocimientos",
            "habilidades": "Habilidades que necesitan mejorar",
            "tecnica": "Brecha técnica promedio",
            "digital": "Brecha digital promedio",
            "blandas": "Brecha de habilidades blandas",
            "sin_formacion": "Estudiantes sin formación digital",
            "bajo_dominio": "Estudiantes con bajo dominio tecnológico",
            "uso_carrera": "% estudiantes que usan herramientas de su carrera",
            "carrera": "Comparación por carrera profesional",
            "semestre": "Comparación por semestre académico",
            "edad": "Comparación por edad",
        }
        data = get_brechas_df()
        show_brechas_item(data, key_map[key], title_map[key])
        return

    if cmd.startswith("empleabilidad."):
        key = cmd.split(".", 1)[1]
        key_map = {
            "preparacion": "nivel_preparacion_mercado",
            "institucional": "preparacion_institucional",
            "dificultad": "dificultad_conseguir_trabajo",
            "practicas": "practicas_preprofesionales",
            "interes": "interes_formacion",
            "comunicacion": "importancia_comunicacion",
            "equipo": "importancia_trabajo_equipo",
            "problemas": "importancia_resolucion_problemas",
            "adaptabilidad": "importancia_adaptabilidad",
            "organizacion": "importancia_organizacion_tiempo",
            "centro": "importancia_centro_evaluacion",
            "carrera": "comparacion_carrera",
            "semestre": "comparacion_semestre",
            "valoradas": "ranking_habilidades_valoradas",
            "debiles": "ranking_habilidades_debiles",
            "indicador": "indicador_general_empleabilidad",
            "listos": "estudiantes_listos_mercado",
            "insuficientes": "estudiantes_insuficiente_preparacion",
        }
        if key not in key_map:
            print(f"\n  ✗ Indicador '{key}' no reconocido. Usa 'python cli.py list'\n")
            sys.exit(1)
        title_map = {
            "preparacion": "Nivel de preparación para ingresar al mercado laboral",
            "institucional": "Nivel de preparación institucional percibida",
            "dificultad": "Dificultad percibida para conseguir trabajo",
            "practicas": "% con prácticas preprofesionales",
            "interes": "Interés en recibir más formación profesional",
            "comunicacion": "Importancia de la comunicación efectiva",
            "equipo": "Importancia del trabajo en equipo",
            "problemas": "Importancia de resolución de problemas",
            "adaptabilidad": "Importancia de la adaptabilidad",
            "organizacion": "Importancia de organización y manejo del tiempo",
            "centro": "Importancia del centro de evaluación",
            "carrera": "Comparación de empleabilidad por carrera",
            "semestre": "Comparación por semestre",
            "valoradas": "Ranking de habilidades más valoradas",
            "debiles": "Ranking de habilidades más débiles",
            "indicador": "Indicador general de empleabilidad",
            "listos": "Estudiantes listos para el mercado laboral",
            "insuficientes": "Estudiantes que consideran insuficiente la preparación",
        }
        data = get_empleabilidad_df()
        show_empleabilidad_item(data, key_map[key], title_map[key])
        return

    print(f"\n  ✗ Comando '{cmd}' no reconocido. Usa 'python cli.py list'\n")
    sys.exit(1)


if __name__ == "__main__":
    main()
