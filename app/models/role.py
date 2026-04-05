import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid, String

from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class Role(Base):
    __tablename__ = "roles"

    # System roles like admin, analyst, viewer
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    
    users: Mapped[list["User"]] = relationship(back_populates="role")
