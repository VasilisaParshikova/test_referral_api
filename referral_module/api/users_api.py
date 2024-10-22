from fastapi import APIRouter, Path, Depends, Request
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from http import HTTPStatus
from referral_module.api.schemas import UserList
from referral_module.services.dependency import get_user_repository

router = APIRouter()


@router.get("/{id}/referrals", response_model=UserList)
async def auth_google(
    users_service=Depends(get_user_repository), id: int = Path(title="Id of the user")
):
    user_list = await users_service.get_users_referral(id)
    return JSONResponse(content=user_list)
