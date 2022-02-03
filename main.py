from fastapi import FastAPI
from app import home_router, category_router, analyse_router

app = FastAPI()

app.include_router(home_router)
app.include_router(category_router)
app.include_router(analyse_router)
