from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv

from referral_module.api import auth_api, referral_code_api, users_api
from referral_module.models.database import engine, session, Base

load_dotenv()


app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

app.include_router(auth_api.router, prefix="/users", tags=["Users"])
app.include_router(users_api.router, prefix="/users", tags=["Users"])
app.include_router(referral_code_api.router, prefix="", tags=["Codes"])


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.get("/")
async def root():
    return {"message": "Welcome to API"}


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
