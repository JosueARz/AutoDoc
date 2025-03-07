import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from autodoc.parser import CodeParser

def test_extract_docstrings():
    parser = CodeParser("tests/mocks/example.py")
    docstrings = parser.extract_docstrings()

    assert "MiClase" in docstrings
    assert docstrings["MiClase"] == "Esta es una clase de ejemplo."

    assert "mi_funcion" in docstrings
    assert docstrings["mi_funcion"] == "Esta es una función de prueba."
    
    assert "Módulo" in docstrings
    assert docstrings["Módulo"] == "Este es un módulo de prueba."
