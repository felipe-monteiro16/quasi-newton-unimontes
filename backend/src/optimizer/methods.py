from collections.abc import Iterable
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import Any

import numpy as np
import numpy.typing as npt

from src.optimizer.functions import f_x, gradient

@dataclass
class OptimizationResult:
    numero_iteracoes: int
    f_otimo: float
    X_otimo: list[float] = field(default_factory=list)
    X_iteracoes: list[npt.NDArray[np.float64]] = field(default_factory=list)
    f_iteracoes: list[float] = field(default_factory=list)


def quasi_newton(
    initial_points: Iterable[float], funcao_string: str, tol: float = 1e-6, max_iter: int = 10
) -> dict[str, Any]:
    """Busca o mínimo de uma dada função a partir do algoritmo BFGS Quasi-Newton.

    Args:
        initial_points: pontos iniciais utilizados no início da otimização.
        tol: valor máximo que a norma do gradiente pode ter para que a busca continue sendo executada. Defaults to 1e-6.
        max_iter: número de iterações máxima que a busca deve executar. Defaults to 10.

    Returns:
        o valor ótimo da função objetivo, os pontos x1 e x2 correspondentes, os valores, em suas respectivas listas, dos pontos e da função objetivo em cada ponto.
    """
    _, _, _, equation = f_x(funcao_string)
    xk = np.asarray(initial_points, dtype=np.float64)
    n = xk.size
    hinv_aprox = np.eye(n)  # Inversa da hessiana inicial
    gradk = gradient(xk, funcao_string)

    result = OptimizationResult(
        numero_iteracoes=0,
        X_otimo=xk.tolist(),
        f_otimo=float("inf"),
        X_iteracoes=[xk.tolist()],
        f_iteracoes=[float(equation(*xk))],
    )

    for k in range(max_iter):
        result.numero_iteracoes += 1
        if np.linalg.norm(gradk) < tol:
            print(f"Convergiu em {k} iterações")
            result.X_otimo = deepcopy(xk.tolist())
            result.f_otimo = float(equation(*xk))
            return asdict(result)

        # Direção de busca
        direction = np.asarray(-hinv_aprox @ gradk.T).reshape((1, 2))

        # Busca linear do parâmetro alpha (Backtracking simples)
        alpha = 1.0
        c = 1e-4
        while (
            equation(*(xk + alpha * direction.reshape(2)))
            > equation(*xk) + c * alpha * gradk @ direction.T
        ):
            alpha *= 0.5

        # Atualização de posição e gradiente
        xk_new = xk + alpha * direction.reshape(2)
        grad_new = gradient(xk_new, funcao_string)
        s = xk_new - xk
        y = grad_new - gradk

        # Atualização BFGS
        rho = 1.0 / (y @ s.T)
        idt = np.eye(n)

        # Forma padrão de Sherman-Morrison
        hinv_aprox = (idt - rho * np.outer(s, y)) @ hinv_aprox @ (
            idt - rho * np.outer(y, s)
        ) + rho * np.outer(s, s)

        xk, gradk = xk_new, grad_new

        result.X_iteracoes.append(xk.tolist())
        result.f_iteracoes.append(float(equation(*xk)))

    return asdict(result)
