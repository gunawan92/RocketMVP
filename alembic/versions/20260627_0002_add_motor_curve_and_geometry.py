"""add motor curve and rocket geometry fields

Revision ID: 20260627_0002
Revises: 20260625_0001
Create Date: 2026-06-27
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260627_0002"
down_revision: Union[str, None] = "20260625_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("engines", sa.Column("motor_curve", postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column("engines", sa.Column("nozzle_radius", sa.Float(), nullable=True))
    op.add_column("engines", sa.Column("throat_radius", sa.Float(), nullable=True))
    op.create_check_constraint("check_engine_nozzle_radius_positive", "engines", "nozzle_radius IS NULL OR nozzle_radius > 0")
    op.create_check_constraint("check_engine_throat_radius_positive", "engines", "throat_radius IS NULL OR throat_radius > 0")

    op.add_column("rockets", sa.Column("center_of_mass_position", sa.Float(), nullable=True))
    op.add_column("rockets", sa.Column("motor_position", sa.Float(), nullable=True))
    op.add_column("rockets", sa.Column("nose_length", sa.Float(), nullable=True))
    op.add_column("rockets", sa.Column("nose_kind", sa.String(length=80), nullable=True))
    op.add_column("rockets", sa.Column("fin_count", sa.Integer(), nullable=True))
    op.add_column("rockets", sa.Column("fin_root_chord", sa.Float(), nullable=True))
    op.add_column("rockets", sa.Column("fin_tip_chord", sa.Float(), nullable=True))
    op.add_column("rockets", sa.Column("fin_span", sa.Float(), nullable=True))
    op.add_column("rockets", sa.Column("fin_position", sa.Float(), nullable=True))
    op.create_check_constraint(
        "check_rocket_center_of_mass_position_non_negative",
        "rockets",
        "center_of_mass_position IS NULL OR center_of_mass_position >= 0",
    )
    op.create_check_constraint("check_rocket_motor_position_non_negative", "rockets", "motor_position IS NULL OR motor_position >= 0")
    op.create_check_constraint("check_rocket_nose_length_positive", "rockets", "nose_length IS NULL OR nose_length > 0")
    op.create_check_constraint("check_rocket_fin_count_positive", "rockets", "fin_count IS NULL OR fin_count > 0")
    op.create_check_constraint("check_rocket_fin_root_chord_positive", "rockets", "fin_root_chord IS NULL OR fin_root_chord > 0")
    op.create_check_constraint("check_rocket_fin_tip_chord_positive", "rockets", "fin_tip_chord IS NULL OR fin_tip_chord > 0")
    op.create_check_constraint("check_rocket_fin_span_positive", "rockets", "fin_span IS NULL OR fin_span > 0")
    op.create_check_constraint("check_rocket_fin_position_non_negative", "rockets", "fin_position IS NULL OR fin_position >= 0")


def downgrade() -> None:
    op.drop_constraint("check_rocket_fin_position_non_negative", "rockets", type_="check")
    op.drop_constraint("check_rocket_fin_span_positive", "rockets", type_="check")
    op.drop_constraint("check_rocket_fin_tip_chord_positive", "rockets", type_="check")
    op.drop_constraint("check_rocket_fin_root_chord_positive", "rockets", type_="check")
    op.drop_constraint("check_rocket_fin_count_positive", "rockets", type_="check")
    op.drop_constraint("check_rocket_nose_length_positive", "rockets", type_="check")
    op.drop_constraint("check_rocket_motor_position_non_negative", "rockets", type_="check")
    op.drop_constraint("check_rocket_center_of_mass_position_non_negative", "rockets", type_="check")
    op.drop_column("rockets", "fin_position")
    op.drop_column("rockets", "fin_span")
    op.drop_column("rockets", "fin_tip_chord")
    op.drop_column("rockets", "fin_root_chord")
    op.drop_column("rockets", "fin_count")
    op.drop_column("rockets", "nose_kind")
    op.drop_column("rockets", "nose_length")
    op.drop_column("rockets", "motor_position")
    op.drop_column("rockets", "center_of_mass_position")

    op.drop_constraint("check_engine_throat_radius_positive", "engines", type_="check")
    op.drop_constraint("check_engine_nozzle_radius_positive", "engines", type_="check")
    op.drop_column("engines", "throat_radius")
    op.drop_column("engines", "nozzle_radius")
    op.drop_column("engines", "motor_curve")
