"""create initial tables

Revision ID: 20260625_0001
Revises:
Create Date: 2026-06-25
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260625_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "missions",
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "engines",
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("thrust", sa.Float(), nullable=False),
        sa.Column("isp", sa.Float(), nullable=False),
        sa.Column("burn_time", sa.Float(), nullable=True),
        sa.Column("propellant_mass", sa.Float(), nullable=True),
        sa.Column("manufacturer", sa.String(length=150), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("burn_time IS NULL OR burn_time > 0", name="check_engine_burn_time_positive"),
        sa.CheckConstraint("isp > 0", name="check_engine_isp_positive"),
        sa.CheckConstraint("propellant_mass IS NULL OR propellant_mass > 0", name="check_engine_propellant_mass_positive"),
        sa.CheckConstraint("thrust > 0", name="check_engine_thrust_positive"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "rockets",
        sa.Column("mission_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("engine_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("wet_mass", sa.Float(), nullable=False),
        sa.Column("dry_mass", sa.Float(), nullable=False),
        sa.Column("payload_mass", sa.Float(), nullable=False),
        sa.Column("diameter", sa.Float(), nullable=True),
        sa.Column("length", sa.Float(), nullable=True),
        sa.Column("drag_coefficient", sa.Float(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("diameter IS NULL OR diameter > 0", name="check_rocket_diameter_positive"),
        sa.CheckConstraint("drag_coefficient IS NULL OR drag_coefficient > 0", name="check_rocket_drag_coefficient_positive"),
        sa.CheckConstraint("dry_mass > 0", name="check_rocket_dry_mass_positive"),
        sa.CheckConstraint("length IS NULL OR length > 0", name="check_rocket_length_positive"),
        sa.CheckConstraint("payload_mass <= wet_mass", name="check_rocket_payload_not_greater_than_wet_mass"),
        sa.CheckConstraint("payload_mass >= 0", name="check_rocket_payload_mass_non_negative"),
        sa.CheckConstraint("wet_mass > 0", name="check_rocket_wet_mass_positive"),
        sa.CheckConstraint("wet_mass > dry_mass", name="check_rocket_wet_mass_greater_than_dry_mass"),
        sa.ForeignKeyConstraint(["engine_id"], ["engines.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["mission_id"], ["missions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_rockets_engine_id", "rockets", ["engine_id"])
    op.create_index("idx_rockets_mission_id", "rockets", ["mission_id"])
    op.create_table(
        "calculator_results",
        sa.Column("mission_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("rocket_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("calculator_type", sa.String(length=100), nullable=False),
        sa.Column("input_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("result_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.ForeignKeyConstraint(["mission_id"], ["missions.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["rocket_id"], ["rockets.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_calculator_results_mission_id", "calculator_results", ["mission_id"])
    op.create_index("idx_calculator_results_rocket_id", "calculator_results", ["rocket_id"])
    op.create_index("idx_calculator_results_type", "calculator_results", ["calculator_type"])
    op.create_table(
        "simulation_results",
        sa.Column("mission_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("rocket_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("apogee", sa.Float(), nullable=True),
        sa.Column("max_velocity", sa.Float(), nullable=True),
        sa.Column("max_acceleration", sa.Float(), nullable=True),
        sa.Column("flight_duration", sa.Float(), nullable=True),
        sa.Column("summary", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("time_series", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("raw_result", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.ForeignKeyConstraint(["mission_id"], ["missions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["rocket_id"], ["rockets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_simulation_results_created_at", "simulation_results", ["created_at"])
    op.create_index("idx_simulation_results_mission_id", "simulation_results", ["mission_id"])
    op.create_index("idx_simulation_results_rocket_id", "simulation_results", ["rocket_id"])
    op.create_index("idx_simulation_results_status", "simulation_results", ["status"])


def downgrade() -> None:
    op.drop_index("idx_simulation_results_status", table_name="simulation_results")
    op.drop_index("idx_simulation_results_rocket_id", table_name="simulation_results")
    op.drop_index("idx_simulation_results_mission_id", table_name="simulation_results")
    op.drop_index("idx_simulation_results_created_at", table_name="simulation_results")
    op.drop_table("simulation_results")
    op.drop_index("idx_calculator_results_type", table_name="calculator_results")
    op.drop_index("idx_calculator_results_rocket_id", table_name="calculator_results")
    op.drop_index("idx_calculator_results_mission_id", table_name="calculator_results")
    op.drop_table("calculator_results")
    op.drop_index("idx_rockets_mission_id", table_name="rockets")
    op.drop_index("idx_rockets_engine_id", table_name="rockets")
    op.drop_table("rockets")
    op.drop_table("engines")
    op.drop_table("missions")
