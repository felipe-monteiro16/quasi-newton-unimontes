"""Nonlinear optimization entry point"""

import json
from pathlib import Path

from methods import quasi_newton

ERROR_THRESHOLD = 1e-64
N_ITER = 100
INITIAL_POINTS = [1e32, 2]



def main() -> int:
    """Executar o algoritmo de otimização Quasi-Newton.

    Returns:
        Um inteiro para ser consumido pelo SytemExit.
    """

    result_dict = quasi_newton(
        initial_points=INITIAL_POINTS, tol=ERROR_THRESHOLD, max_iter=N_ITER
    )
    path = Path(__file__).resolve().parent / "optimization_result.json"
    with open(path, "w") as json_file:
        json.dump(result_dict, json_file, indent=4)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
