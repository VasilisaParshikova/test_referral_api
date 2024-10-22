from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.exc import DBAPIError

from referral_module.models.models import Users, Codes
from referral_module.models.database import session


class UsersRepository:

    def __init__(self, db_session=session):
        self._session = db_session

    async def get_by_id(self, id: int):
        user = await self._session.execute(select(Users).where(Users.id == id))
        user = user.scalars().first()
        if not user:
            return {}
        return user.to_json()

    async def get_by_email(self, email: str):
        user = await self._session.execute(select(Users).where(Users.email == email))
        user = user.scalars().first()
        if not user:
            return {}
        return user.to_json()

    async def get_users_referral(self, id: int):
        referrals = await self._session.execute(select(Users).where(Users.referr_id == id))
        referrals = referrals.scalars().all()
        return [referral.to_json() for referral in referrals]

    async def create_user(self, email, hashed_password=None, referr_id=None):
        new_user = Users(email=email, hashed_password=hashed_password, referr_id=referr_id)
        self._session.add(new_user)
        try:
            await self._session.commit()
            return new_user.to_json()
        except DBAPIError as exc:
            raise Exception(f'{exc.detail}')


class CodesRepository:

    def __init__(self, db_session=session):
        self._session = db_session

    async def get_code_by_user_id(self, user_id: int):
        code = await self._session.execute(
            select(Codes).where(Codes.user_id == user_id, Codes.expired_date > func.now()))
        code = code.scalars().first()
        if not code:
            return {}
        return code.to_json()

    async def create_code(self, code: str, expired_date, user_id: int):
        new_code = Codes(code=code, expired_date=expired_date, user_id=user_id)
        self._session.add(new_code)
        try:
            await self._session.commit()
            return new_code.to_json()
        except DBAPIError as exc:
            raise Exception(f'{exc.detail}')

    async def delete_code(self, id: int):
        code = await self._session.execute(select(Codes).where(Codes.id == id))
        code = code.scalars().first()
        if not code:
            raise Exception('No this referral code in database.')
        try:
            await self._session.delete(code)
            return True
        except DBAPIError as exc:
            raise Exception(f'{exc.detail}')

    async def get_code_by_ref_code(self, code: str):
        code = await self._session.execute(select(Codes).where(Codes.code == code))
        code = code.scalars().first()
        if not code:
            return {}
        return code.to_json()

    async def get_code_by_id(self, id:int):
        code = await self._session.execute(select(Codes).where(Codes.id == id))
        code = code.scalars().first()
        if not code:
            return {}
        return code.to_json()
