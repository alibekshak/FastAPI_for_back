from typing import Any

from fastapi import Depends, status
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreateShanyrakRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


class CreateShanyrakResponse(AppModel):
    id: Any = Field(alias="_id")


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_shanyrak(
    input: CreateShanyrakRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:

    date = svc.repository.create_shanyrak(jwt_data.user_id, input.dict())
    return CreateShanyrakResponse(id=date)
