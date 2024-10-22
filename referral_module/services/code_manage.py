import random
import string
import os
from dotenv import load_dotenv

from datetime import datetime, timedelta
from referral_module.models.repository import UsersRepository, CodesRepository

load_dotenv()

CODE_LIFE_TIME_DAYS = os.getenv("CODE_LIFE_TIME_DAYS")


class RefCodeGeneration:

    def __init__(
        self, cose_service_cls=CodesRepository, users_service_cls=UsersRepository
    ):
        self._code_service = cose_service_cls()
        self._user_service = users_service_cls()

    def _generate_unique_code(self, length):
        characters = string.ascii_letters + string.digits
        unique_code = "".join(random.choice(characters) for _ in range(length))
        return unique_code

    def _expired_date(self):
        return datetime.today() + timedelta(days=int(CODE_LIFE_TIME_DAYS))

    async def generate_code(self, user_id, length=10):
        current_code = await self._code_service.get_code_by_user_id(user_id=user_id)
        if current_code:
            raise Exception("You can't have more than one active referral code")
        code = self._generate_unique_code(length)
        expired_date = self._expired_date()
        try:
            new_code = await self._code_service.create_code(
                code=code, expired_date=expired_date, user_id=user_id
            )
            return new_code
        except:
            raise Exception("Something went wrong, please try again later")

    async def get_code_by_email(self, email):
        user = await self._user_service.get_by_email(email=email)
        if not user:
            raise Exception("No users with this email")
        code = await self._code_service.get_code_by_user_id(user_id=user["id"])
        return code

    async def delete_code(self, code_id, user_id):
        code = await self._code_service.get_code_by_id(code_id)
        if not code:
            raise Exception("No this code in database")
        if code["user_id"] != user_id:
            raise Exception("Denied")
        await self._code_service.delete_code(code_id)
