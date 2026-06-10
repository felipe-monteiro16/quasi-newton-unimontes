from collections.abc import Callable

import numpy as np
import numpy.typing as npt

from ..functions import BaseFunction


def initial_variables(
    function_instance: BaseFunction,
) -> tuple[np.float64, np.float64, npt.NDArray[np.float64]]:
    scale = np.float64(function_instance.xx.mean())
    alpha = scale if scale != 0 else np.float64(0.1)
    best_xx = np.asarray([], np.float64)
    best_y = function_instance.y().flatten()[0]
    return alpha, best_y, best_xx


def minimizing(
    function_instance: BaseFunction,
    dk_function: Callable[[], npt.NDArray[np.float64]],
    error_threshold: np.float64,
    n_iter: int,
) -> tuple[np.float64, npt.NDArray[np.float64]]:
    # SET UP THE OPTIMIZING
    alpha, best_y, best_xx = initial_variables(function_instance)

    # RUN THE OPTIMIZING
    for _ in range(n_iter):
        xx_k = function_instance.xx
        xx_k = xx_k - alpha * dk_function()
        xx_k = np.vstack((function_instance.xx, xx_k))
        function_instance.xx = xx_k
        values = function_instance.y()
        function_instance.xx = xx_k[np.argmin(values)]
        y = np.float64(values.min())
        if y < best_y:
            if abs(y - best_y) < error_threshold:
                best_y = y
                best_xx = function_instance.xx
                return best_y, best_xx
            best_y = y
            best_xx = function_instance.xx
        else:
            alpha *= 0.1
    print("Maximum number of iterations performed")
    return best_y, best_xx
