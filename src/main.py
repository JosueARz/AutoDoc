from autodoc.parser import CodeParser

archivo_python = "tests/mocks/mixed_practices.py"
parser = CodeParser(archivo_python)
resultados = parser.extract_docstrings()

print("\n📄 Análisis del código:")
for resultado in resultados:
    print(f"\n🔹 Tipo: {resultado['tipo']}")
    print(f"   🏷 Nombre: {resultado['nombre']}")
    print(f"   📜 Documentado: {resultado['documentado']}")
    print(f"   ⚠️ Gravedad: {resultado['gravedad']}")
