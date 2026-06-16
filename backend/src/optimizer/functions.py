"""Definição da função objetivo e de seu gradiente"""

from typing import Any

import numpy as np
import numpy.typing as npt
import sympy as sp


def f_x() -> tuple[sp.Symbol, sp.Symbol, Any, Any]:
    """Prepara a função objetivo para ser utilizada posteriormente tanto no formato sympy quando numpy.

    Returns:
        As variáveis simbólicas de x1 e x2. A assinatura da função f(x) no formato sympy ou numpy.
    """
    x1_symbol = sp.Symbol("x1")
    x2_symbol = sp.Symbol("x2")
    term1 = ((x1_symbol - (5 * 5.7 / 5)) ** 2) / 4
    term2 = ((x2_symbol - (5 * 5.7 / 5)) ** 2) / 9
    sp_equation = term1 + term2 + 150
    np_equation = sp.lambdify((x1_symbol, x2_symbol), sp_equation, "numpy")
    return x1_symbol, x2_symbol, sp_equation, np_equation


def gradient(points: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    """Calcula o gradiente da função f_x() considerando os pontos dados.

    Args:
        points: uma array com os valores de x1 e X2.

    Returns:
        Uma array com os respectivos valores das derivadas parciais de f(x) em relação a x1 e x2.
    """
    x1_symbol, x2_symbol, sp_equation, _ = f_x()
    x1, x2 = points.flatten()
    diff_y_x1 = sp.diff(sp_equation, x1_symbol)
    diff_y_x2 = sp.diff(sp_equation, x2_symbol)
    y_x1 = sp.lambdify((x1_symbol, x2_symbol), diff_y_x1, "numpy")
    y_x2 = sp.lambdify((x1_symbol, x2_symbol), diff_y_x2, "numpy")
    g = [y_x1(x1, x2), y_x2(x1, x2)]
    return np.asarray(g, dtype=np.float64).reshape(1, 2)
