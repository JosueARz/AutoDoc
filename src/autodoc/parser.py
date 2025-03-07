import ast
from typing import List, Dict

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
        
        for node in self.tree.body:  # Se recorre directamente para mantener el orden
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
                results.append(self._get_doc_info(node))

                # Si es una clase, evaluar sus métodos en orden
                if isinstance(node, ast.ClassDef):
                    for sub_node in node.body:
                        if isinstance(sub_node, ast.FunctionDef):  # Métodos dentro de la clase
                            results.append(self._get_doc_info(sub_node, clase_padre=node.name))

        return results

    def _get_doc_info(self, node, clase_padre=None) -> Dict[str, str]:
        """
        Obtiene la información del docstring de un nodo (módulo, clase o función).

        :param node: Nodo del AST (módulo, clase o función).
        :param clase_padre: Nombre de la clase padre si el nodo es un método.
        :return: Diccionario con la información del elemento.
        """
        docstring = ast.get_docstring(node)
        tipo = "Módulo" if isinstance(node, ast.Module) else "Clase" if isinstance(node, ast.ClassDef) else "Método" if clase_padre else "Función"

        info = {
            "tipo": tipo,
            "nombre": f"{clase_padre}.{node.name}" if clase_padre else node.name,
            "docstring": docstring,
            "documentado": "✅ Sí" if docstring else "❌ No",
            "gravedad": self._calcular_gravedad(tipo, docstring),
        }
        return info

    def _calcular_gravedad(self, tipo: str, docstring: str) -> str:
        """Determina el nivel de gravedad si la documentación falta."""
        if docstring:
            return "🟢 BAJA"
        return "🔴 ALTA" if tipo == "Módulo" else "🟠 MEDIA" if tipo == "Clase" else "🟡 BAJA"
