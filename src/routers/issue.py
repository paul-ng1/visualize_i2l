from fastapi import APIRouter
from fastapi.responses import JSONResponse
from http import HTTPStatus

from src.database.crud import create_issue, get_issues_by_page, get_issue, update_issue, delete_issue
from src.database.schemas import IssueBase


router = APIRouter(
    prefix="/issues"
)


@router.post("")
def create_issue_api(data: IssueBase):
    res = create_issue(data.generate_output_id, data.issue_image_url, data.issue_type, data.note)
    if res is None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={
            "status": "fail",
            "code": HTTPStatus.BAD_REQUEST,
            "message": "Creste issue failed!"
        })
    
    return JSONResponse(status_code=HTTPStatus.OK, content={
        "status": "success",
        "code": HTTPStatus.OK,
    })


@router.get("")
def get_issues_by_pages_api(page: int=1, limit: int=10):
    issues = get_issues_by_page(page, limit)
    result = [issue.to_dict() for issue in issues]
    if issues is None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={
            "status": "fail",
            "code": HTTPStatus.BAD_REQUEST,
            "message": "Get issues failed!"
        })
    
    return JSONResponse(status_code=HTTPStatus.OK, content={
        "status": "success",
        "code": HTTPStatus.OK,
        "data": result
    })


@router.get("/{id}")
def get_issue_api(id: int):
    issue = get_issue(id)
    if issue is None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={
            "status": "fail",
            "code": HTTPStatus.BAD_REQUEST,
            "message": "Get issue failed!"
        })
    
    return JSONResponse(status_code=HTTPStatus.OK, content={
        "status": "success",
        "code": HTTPStatus.OK,
        "data": issue.to_dict()
    })


@router.put("/{id}")
def update_issue_api(id: int):
    check = update_issue(id)
    if check is None or check == 0:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={
            "status": "fail",
            "code": HTTPStatus.BAD_REQUEST,
            "message": "Update failed!"
        })
    
    return JSONResponse(status_code=HTTPStatus.OK, content={
        "status": "success",
        "code": HTTPStatus.OK
    })


@router.delete("/{id}")
def delete_issue_api(id: int):
    id_ = delete_issue(id)
    if id_ is None:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={
            "status": "fail",
            "code": HTTPStatus.BAD_REQUEST,
            "message": "Delete failed!"
        })
    
    return JSONResponse(status_code=HTTPStatus.OK, content={
        "status": "success",
        "code": HTTPStatus.OK,
    })
