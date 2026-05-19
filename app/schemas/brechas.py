from pydantic import BaseModel
from typing import Optional


class NivelConocimientosTecnicos(BaseModel):
    promedio: float
    distribucion: dict

class NivelDominioDigital(BaseModel):
    promedio: float
    distribucion: dict

class FrecuenciaUsoDigital(BaseModel):
    frecuencia: dict

class FormacionDigital(BaseModel):
    con_formacion: int
    sin_formacion: int
    porcentaje_con_formacion: float

class HerramientasMasUsadas(BaseModel):
    items: list[dict]

class PreparacionLaboral(BaseModel):
    promedio: float
    distribucion: dict

class HabilidadesMejorar(BaseModel):
    items: list[dict]

class BrechaTecnicaPromedio(BaseModel):
    promedio: float
    maximo: int
    minimo: int

class BrechaDigitalPromedio(BaseModel):
    promedio: float
    maximo: int
    minimo: int

class BrechaHabilidadesBlandas(BaseModel):
    promedio_comunicacion: float
    promedio_trabajo_equipo: float
    promedio_resolucion_problemas: float
    promedio_adaptabilidad: float
    promedio_organizacion: float

class EstudiantesSinFormacionDigital(BaseModel):
    cantidad: int
    porcentaje: float

class EstudiantesBajoDominioTecnologico(BaseModel):
    cantidad: int
    porcentaje: float

class UsoHerramientasCarrera(BaseModel):
    porcentaje_uso_frecuente: float
    distribucion: dict

class ComparacionCarrera(BaseModel):
    items: list[dict]

class ComparacionSemestre(BaseModel):
    items: list[dict]

class ComparacionEdad(BaseModel):
    items: list[dict]

class DashboardBrechas(BaseModel):
    nivel_conocimientos_tecnicos: NivelConocimientosTecnicos
    nivel_dominio_digital: NivelDominioDigital
    frecuencia_uso_digital: FrecuenciaUsoDigital
    formacion_digital: FormacionDigital
    herramientas_mas_usadas: HerramientasMasUsadas
    preparacion_laboral: PreparacionLaboral
    habilidades_mejorar: HabilidadesMejorar
    brecha_tecnica_promedio: BrechaTecnicaPromedio
    brecha_digital_promedio: BrechaDigitalPromedio
    brecha_habilidades_blandas: BrechaHabilidadesBlandas
    estudiantes_sin_formacion_digital: EstudiantesSinFormacionDigital
    estudiantes_bajo_dominio_tecnologico: EstudiantesBajoDominioTecnologico
    uso_herramientas_carrera: UsoHerramientasCarrera
    comparacion_carrera: ComparacionCarrera
    comparacion_semestre: ComparacionSemestre
    comparacion_edad: ComparacionEdad
