from fastapi import FastAPI
from api import router


app = FastAPI(
    title='testlastic',
    description='Сервис поиска по тексту',
    version='1.0.0')

app.include_router(router)

