from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Mission(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "missions"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="DRAFT", nullable=False)

    rockets: Mapped[list["Rocket"]] = relationship(back_populates="mission", cascade="all, delete-orphan")
    calculator_results: Mapped[list["CalculatorResult"]] = relationship(back_populates="mission")
    simulation_results: Mapped[list["SimulationResult"]] = relationship(back_populates="mission", cascade="all, delete-orphan")
