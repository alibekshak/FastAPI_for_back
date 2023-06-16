from typing import Any

from fastapi import Depends, Response, HTTPException
import imghdr

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


@router.delete("/shanyraks/{id}/media")
def delete_shanyrak(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    delete_result = svc.repository.delete_shanyrak_by_id(shanyrak_id, jwt_data.user_id)
    if delete_result.deleted_count == 1:
        return Response(status_code=200)
    raise HTTPException(status_code=404)


@router.delete("/shanyraks/{id}/media")
def delete_shanyrak_photos(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Any:
    shanyrak = svc.repository.get_shanyrak_by_id(shanyrak_id, jwt_data.user_id)
    delete = shanyrak.get("media", [])
    for url in delete:
        svc.s3_service.delete_file(url.split("/")[-1])
    return delete

@router.delete("/shanyraks/{id}/comments/{comment_id}")
def delete_comment(
    comment_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    delete_comment = svc.comment_repository.delete_comment_by_id(comment_id, jwt_data.user_id)
    if delete_comment.deleted_count == 1:
        return Response(status_code=200)
    raise HTTPException(status_code=404)