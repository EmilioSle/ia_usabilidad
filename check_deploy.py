#!/usr/bin/env python3
"""
Script de verificación pre-despliegue para Railway
Verifica que todos los archivos y configuraciones necesarios estén presentes.
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath: str, description: str) -> bool:
    """Verifica si un archivo existe"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} NO ENCONTRADO: {filepath}")
        return False

def check_env_example() -> bool:
    """Verifica que exista .env.example"""
    return check_file_exists(".env.example", "Plantilla de variables de entorno")

def check_env_file() -> bool:
    """Verifica que exista .env (advertencia, no error)"""
    if os.path.exists(".env"):
        print("✅ Archivo .env encontrado (recuerda configurar las variables en Railway)")
        
        # Verificar que contenga GROQ_API_KEY
        with open(".env", "r") as f:
            content = f.read()
            if "GROQ_API_KEY" in content:
                print("   ℹ️  GROQ_API_KEY encontrada en .env")
            else:
                print("   ⚠️  GROQ_API_KEY no encontrada en .env")
        return True
    else:
        print("⚠️  Archivo .env no encontrado (crear desde .env.example)")
        return False

def check_requirements() -> bool:
    """Verifica requirements.txt"""
    if not check_file_exists("requirements.txt", "Archivo de dependencias"):
        return False
    
    # Verificar que contenga las dependencias principales
    required_packages = ["fastapi", "uvicorn", "groq", "agno"]
    with open("requirements.txt", "r") as f:
        content = f.read().lower()
        missing = [pkg for pkg in required_packages if pkg not in content]
        
        if missing:
            print(f"   ⚠️  Paquetes faltantes: {', '.join(missing)}")
            return False
        else:
            print("   ✅ Todas las dependencias principales presentes")
            return True

def check_procfile() -> bool:
    """Verifica Procfile"""
    if not check_file_exists("Procfile", "Archivo de inicio de Railway"):
        return False
    
    with open("Procfile", "r") as f:
        content = f.read()
        if "uvicorn main:app" in content:
            print("   ✅ Comando de inicio correcto")
            return True
        else:
            print("   ⚠️  Comando de inicio podría ser incorrecto")
            return False

def check_railway_config() -> bool:
    """Verifica railway.json"""
    return check_file_exists("railway.json", "Configuración de Railway")

def check_main_file() -> bool:
    """Verifica que main.py exista"""
    return check_file_exists("main.py", "Archivo principal de la aplicación")

def check_gitignore() -> bool:
    """Verifica .gitignore"""
    if not check_file_exists(".gitignore", "Archivo .gitignore"):
        return False
    
    with open(".gitignore", "r") as f:
        content = f.read()
        if ".env" in content:
            print("   ✅ .env está en .gitignore (seguro)")
            return True
        else:
            print("   ⚠️  .env NO está en .gitignore (¡PELIGRO!)")
            return False

def main():
    print("\n" + "="*60)
    print("🔍 VERIFICACIÓN PRE-DESPLIEGUE RAILWAY")
    print("="*60 + "\n")
    
    checks = [
        ("Archivo principal", check_main_file),
        ("Requirements.txt", check_requirements),
        ("Procfile", check_procfile),
        ("Railway.json", check_railway_config),
        (".env.example", check_env_example),
        (".gitignore", check_gitignore),
        ("Archivo .env", check_env_file),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error al verificar {name}: {str(e)}")
            results.append((name, False))
        print()
    
    print("="*60)
    print("📊 RESUMEN")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\n✅ Verificaciones exitosas: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ¡TODO LISTO PARA DESPLEGAR EN RAILWAY!")
        print("\n📝 Próximos pasos:")
        print("1. git add .")
        print("2. git commit -m 'Preparar para Railway'")
        print("3. git push origin main")
        print("4. Ir a railway.app y crear proyecto desde GitHub")
        print("5. Configurar GROQ_API_KEY en las variables de entorno")
        return 0
    else:
        print("\n⚠️  Hay problemas que resolver antes de desplegar")
        print("   Revisa los errores arriba y corrígelos")
        return 1

if __name__ == "__main__":
    sys.exit(main())
