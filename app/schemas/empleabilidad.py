from pydantic import BaseModel


class NivelPreparacionMercado(BaseModel):
    promedio: float
    distribucion: dict

class PreparacionInstitucional(BaseModel):
    promedio: float
    distribucion: dict

class DificultadConseguirTrabajo(BaseModel):
    items: list[dict]

class PracticasPreprofesionales(BaseModel):
    con_practicas: int
    sin_practicas: int
    porcentaje_con_practicas: float

class InteresFormacion(BaseModel):
    si: int
    no: int
    porcentaje_interes: float

class ImportanciaIndicador(BaseModel):
    promedio: float
    distribucion: dict

class ComparacionEmpleabilidadCarrera(BaseModel):
    items: list[dict]

class ComparacionSemestre(BaseModel):
    items: list[dict]

class RankingHabilidadesValoradas(BaseModel):
    items: list[dict]

class RankingHabilidadesDebiles(BaseModel):
    items: list[dict]

class IndicadorGeneralEmpleabilidad(BaseModel):
    promedio_general: float
    nivel: str

class EstudiantesListosMercado(BaseModel):
    cantidad: int
    porcentaje: float

class EstudiantesInsuficientePreparacion(BaseModel):
    cantidad: int
    porcentaje: float

class DashboardEmpleabilidad(BaseModel):
    nivel_preparacion_mercado: NivelPreparacionMercado
    preparacion_institucional: PreparacionInstitucional
    dificultad_conseguir_trabajo: DificultadConseguirTrabajo
    practicas_preprofesionales: PracticasPreprofesionales
    interes_formacion: InteresFormacion
    importancia_comunicacion: ImportanciaIndicador
    importancia_trabajo_equipo: ImportanciaIndicador
    importancia_resolucion_problemas: ImportanciaIndicador
    importancia_adaptabilidad: ImportanciaIndicador
    importancia_organizacion_tiempo: ImportanciaIndicador
    importancia_centro_evaluacion: ImportanciaIndicador
    comparacion_carrera: ComparacionEmpleabilidadCarrera
    comparacion_semestre: ComparacionSemestre
    ranking_habilidades_valoradas: RankingHabilidadesValoradas
    ranking_habilidades_debiles: RankingHabilidadesDebiles
    indicador_general_empleabilidad: IndicadorGeneralEmpleabilidad
    estudiantes_listos_mercado: EstudiantesListosMercado
    estudiantes_insuficiente_preparacion: EstudiantesInsuficientePreparacion
