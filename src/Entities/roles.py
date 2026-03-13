import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.app import db


class Role(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="roles")