"""
Este módulo contiene ejemplos de buenas y malas prácticas en documentación.
"""

# ✅ MUY BUENAS PRÁCTICAS (Documentación clara y detallada)
class Calculadora:
    """
    Clase para realizar operaciones matemáticas básicas.
    """

    def suma(self, a: float, b: float) -> float:
        """
        Suma dos números y devuelve el resultado.

        :param a: Primer número
        :param b: Segundo número
        :return: La suma de `a` y `b`
        """
        return a + b

    def resta(self, a: float, b: float) -> float:
        """
        Resta dos números y devuelve el resultado.

        :param a: Primer número
        :param b: Segundo número
        :return: La resta de `a` y `b`
        """
        return a - b

# 👍 BUENAS PRÁCTICAS (Documentación breve pero suficiente)
class Usuario:
    """Representa un usuario del sistema."""

    def __init__(self, nombre: str):
        """Inicializa un usuario con su nombre."""
        self.nombre = nombre

    def mostrar(self):
        """Muestra el nombre del usuario."""
        print(f"Usuario: {self.nombre}")

# ⚠️ MALAS PRÁCTICAS (Sin docstrings en métodos importantes)
class SinDocstring:
    """Clase sin documentación detallada."""

    def metodo(self):
        pass  # No hay docstring, no se sabe qué hace este método

    def otro_metodo(self, x):
        return x * 2  # No hay información sobre `x` ni qué devuelve la función

# ❌ MUY MALAS PRÁCTICAS (Nada de documentación, código poco entendible)
def f(x, y):
    return x**y  # No hay docstring, no se sabe qué hace

class X:
    def y(self, z):
        return z + 1  # No hay contexto, nombres poco descriptivos
