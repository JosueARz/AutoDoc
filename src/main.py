from autodoc.parser import CodeParser

if __name__ == "__main__":
    archivo_python = "tests/mocks/mixed_practices.py"
    parser = CodeParser(archivo_python)

    # Extraer información del código
    resultados = parser.extract_docstrings()

    # Evaluar con OpenAI
    evaluaciones = parser.evaluate_with_openai(resultados)

    # Mostrar resultados
    print("\n📄 Evaluación de documentación con OpenAI:")
    for resultado in evaluaciones:
        print("\n───────────────────────────────────────")
        print(f"🔹 Tipo: {resultado['tipo']}")
        print(f"   🏷 Nombre: {resultado['nombre']}")
        print(f"   📜 Documentado: {resultado['docstring']}")
        print(f"   🎯 Puntuación: {resultado.get('puntuación', 'No evaluado')}")
        print(f"   🏆 Clasificación: {resultado.get('clasificación', 'No evaluado')}")
    print("\n───────────────────────────────────────")
