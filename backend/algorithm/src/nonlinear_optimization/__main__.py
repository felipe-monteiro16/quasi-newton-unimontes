from time import time

from nonlinear_optimization.methods import quasi_newton

ERROR_THRESHOLD = 1e-64
N_ITER = 100
INITIAL_POINTS = [1e32, 2]


def main() -> int:
    start_time = time()

    best_point = quasi_newton(
        initial_points=INITIAL_POINTS, tol=ERROR_THRESHOLD, max_iter=N_ITER
    )
    print(best_point)
    print(time() - start_time)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
