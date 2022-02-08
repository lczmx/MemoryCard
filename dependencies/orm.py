"""
orm相关的依赖
"""

from orm import SessionLocal


async def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
