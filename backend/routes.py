"""
Define os endpoints da API.

Recebe requisições, chama o algoritmo e retorna a resposta.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from src.optimizer.methods import quasi_newton

router = APIRouter()

class OptimizeRequest(BaseModel):
    """Modelo para a requisição optimize"""
    objective_function: str # atualmente não usado
    initial_point: list
    tolerance: float
    stopping_criterion: str # atualmente não usado
    max_iterations: int


@router.post('/optimize')
def optimize(request_data: OptimizeRequest):
    """Execução do Algoritmo Quasi-Newton"""
    result_dict = quasi_newton(
        initial_points=request_data.initial_point,
        tol=request_data.tolerance,
        max_iter=request_data.max_iterations
    )

    return result_dict
