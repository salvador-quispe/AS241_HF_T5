"""
Digital Skills ETL Module
Data transformations and queries for digital skills BI dashboard
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging
import re
from datetime import datetime

from app.config.database import get_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DigitalSkillsETL:
    """
    ETL processor for digital skills data
    Contains all queries and transformations for BI analysis
    """
    
    def __init__(self):
        """Initialize ETL by loading data from database"""
        self.df = get_data()
        self.total_students = len(self.df)
        logger.info(f"Digital Skills ETL initialized with {self.total_students} students")
        
        # Process digital tools data
        self._process_digital_tools()
    
    def _process_digital_tools(self):
        """Process and categorize digital tools from survey responses"""
        # Extraer TODAS las herramientas únicas de los datos
        self.all_tools = set()
        
        if 'herramientas_digitales' in self.df.columns:
            for tools_str in self.df['herramientas_digitales'].dropna():
                # Dividir por comas y limpiar espacios
                tools = [t.strip() for t in str(tools_str).split(',')]
                self.all_tools.update(tools)
        
        # Map digital tools to categories
        self.tool_categories = {
            'Excel o Google Sheets': 'Ofimática',
            'Word o Google Docs': 'Ofimática', 
            'Editor de código (Visual Studio Code, IntelliJ, etc.)': 'Programación',
            'Bases de datos (MySQL, PostgreSQL, etc.)': 'Programación',
            'Git / GitHub': 'Programación',
            'Herramientas de IA (ChatGPT, Gemini, etc.)': 'IA/Productividad',
            'Google Apps Script': 'Programación',
            'Utilizo el visual studio code pero me falta aprender mas cosas': 'Programación'
        }
        
        # Agregar cualquier herramienta nueva encontrada en los datos
        for tool in self.all_tools:
            if tool not in self.tool_categories:
                # Categorizar automáticamente basado en palabras clave
                tool_lower = tool.lower()
                if any(word in tool_lower for word in ['excel', 'sheets', 'word', 'docs', 'powerpoint', 'prezi', 'teams', 'slack']):
                    self.tool_categories[tool] = 'Ofimática'
                elif any(word in tool_lower for word in ['código', 'code', 'python', 'java', 'javascript', 'git', 'github', 'database', 'sql', 'mysql', 'postgresql']):
                    self.tool_categories[tool] = 'Programación'
                elif any(word in tool_lower for word in ['ia', 'ai', 'chatgpt', 'gemini', 'copilot', 'claude']):
                    self.tool_categories[tool] = 'IA/Productividad'
                else:
                    self.tool_categories[tool] = 'Otras Herramientas'
        
        logger.info(f"Detected {len(self.all_tools)} unique digital tools")
    
    # ============================================
    # 1. KPI METRICS (Summary Cards)
    # ============================================
    
    def get_kpi_metrics(self) -> Dict[str, Any]:
        """
        Calculate main KPI metrics for digital skills dashboard
        
        Returns:
            Dict with KPI values matching dashboard design
        """
        # Dominio promedio (1-5 scale)
        if 'nivel_dominio_herramientas_digitales' in self.df.columns:
            dominio_promedio = round(self.df['nivel_dominio_herramientas_digitales'].mean(), 1)
        else:
            dominio_promedio = 4.2
        
        # Capacitación completada (porcentaje con formación)
        if 'formacion_herramientas_digitales' in self.df.columns:
            capacitados = len(self.df[self.df['formacion_herramientas_digitales'] == 'Si'])
            capacitacion_completada = round((capacitados / self.total_students) * 100, 0)
        else:
            capacitacion_completada = 87.0
        
        # Uso diario promedio (convertir frecuencia a horas)
        frecuencia_map = {
            'Siempre': 8.0,
            'Frecuentemente': 6.8, 
            'A veces': 4.0,
            'Raramente': 2.0,
            'Nunca': 0.0
        }
        
        if 'frecuencia_uso_herramientas_digitales' in self.df.columns:
            self.df['horas_uso'] = self.df['frecuencia_uso_herramientas_digitales'].map(frecuencia_map)
            uso_diario_promedio = round(self.df['horas_uso'].mean(), 1)
        else:
            uso_diario_promedio = 6.8
        
        # Alertas de nivel bajo (dominio <= 2)
        if 'nivel_dominio_herramientas_digitales' in self.df.columns:
            alertas_nivel_bajo = len(self.df[self.df['nivel_dominio_herramientas_digitales'] <= 2])
        else:
            alertas_nivel_bajo = 4
        
        return {
            'dominio_promedio': dominio_promedio,
            'capacitacion_completada': capacitacion_completada,
            'uso_diario_promedio': uso_diario_promedio,
            'alertas_nivel_bajo': alertas_nivel_bajo,
            'total_estudiantes': self.total_students
        }
    
    # ============================================
    # 2. HERRAMIENTAS OFIMÁTICAS
    # ============================================
    
    def get_herramientas_ofimaticas(self) -> List[Dict[str, Any]]:
        """
        Calculate usage and proficiency of office tools
        Automatically detects ALL tools from survey data
        
        Returns:
            List of office tools with usage statistics
        """
        herramientas_data = []
        
        if 'herramientas_digitales' in self.df.columns:
            # Procesar TODAS las herramientas encontradas en los datos
            for tool in sorted(self.all_tools):
                # Contar estudiantes que usan esta herramienta
                users = self.df[self.df['herramientas_digitales'].str.contains(re.escape(tool), na=False, case=False)]
                estudiantes_usan = len(users)
                
                if estudiantes_usan > 0:
                    # Calcular nivel promedio de dominio para usuarios de esta herramienta
                    if 'nivel_dominio_herramientas_digitales' in users.columns:
                        nivel_promedio = users['nivel_dominio_herramientas_digitales'].mean()
                    else:
                        nivel_promedio = 3.5
                    
                    porcentaje_dominio = (estudiantes_usan / self.total_students) * 100
                    
                    # Categorizar la herramienta
                    categoria = self.tool_categories.get(tool, 'Otras Herramientas')
                    
                    herramientas_data.append({
                        'herramienta': tool,
                        'categoria': categoria,
                        'porcentaje_dominio': round(porcentaje_dominio, 1),
                        'nivel_promedio': round(nivel_promedio, 1),
                        'estudiantes_usan': estudiantes_usan
                    })
            
            # Ordenar por porcentaje de dominio descendente
            herramientas_data.sort(key=lambda x: x['porcentaje_dominio'], reverse=True)
        else:
            # Datos de ejemplo basados en el dashboard
            herramientas_data = [
                {'herramienta': 'MICROSOFT EXCEL (AVANZADO)', 'categoria': 'Ofimática', 'porcentaje_dominio': 78, 'nivel_promedio': 3.9, 'estudiantes_usan': 53},
                {'herramienta': 'MICROSOFT WORD', 'categoria': 'Ofimática', 'porcentaje_dominio': 92, 'nivel_promedio': 4.6, 'estudiantes_usan': 63},
                {'herramienta': 'PRESENTACIONES (POWERPOINT/PREZI)', 'categoria': 'Ofimática', 'porcentaje_dominio': 85, 'nivel_promedio': 4.2, 'estudiantes_usan': 58},
                {'herramienta': 'HERRAMIENTAS COLABORATIVAS (TEAMS)', 'categoria': 'Ofimática', 'porcentaje_dominio': 64, 'nivel_promedio': 3.2, 'estudiantes_usan': 44}
            ]
        
        return herramientas_data
    
    # ============================================
    # 3. PLATAFORMAS Y LENGUAJES
    # ============================================
    
    def get_plataformas_lenguajes(self) -> List[Dict[str, Any]]:
        """
        Calculate programming platforms and languages proficiency
        Automatically detects ALL programming tools from survey data
        
        Returns:
            List of platforms/languages with proficiency data
        """
        plataformas_data = []
        
        if 'herramientas_digitales' in self.df.columns:
            # Filtrar solo herramientas de programación
            herramientas_programacion = [
                tool for tool in self.all_tools 
                if self.tool_categories.get(tool) == 'Programación'
            ]
            
            for tool in sorted(herramientas_programacion):
                # Buscar estudiantes que usan esta herramienta
                users = self.df[self.df['herramientas_digitales'].str.contains(re.escape(tool), na=False, case=False)]
                
                if len(users) > 0:
                    # Calcular dominio promedio
                    if 'nivel_dominio_herramientas_digitales' in users.columns:
                        dominio = int(users['nivel_dominio_herramientas_digitales'].mean())
                    else:
                        dominio = 3
                    
                    # Verificar si tienen formación
                    if 'formacion_herramientas_digitales' in users.columns:
                        capacitados = len(users[users['formacion_herramientas_digitales'] == 'Si'])
                        capacitacion = 'Si' if capacitados > len(users) // 2 else 'No'
                    else:
                        capacitacion = 'Si'
                    
                    # Convertir dominio numérico a texto
                    nivel_texto_map = {1: 'Básico', 2: 'Básico', 3: 'Intermedio', 4: 'Intermedio', 5: 'Avanzado'}
                    nivel_texto = nivel_texto_map.get(dominio, 'Básico')
                    
                    plataformas_data.append({
                        'categoria': tool,
                        'dominio': dominio,
                        'capacitacion': capacitacion,
                        'nivel_texto': nivel_texto,
                        'estudiantes': len(users)
                    })
        else:
            # Datos de ejemplo basados en el dashboard
            plataformas_data = [
                {'categoria': 'SQL / Bases de Datos', 'dominio': 3, 'capacitacion': 'Si', 'nivel_texto': 'Intermedio', 'estudiantes': 20},
                {'categoria': 'Python para Análisis', 'dominio': 2, 'capacitacion': 'Si', 'nivel_texto': 'Básico', 'estudiantes': 15},
                {'categoria': 'LMS (Moodle/Canvas)', 'dominio': 4, 'capacitacion': 'Si', 'nivel_texto': 'Intermedio', 'estudiantes': 25},
                {'categoria': 'Desarrollo Web (HTML/CSS)', 'dominio': 2, 'capacitacion': 'No', 'nivel_texto': 'Básico', 'estudiantes': 10}
            ]
        
        return plataformas_data
    
    # ============================================
    # 4. ESTUDIANTES INDIVIDUALES
    # ============================================
    
    def get_estudiantes_habilidades(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get individual student digital skills breakdown
        
        Args:
            limit: Number of students to return
            
        Returns:
            List of student digital skills data
        """
        estudiantes_data = []
        
        for idx, row in self.df.head(limit).iterrows():
            # Generar expediente basado en DNI
            dni = str(row.get('dni', f'VG-2024-{idx:03d}'))
            expediente = f"VG-2024-{dni[-3:]}"
            
            # Generar nombre ficticio
            nombres = ['ALVARADO, CARLOS', 'BENÍTEZ, MARÍA', 'CASTRO, JORGE', 'DÍAZ, ELENA', 
                      'FERNÁNDEZ, ANA', 'GARCÍA, LUIS', 'HERNÁNDEZ, SOFÍA', 'JIMÉNEZ, PEDRO']
            estudiante = nombres[idx % len(nombres)]
            
            # Calcular puntuaciones
            if 'nivel_dominio_herramientas_digitales' in row:
                ofimatica = float(row['nivel_dominio_herramientas_digitales'])
                programacion = ofimatica * 0.8  # Programación típicamente menor que ofimática
            else:
                ofimatica = np.random.uniform(2.0, 5.0)
                programacion = np.random.uniform(1.0, 4.5)
            
            # Frecuencia de uso en horas
            if 'frecuencia_uso_herramientas_digitales' in row:
                frecuencia_map = {'Siempre': 8.5, 'Frecuentemente': 6.0, 'A veces': 3.5, 'Raramente': 1.0}
                frecuencia_hrs = frecuencia_map.get(row['frecuencia_uso_herramientas_digitales'], 4.0)
            else:
                frecuencia_hrs = np.random.uniform(3.0, 12.0)
            
            # Determinar estado basado en puntuaciones
            promedio = (ofimatica + programacion) / 2
            if promedio >= 4.5:
                estado = 'EXCELENTE'
            elif promedio >= 3.5:
                estado = 'COMPETENTE'
            elif promedio >= 2.5:
                estado = 'REGULAR'
            else:
                estado = 'EN FORMACIÓN'
            
            estudiantes_data.append({
                'expediente': expediente,
                'estudiante': estudiante,
                'ofimatica': round(ofimatica, 1),
                'programacion': round(programacion, 1),
                'frecuencia_hrs': round(frecuencia_hrs, 1),
                'estado': estado
            })
        
        return estudiantes_data
    
    # ============================================
    # 5. ANÁLISIS E INSIGHTS
    # ============================================
    
    def generate_conclusions(self) -> str:
        """
        Generate business conclusions from digital skills analysis
        
        Returns:
            String with analysis conclusions
        """
        kpi = self.get_kpi_metrics()
        herramientas = self.get_herramientas_ofimaticas()
        
        # Encontrar herramienta con mayor dominio
        mejor_herramienta = max(herramientas, key=lambda x: x['porcentaje_dominio'])
        
        # Analizar nivel de capacitación
        if kpi['capacitacion_completada'] >= 85:
            capacitacion_status = "superior al promedio institucional"
        else:
            capacitacion_status = "requiere reforzamiento"
        
        # Identificar brecha crítica
        herramientas_bajas = [h for h in herramientas if h['porcentaje_dominio'] < 70]
        if herramientas_bajas:
            brecha_critica = f"se identifica una brecha crítica en el uso de {herramientas_bajas[0]['herramienta'].lower()}"
        else:
            brecha_critica = "no se identifican brechas críticas significativas"
        
        conclusion = f"El nivel de adopción de herramientas de ofimática es {capacitacion_status}, " \
                    f"sin embargo, {brecha_critica} para análisis de datos."
        
        return conclusion
    
    def generate_recommended_actions(self) -> List[str]:
        """
        Generate recommended actions based on analysis
        
        Returns:
            List of recommended actions
        """
        kpi = self.get_kpi_metrics()
        
        actions = []
        
        # Acción basada en capacitación
        if kpi['capacitacion_completada'] < 90:
            actions.append("Reforzar capacitación en Python.")
        
        # Acción basada en alertas
        if kpi['alertas_nivel_bajo'] > 0:
            actions.append("Implementar taller de SQL avanzado.")
        
        # Acción estándar
        actions.append("Certificación obligatoria en Teams.")
        
        return actions
    
    def get_proxima_evaluacion(self) -> str:
        """Get next evaluation date"""
        return "15 OCT 2026"
    
    # ============================================
    # 6. DASHBOARD COMPLETO
    # ============================================
    
    def get_complete_dashboard_data(self) -> Dict[str, Any]:
        """
        Get all dashboard data in one consolidated dictionary
        
        Returns:
            Complete dashboard data ready for API response
        """
        logger.info("Generating complete digital skills dashboard data...")
        
        dashboard_data = {
            'indicadores_kpi': self.get_kpi_metrics(),
            'herramientas_ofimaticas': self.get_herramientas_ofimaticas(),
            'plataformas_lenguajes': self.get_plataformas_lenguajes(),
            'estudiantes_habilidades': self.get_estudiantes_habilidades(),
            'conclusiones_modulo': self.generate_conclusions(),
            'acciones_recomendadas': self.generate_recommended_actions(),
            'proxima_evaluacion': self.get_proxima_evaluacion()
        }
        
        logger.info("Digital skills dashboard data generation complete")
        return dashboard_data
    
    # ============================================
    # 7. FUNCIONES DE EXPORTACIÓN
    # ============================================
    
    def export_to_csv(self, filepath: str) -> None:
        """Export cleaned data to CSV for backup"""
        self.df.to_csv(filepath, index=False, encoding='utf-8-sig')
        logger.info(f"Digital skills data exported to {filepath}")
    
    def get_summary_statistics(self) -> pd.DataFrame:
        """Get summary statistics for all numeric columns"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        return self.df[numeric_cols].describe()