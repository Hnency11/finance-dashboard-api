from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session for FastAPI dependencies."""
    # The session is request-scoped and will auto-close when the request finishes
    async with AsyncSessionLocal() as session:
        yield session
