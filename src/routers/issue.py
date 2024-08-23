from fastapi import APIRouter
from fastapi.responses import JSONResponse
from http import HTTPStatus

from src.database.crud import create_issue, delete_issue


router = APIRouter(
    prefix="/issues"
)


router.post("")
def create_issue_api(generate_output_id: int, issue_image_url: str, issue_type: str):
    res = create_issue(generate_output_id, issue_image_url, issue_type)
    if res is None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={
            "status": "fail",
            "code": HTTPStatus.BAD_REQUEST,
            "message": "Get urls failed!"
        })
    
    return JSONResponse(status_code=HTTPStatus.OK, content={
        "status": "success",
        "code": HTTPStatus.OK,
    })


router.delete("")
def delete_issue_api(id: int):
    res = delete_issue(id)
    if res is None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={
            "status": "fail",
            "code": HTTPStatus.BAD_REQUEST,
            "message": "Get urls failed!"
        })
    
    return JSONResponse(status_code=HTTPStatus.OK, content={
        "status": "success",
        "code": HTTPStatus.OK,
    })
