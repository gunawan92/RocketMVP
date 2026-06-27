from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.calculator_result import CalculatorResult
from app.models.engine import Engine
from app.models.mission import Mission
from app.models.rocket import Rocket
from app.models.simulation_result import SimulationResult
from app.schemas.dashboard import BestApogeeSummary, DashboardSummary, LatestSimulationSummary


class DashboardService:
    @staticmethod
    def get_summary(db: Session) -> DashboardSummary:
        best_apogee_result = db.scalar(
            select(SimulationResult)
            .where(SimulationResult.apogee.is_not(None))
            .order_by(SimulationResult.apogee.desc())
            .limit(1)
        )
        latest_simulation = db.scalar(
            select(SimulationResult)
            .order_by(SimulationResult.created_at.desc())
            .limit(1)
        )

        return DashboardSummary(
            total_missions=DashboardService._count(db, Mission),
            total_engines=DashboardService._count(db, Engine),
            total_rockets=DashboardService._count(db, Rocket),
            total_simulations=DashboardService._count(db, SimulationResult),
            total_calculator_results=DashboardService._count(db, CalculatorResult),
            best_apogee=BestApogeeSummary(
                value=best_apogee_result.apogee if best_apogee_result else None,
                simulation_id=best_apogee_result.id if best_apogee_result else None,
            ),
            latest_simulation=LatestSimulationSummary(
                id=latest_simulation.id if latest_simulation else None,
                status=latest_simulation.status if latest_simulation else None,
                created_at=latest_simulation.created_at if latest_simulation else None,
            ),
        )

    @staticmethod
    def _count(db: Session, model) -> int:
        return db.scalar(select(func.count()).select_from(model)) or 0
