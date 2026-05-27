import json
import re
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. Carga de Datos de Google Sheets
archivo_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSBNPpHFjJU7QmGpDNwIP7TfkLE8B0hgSlISuUUjKtVrbTXQhgLRFo72YypW4yf6g7s2v3K0lJgGUQK/pub?gid=1157215314&single=true&output=csv"
df = pd.read_csv(archivo_csv)
df.columns = df.columns.str.strip()

columna = df.columns[27] if "¿Qué habilidades consideras que necesitas mejorar?" not in df.columns else "¿Qué habilidades consideras que necesitas mejorar?"

# 2. Configuración de Patrones (Orden de Prioridad Estricto)
PATRONES = {
    "Lógica y Algoritmia (Seudocódigo/Flujograma)": r"logica|lógica|seudocó|pseudocó|flujograma|algorit",
    "Bases de Datos y Análisis (SQL/Sheets)": r"base de datos|bases de datos|sql|mysql|sheets|excel|herramientas avanzadas",
    "Refuerzo General y Práctica Constante": r"seguir practicando|todo de la carrera|practica constante|practca constante|carrera",
    "Desarrollo Frontend (HTML/CSS)": r"html|css|sitios web|frontend|oaginas|paginas",
    "Arquitectura, Backend y DevOps (Docker)": r"arquitectura|backend|docker|kubernetes|distribuid|proyectos backend",
    "Infraestructura, Redes y AWS": r"aws|visual estudio|redes|ciberseguridad",
    "Programación y Código General": r"programac|cód|cod|lenguaje|memoriz|versiones|implementar|tecnic|digital|programas"
}

# 3. Clasificación Excluyente Optimizada
def clasificar(texto):
    if pd.isna(texto): return None
    texto_limpio = " ".join(str(texto).lower().split())
    for cat, patron in PATRONES.items():
        if re.search(patron, texto_limpio): return cat
    return None

df['Categoria_Asignada'] = df[columna].apply(clasificar)
df_mapeados = df[df['Categoria_Asignada'].notna()]

# 4. Cálculo de Métricas y JSON
total_encuestados = len(df)
total_mapeados = len(df_mapeados)
pct_global = round((total_mapeados / total_encuestados) * 100, 1) if total_encuestados > 0 else 0

conteos = df_mapeados['Categoria_Asignada'].value_counts()
lista_resultados = [
    {
        "categoria": cat,
        "votos": int(conteos.get(cat, 0)),
        "porcentaje_del_subtotal": round((int(conteos.get(cat, 0)) / total_mapeados) * 100, 1) if total_mapeados > 0 else 0
    }
    for cat in PATRONES.keys()
]
lista_resultados = sorted(lista_resultados, key=lambda x: x['votos'], reverse=True)

json_final = {
    "resumen_global": {"total_encuestados": total_encuestados, "total_mapeados": total_mapeados, "porcentaje_impacto_global": pct_global},
    "subcategorias_tecnicas": lista_resultados
}

with open("datos_tecnicos_react.json", "w", encoding="utf-8") as f:
    json.dump(json_final, f, ensure_ascii=False, indent=4)

# =================================================================
# ENTRADA IMPRESA EN TERMINAL (Reporte en Tiempo Real)
# =================================================================
print("\n" + "="*66)
print(" ¡REPORTE ETL DE HABILIDADES TÉCNICAS EN EN VIVO!")
print("="*66)
print(f"Total Alumnos en la Base de Datos : {total_encuestados}")
print(f"Total Alumnos Mapeados (Válidos) : {total_mapeados} ({pct_global}%)")
print("-"*66)
print(f"{'CATEGORÍA':<45} | {'ALUMNOS':<8} | {'PORCENTAJE'}")
print("-"*66)
for res in lista_resultados:
    print(f"{res['categoria']:<45} | {res['votos']:<8} | {res['porcentaje_del_subtotal']}%")
print("="*66)
print(" Archivo 'datos_tecnicos_react.json' actualizado para React.\n")

# 5. Visualización Dinámica (Gráfico de Dona)
df_pie = pd.DataFrame(lista_resultados)
colores = ['#0f172a', '#1d4ed8', '#38bdf8', '#10b981', '#f59e0b', '#f97316', '#cbd5e1']

fig, ax = plt.subplots(figsize=(12, 7), facecolor="#fafafa")
wedges, _ = ax.pie(df_pie["votos"], colors=colores[:len(df_pie)], startangle=90, wedgeprops=dict(width=0.35, edgecolor='#ffffff', linewidth=3))

ax.text(0, 0, f"{total_mapeados}\nAlumnos\nMapeados\n({pct_global}%)", ha='center', va='center', fontsize=13, weight='black', color='#1e293b')

etiquetas = [f"{r['porcentaje_del_subtotal']}%  {r['categoria']}  ({r['votos']} Alum.)" for _, r in df_pie.iterrows()]
ax.legend(wedges, etiquetas, title="DESGLOSE OPERACIONAL AUTOMÁTICO (MUTUALLY EXCLUSIVE)", title_fontproperties={'weight': 'bold', 'size': 11}, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), frameon=True, facecolor="#ffffff", edgecolor="#e2e8f0", labelspacing=1.1, borderpad=1.2)

plt.title("MATRIZ OPERACIONAL DE REQUERIMIENTOS - ENGINE V3.1", fontsize=12, loc="left", pad=20, color="#0f172a", weight="bold")
plt.tight_layout()
plt.show(block=True)