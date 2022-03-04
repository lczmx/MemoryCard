"""
路由分发页面
"""
from fastapi import FastAPI

from api import review, cards, analyse, category, plans, user, help


def bind_router(app: FastAPI):
    app.include_router(review.router)
    app.include_router(cards.router)
    app.include_router(category.router)
    app.include_router(analyse.router)
    app.include_router(plans.router)
    app.include_router(user.router)
    app.include_router(help.router)
