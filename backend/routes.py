"""
Define os endpoints da API.

Recebe requisições, chama o algoritmo e retorna a resposta.
"""
from fastapi import APIRouter
from pydantic import BaseModel, Field, ConfigDict
from src.optimizer.methods import quasi_newton

router = APIRouter()

class OptimizeRequest(BaseModel):
    """Modelo para a entrada o end-point optimize"""
    objective_function: str # atualmente não usado
    initial_point: list
    tolerance: float
    stopping_criterion: str # atualmente não usado
    max_iterations: int



class OptimizationResponse(BaseModel):
    """Modelo para a saída do end-point optimize"""
    numero_iteracoes: int
    f_otimo: float
    X_otimo: tuple[float, float] = Field(
        ...,
        description="Coordenadas do ponto ótimo encontrado"
    )
    X_iteracoes: list[tuple[float, float]] = Field(
        ...,
        description="Histórico dos pontos x1 e x2 a cada iteração"
    )
    f_iteracoes: list[float] = Field(
        ...,
        description="Histórico do valor da função objetivo"
    )

    # Configuração centralizada do exemplo para o Swagger
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "numero_iteracoes": 9,
                "f_otimo": 150.0,
                "X_otimo": [5.7, 5.700000000000015],
                "X_iteracoes": [
                    [1e+32, 2.0],
                    [5e+31, 2.8222222222222255],
                    [5.700075221731893, 5.700004161706511],
                    [5.7, 5.700000000000015]
                ],
                "f_iteracoes": [2.50000004e+63, 150.17085984, 150.4403478, 150.0]
            }
        }
    )



@router.post(
    '/optimize',
    response_model=OptimizationResponse,
    summary="Executa Otimização Quasi-Newton (BFGS)",
    description="Endpoint que recebe a função objetivo e os pontos iniciais para calcular o mínimo local usando o algoritmo BFGS."
)
async def optimize(payload: OptimizeRequest):
    """Execução do Algoritmo Quasi-Newton"""
    result_dict = quasi_newton(
        initial_points=payload.initial_point,
        tol=payload.tolerance,
        max_iter=payload.max_iterations
    )

    return result_dict


@router.get('/')
def main():
    return {
        "result": "Success. Acesse o /docs para mais informações."
    }
