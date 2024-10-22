from fastapi import APIRouter, Path, Depends, Body
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from http import HTTPStatus

from referral_module.api.schemas import ReferralCode, UserBase, BoolResponse
from referral_module.services.dependency import (
    get_code_repository,
    get_code_gen_service,
    token_required,
)


router = APIRouter()


@router.post(
    "/codes/", dependencies=[Depends(token_required())], response_model=ReferralCode
)
async def create_new_code(
    code_gen_service=Depends(get_code_gen_service), user=Depends(token_required())
):
    try:
        new_code = await code_gen_service.generate_code(user_id=user["id"])
    except Exception as exc:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=exc.args,
        )
    return JSONResponse(content=new_code)


@router.delete(
    "/codes/{id}", dependencies=[Depends(token_required())], response_model=BoolResponse
)
async def delete_code(
    codes_service=Depends(get_code_gen_service),
    user=Depends(token_required()),
    id: int = Path(title="Id of the code"),
):
    try:
        await codes_service.delete_code(code_id=id, user_id=user["id"])
        return JSONResponse(content={"result": True})
    except Exception as exc:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=exc.args,
        )


@router.get(
    "/codes/email/",
    dependencies=[Depends(token_required())],
    response_model=ReferralCode,
)
async def get_code_by_email(
    user_email: UserBase, codes_service=Depends(get_code_gen_service)
):
    try:
        code = await codes_service.get_code_by_email(user_email.email)
        return JSONResponse(content=code)
    except Exception as exc:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=exc.args,
        )
