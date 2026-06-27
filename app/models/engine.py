from sqlalchemy import CheckConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, JSONData, TimestampMixin, UUIDPrimaryKeyMixin


class Engine(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "engines"
    __table_args__ = (
        CheckConstraint("thrust > 0", name="check_engine_thrust_positive"),
        CheckConstraint("isp > 0", name="check_engine_isp_positive"),
        CheckConstraint("burn_time IS NULL OR burn_time > 0", name="check_engine_burn_time_positive"),
        CheckConstraint("propellant_mass IS NULL OR propellant_mass > 0", name="check_engine_propellant_mass_positive"),
        CheckConstraint("nozzle_radius IS NULL OR nozzle_radius > 0", name="check_engine_nozzle_radius_positive"),
        CheckConstraint("throat_radius IS NULL OR throat_radius > 0", name="check_engine_throat_radius_positive"),
    )

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    thrust: Mapped[float] = mapped_column(nullable=False)
    isp: Mapped[float] = mapped_column(nullable=False)
    burn_time: Mapped[float | None]
    propellant_mass: Mapped[float | None]
    motor_curve: Mapped[list[dict] | None] = mapped_column(JSONData())
    nozzle_radius: Mapped[float | None]
    throat_radius: Mapped[float | None]
    manufacturer: Mapped[str | None] = mapped_column(String(150))
    notes: Mapped[str | None] = mapped_column(Text)

    rockets: Mapped[list["Rocket"]] = relationship(back_populates="engine")
