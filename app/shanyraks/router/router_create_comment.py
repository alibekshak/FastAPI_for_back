from fastapi import Depends, HTTPException, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router
from ...utils import AppModel


class CreateCommentRequest(AppModel):
    content: str


@router.post("/shanyraks/{id}/comments")
def create_comment(
    id: str,
    request: CreateCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Response:

    success = svc.comment_repository.create_comment(id, jwt_data.user_id, request.dict())
    if not success:
        raise HTTPException(status_code=404)
    return Response(status_code=200)

