from fastapi import APIRouter
from fastapi.responses import JSONResponse
from http import HTTPStatus

from src.database.crud import get_generate_outputs_by_checked_and_page,\
                            get_generate_output_by_id, update_generate_output_to_checked
from src.routers.utils import filter_generate_output, filter_generate_outputs


router = APIRouter(
    prefix="/generate_outputs"
)


@router.get("")
def get_generate_outputs_api(page: int=1, limit: int=10, checked: bool|None=None):
    generate_outputs = get_generate_outputs_by_checked_and_page(page, limit, checked)
    if generate_outputs is None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={
            "status": "fail",
            "code": HTTPStatus.BAD_REQUEST,
            "message": "Get generate outputs failed!"
        })

    result = filter_generate_outputs(generate_outputs)

    return JSONResponse(status_code=HTTPStatus.OK, content={
        "status": "success",
        "code": HTTPStatus.OK,
        "data": result
    })


@router.get("/{id}")
def get_generate_output_api(id: int):
    generate_output = get_generate_output_by_id(id)
    if generate_output is None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={
            "status": "fail",
            "code": HTTPStatus.BAD_REQUEST,
            "message": "Get generate output failed!"
        })

    result = [filter_generate_output(generate_output)]

    return JSONResponse(status_code=HTTPStatus.OK, content={
        "status": "success",
        "code": HTTPStatus.OK,
        "data": result
    })


@router.put("/checked/{id}")
def update_generate_output_to_checked_api(id: int):
    check = update_generate_output_to_checked(id)
    if check is None or check == 0:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={
            "status": "fail",
            "code": HTTPStatus.BAD_REQUEST,
            "message": "Update failed!"
        })    

    return JSONResponse(status_code=HTTPStatus.OK, content={
        "status": "success",
        "code": HTTPStatus.OK,
    })
