from autodoc.parser import CodeParser

if __name__ == "__main__":
    archivo_python = "tests/mocks/mixed_practices.py"
    parser = CodeParser(archivo_python)

    # Extraer información del código
    resultados = parser.extract_docstrings()

    # Evaluar con OpenAI
    evaluaciones = parser.evaluate_with_openai(resultados)

    # Generar reporte en Markdown
    parser.generate_markdown_report(evaluaciones, "docs/evaluacion.md")
