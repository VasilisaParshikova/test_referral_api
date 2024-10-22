from referral_module.models.repository import UsersRepository, CodesRepository
from referral_module.services.code_manage import RefCodeGeneration
from referral_module.services.auth_utils import auth_user_func, register_user_func, get_current_user, oauth, GOOGLE_REDIRECT_URI, auth_google_callback


def get_user_repository():
    return UsersRepository()


def get_code_repository():
    return CodesRepository()


def get_code_gen_service():
    return RefCodeGeneration()


def get_auth_user_func():
    return auth_user_func

def get_register_user_func():
    return register_user_func

def get_auth_google_user_func():
    return auth_google_callback

def token_required():
    return get_current_user