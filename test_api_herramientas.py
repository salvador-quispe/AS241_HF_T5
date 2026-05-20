"""
Script para probar el endpoint de herramientas del API
"""

import sys
sys.path.append('.')

from app.services.digital_skills_service import get_herramientas_ofimaticas
import json

print("🔍 PROBANDO ENDPOINT DE HERRAMIENTAS")
print("=" * 60)

try:
    herramientas = get_herramientas_ofimaticas()
    
    print(f"\n✅ Conexión exitosa!")
    print(f"📊 Total herramientas: {len(herramientas)}\n")
    
    # Mostrar en formato JSON
    print("📋 RESPUESTA DEL API (JSON):")
    print("-" * 60)
    
    herramientas_dict = [h.dict() for h in herramientas]
    print(json.dumps(herramientas_dict, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()