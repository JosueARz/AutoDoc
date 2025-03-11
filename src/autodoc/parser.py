import ast
import openai
import os
import re
from typing import List, Dict
from dotenv import load_dotenv

# Cargar variables de entorno desde .env (si existe)
load_dotenv()

class CodeParser:
    """
    Clase para analizar código Python y extraer información detallada sobre docstrings.
    """

    def __init__(self, file_path: str):
        """
        Inicializa el analizador de código.

        :param file_path: Ruta del archivo Python a analizar.
        """
        self.file_path = file_path
        self.tree = self._parse_file()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        if not self.openai_api_key:
            raise ValueError("❌ ERROR: La clave de API de OpenAI no está configurada.")

        openai.api_key = self.openai_api_key

    def _parse_file(self):
        """Lee y convierte el código fuente en un árbol AST manteniendo el orden de los nodos."""
        with open(self.file_path, "r", encoding="utf-8") as file:
            return ast.parse(file.read())

    def extract_docstrings(self) -> List[Dict[str, str]]:
        """
        Extrae los docstrings y clasifica los elementos en módulos, clases y funciones,
        manteniendo el orden en que aparecen en el código.

        :return: Lista de diccionarios con detalles de cada elemento analizado.
        """
        results = []

        for node in self.tree.body:  # Mantener el orden original
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
                results.append(self._get_doc_info(node))

                if isinstance(node, ast.ClassDef):  # Si es clase, analizar métodos
                    for sub_node in node.body:
                        if isinstance(sub_node, ast.FunctionDef):
                            results.append(self._get_doc_info(sub_node, clase_padre=node.name))

        return results

    def _get_doc_info(self, node, clase_padre=None) -> Dict[str, str]:
        """Obtiene la información del docstring de un nodo (módulo, clase o función)."""
        docstring = ast.get_docstring(node)
        tipo = "Módulo" if isinstance(node, ast.Module) else "Clase" if isinstance(node, ast.ClassDef) else "Método" if clase_padre else "Función"

        return {
            "tipo": tipo,
            "nombre": f"{clase_padre}.{node.name}" if clase_padre else node.name,
            "docstring": docstring if docstring else "No documentado",
        }

    def evaluate_with_openai(self, elements: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Evalúa la calidad de la documentación con OpenAI.

        :param elements: Lista de elementos extraídos del código.
        :return: Lista con las evaluaciones agregadas.
        """
        prompt = (
            "Evalúa la calidad de la documentación en el siguiente código y califica cada elemento del 1 al 10.\n"
            "Clasificación: 'Muy bien documentado', 'Documentación aceptable', 'Falta documentación', 'Mal documentado'.\n"
            "Si está mal documentado, sugiere mejoras.\n"
            "Devuelve la respuesta en este formato: 'Nombre: [nombre] | Puntuación: [1-10] | Clasificación: [texto]'.\n\n"
        )

        for elem in elements:
            prompt += f"- {elem['tipo']} `{elem['nombre']}`:\n  Docstring: {elem['docstring']}\n\n"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )

            evaluation_text = response["choices"][0]["message"]["content"]
            
            # Extraer evaluaciones usando regex
            evaluations = {}
            pattern = r"Nombre: (.*?) \| Puntuación: (\d+) \| Clasificación: (.*?)$"
            matches = re.findall(pattern, evaluation_text, re.MULTILINE)

            for match in matches:
                nombre, puntuacion, clasificacion = match
                evaluations[nombre.strip()] = {
                    "puntuación": puntuacion.strip(),
                    "clasificación": clasificacion.strip()
                }

            # Agregar evaluación a los elementos originales
            for elem in elements:
                nombre = elem["nombre"]
                if nombre in evaluations:
                    elem["puntuación"] = evaluations[nombre]["puntuación"]
                    elem["clasificación"] = evaluations[nombre]["clasificación"]
                else:
                    elem["puntuación"] = "No evaluado"
                    elem["clasificación"] = "No evaluado"

        except openai.error.OpenAIError as e:
            print(f"❌ ERROR de OpenAI: {str(e)}")
            for elem in elements:
                elem["puntuación"] = "Error"
                elem["clasificación"] = "No se pudo evaluar"

        return elements
