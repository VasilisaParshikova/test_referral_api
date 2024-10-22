FROM python:3.11

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./alembic ./alembic

COPY ./alembic.ini .

COPY ./referral_module ./referral_module

#CMD ["uvicorn", "referral_module.main:app", "--host", "0.0.0.0", "--port", "8000"]

CMD ["bash", "-c", "alembic upgrade head && uvicorn referral_module.main:app --host 0.0.0.0 --port 8000"]
