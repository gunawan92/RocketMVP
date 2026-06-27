from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, GUID, TimestampMixin, UUIDPrimaryKeyMixin


class Rocket(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "rockets"
    __table_args__ = (
        CheckConstraint("wet_mass > 0", name="check_rocket_wet_mass_positive"),
        CheckConstraint("dry_mass > 0", name="check_rocket_dry_mass_positive"),
        CheckConstraint("payload_mass >= 0", name="check_rocket_payload_mass_non_negative"),
        CheckConstraint("wet_mass > dry_mass", name="check_rocket_wet_mass_greater_than_dry_mass"),
        CheckConstraint("payload_mass <= wet_mass", name="check_rocket_payload_not_greater_than_wet_mass"),
        CheckConstraint("diameter IS NULL OR diameter > 0", name="check_rocket_diameter_positive"),
        CheckConstraint("length IS NULL OR length > 0", name="check_rocket_length_positive"),
        CheckConstraint("drag_coefficient IS NULL OR drag_coefficient > 0", name="check_rocket_drag_coefficient_positive"),
        CheckConstraint("center_of_mass_position IS NULL OR center_of_mass_position >= 0", name="check_rocket_center_of_mass_position_non_negative"),
        CheckConstraint("motor_position IS NULL OR motor_position >= 0", name="check_rocket_motor_position_non_negative"),
        CheckConstraint("nose_length IS NULL OR nose_length > 0", name="check_rocket_nose_length_positive"),
        CheckConstraint("fin_count IS NULL OR fin_count > 0", name="check_rocket_fin_count_positive"),
        CheckConstraint("fin_root_chord IS NULL OR fin_root_chord > 0", name="check_rocket_fin_root_chord_positive"),
        CheckConstraint("fin_tip_chord IS NULL OR fin_tip_chord > 0", name="check_rocket_fin_tip_chord_positive"),
        CheckConstraint("fin_span IS NULL OR fin_span > 0", name="check_rocket_fin_span_positive"),
        CheckConstraint("fin_position IS NULL OR fin_position >= 0", name="check_rocket_fin_position_non_negative"),
        Index("idx_rockets_mission_id", "mission_id"),
        Index("idx_rockets_engine_id", "engine_id"),
    )

    mission_id: Mapped[str] = mapped_column(GUID(), ForeignKey("missions.id", ondelete="CASCADE"), nullable=False)
    engine_id: Mapped[str | None] = mapped_column(GUID(), ForeignKey("engines.id", ondelete="SET NULL"))
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    wet_mass: Mapped[float] = mapped_column(nullable=False)
    dry_mass: Mapped[float] = mapped_column(nullable=False)
    payload_mass: Mapped[float] = mapped_column(nullable=False)
    diameter: Mapped[float | None]
    length: Mapped[float | None]
    drag_coefficient: Mapped[float | None]
    center_of_mass_position: Mapped[float | None]
    motor_position: Mapped[float | None]
    nose_length: Mapped[float | None]
    nose_kind: Mapped[str | None] = mapped_column(String(80))
    fin_count: Mapped[int | None]
    fin_root_chord: Mapped[float | None]
    fin_tip_chord: Mapped[float | None]
    fin_span: Mapped[float | None]
    fin_position: Mapped[float | None]
    notes: Mapped[str | None] = mapped_column(Text)

    mission: Mapped["Mission"] = relationship(back_populates="rockets")
    engine: Mapped["Engine | None"] = relationship(back_populates="rockets")
    calculator_results: Mapped[list["CalculatorResult"]] = relationship(back_populates="rocket")
    simulation_results: Mapped[list["SimulationResult"]] = relationship(back_populates="rocket", cascade="all, delete-orphan")
