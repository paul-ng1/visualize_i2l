from fastapi import APIRouter
from fastapi.responses import JSONResponse
from http import HTTPStatus

from src.database.crud import get_page_urls_by_checked_page, get_capture_url_by_id,\
                                get_sections_url_by_id, get_atoms_url_by_id,\
                                get_codegens_url_by_id, convert_generate_output_to_checked
from src.routers.utils import filter_urls


router = APIRouter(
    prefix="/generate_output"
)


@router.get("/pages")
def get_pages_url_api(page: int=1, limit: int=10, checked: bool|None=None):
    urls = get_page_urls_by_checked_page(page, limit, checked)
    if urls is None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={
            "status": "fail",
            "code": HTTPStatus.BAD_REQUEST,
            "message": "Get urls failed!"
        })
    
    result = filter_urls(urls)

    return JSONResponse(status_code=HTTPStatus.OK, content={
        "status": "success",
        "code": HTTPStatus.OK,
        "data": result
    })


@router.get("/capture/{id}")
def get_capture_url_api(id: int):
    urls = get_capture_url_by_id(id)
    if urls is None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={
            "status": "fail",
            "code": HTTPStatus.BAD_REQUEST,
            "message": "Get urls failed!"
        })
    
    result = filter_urls(urls)

    return JSONResponse(status_code=HTTPStatus.OK, content={
        "status": "success",
        "code": HTTPStatus.OK,
        "data": result
    })


@router.get("/sections/{id}")
def get_sections_url_image_api(id: int):
    urls = get_sections_url_by_id(id)
    if urls is None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={
            "status": "fail",
            "code": HTTPStatus.BAD_REQUEST,
            "message": "Get urls failed!"
        })
    
    result = filter_urls(urls)

    return JSONResponse(status_code=HTTPStatus.OK, content={
        "status": "success",
        "code": HTTPStatus.OK,
        "data": result
    })


@router.get("/atoms/{id}")
def get_atoms_url_image_api(id: int):
    urls = get_atoms_url_by_id(id)
    if urls is None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={
            "status": "fail",
            "code": HTTPStatus.BAD_REQUEST,
            "message": "Get urls failed!"
        })
    
    result = filter_urls(urls)

    return JSONResponse(status_code=HTTPStatus.OK, content={
        "status": "success",
        "code": HTTPStatus.OK,
        "data": result
    })


@router.get("/codegens/{id}")
def get_codegens_image_api(id: int):
    urls = get_codegens_url_by_id(id)
    if urls is None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={
            "status": "fail",
            "code": HTTPStatus.BAD_REQUEST,
            "message": "Get urls failed!"
        })
    
    result = filter_urls(urls)

    return JSONResponse(status_code=HTTPStatus.OK, content={
        "status": "success",
        "code": HTTPStatus.OK,
        "data": result
    })


@router.put("/checked/{id}")
def convert_generate_output_to_checked_api(id: int):
    urls = convert_generate_output_to_checked(id)
    if urls is None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={
            "status": "fail",
            "code": HTTPStatus.BAD_REQUEST,
            "message": "Get urls failed!"
        })
    
    result = filter_urls(urls)

    return JSONResponse(status_code=HTTPStatus.OK, content={
        "status": "success",
        "code": HTTPStatus.OK,
        "data": result
    })
