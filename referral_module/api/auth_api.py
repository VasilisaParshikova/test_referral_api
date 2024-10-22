from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from http import HTTPStatus
from typing import Union, Annotated
from fastapi.security import OAuth2PasswordRequestForm

from referral_module.services.dependency import get_auth_user_func, get_register_user_func, oauth, GOOGLE_REDIRECT_URI, get_auth_google_user_func
from referral_module.api.schemas import Token, UserAnswer

router = APIRouter()


@router.post("/register/", response_model=UserAnswer)
async def register(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        registration_func=Depends(get_register_user_func),
        ref_code: Union[str, None] = None):
    try:
        new_user = await registration_func(form_data.username, form_data.password, ref_code)
        return JSONResponse(content=new_user)
    except Exception as exc:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=exc.args
        )


@router.post("/login/", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], user_service=Depends(get_auth_user_func)):
    try:
        token = await user_service(form_data.username, form_data.password)
        return JSONResponse(content=token)
    except Exception as exc:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=exc.args,
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.get("/login/google")
async def google_login(request: Request, ref_code: Union[str, None] = None):
    redirect_uri = request.url_for("auth_google")
    print(redirect_uri)
    if not ref_code:
        ref_code='none'
    return await oauth.google.authorize_redirect(request, redirect_uri, state=ref_code)


@router.get("/auth/google", response_model=Token)
async def auth_google(request: Request,
                      registration_func=Depends(get_auth_google_user_func),
                      state: Union[str, None] = None):
    ref_code = None
    if state != 'none':
        ref_code = state
    try:
        token = await registration_func(request, ref_code)
        return JSONResponse(content=token)
    except Exception as exc:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=exc.args
        )
