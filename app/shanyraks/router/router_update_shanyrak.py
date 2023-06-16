from typing import Any, List

from fastapi import Depends, Response, HTTPException, UploadFile

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
import imghdr
from ..service import Service, get_service
from . import router


class UpdateShanyrakRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


class UpdateTextCommentRequest(AppModel):
    content: str

@router.patch("/shanyraks/{id}")
def update_shanyrak(
    shanyrak_id: str,
    input: UpdateShanyrakRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    svc.repository.update_shanyrak_by_id(shanyrak_id, jwt_data.user_id, input.dict())

    return Response(status_code=200)


@router.patch("/shanyraks/{id}/comments/{comment_id}")
def update_text_comment(
    comment_id: str,
    input: UpdateTextCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    svc.comment_repository.update_comment_by_id(comment_id, jwt_data.user_id, input.dict())

    return Response(status_code=200)


@router.post("/shanyraks/{id}/media")
def update_shanyrak_photos(
    shanyrak_id: str,
    files: List[UploadFile],
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Any:
    media_urls = []
    for file in files:
        if not is_image(file.file.read()):
            raise HTTPException(status_code=400)
        url = svc.s3_service.upload_file(file.file, file.filename)
        if url is None:
            raise HTTPException(status_code=500)
        media_urls.append(url)
    update_result = svc.repository.update_shanyrak_by_id(shanyrak_id=shanyrak_id, user_id=jwt_data.user_id, data={"media": media_urls})
    if update_result.acknowledged:
        return media_urls
    raise HTTPException(status_code=404)


def is_image(file_contents: bytes) -> bool:
    image_type = imghdr.what(None, file_contents)
    return image_type is not None