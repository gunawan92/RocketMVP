from math import sqrt
from typing import Any

from rocketpy import Environment

from app.core.constants import G0
from app.core.exceptions import SimulationFailedError
from app.models.rocket import Rocket
from app.schemas.simulation import SimulationEnvironment


class RocketPyAdapter:
    @staticmethod
    def run_basic_simulation(
        rocket: Rocket,
        environment_input: SimulationEnvironment,
        include_time_series: bool,
    ) -> dict[str, Any]:
        try:
            environment = Environment(
                latitude=environment_input.latitude,
                longitude=environment_input.longitude,
                elevation=environment_input.elevation,
                date=environment_input.date,
            )
        except Exception as exc:
            raise SimulationFailedError(
                "RocketPy failed to create environment",
                details=[{"field": "environment", "message": str(exc)}],
            ) from exc

        return RocketPyAdapter._run_analytical_placeholder(
            rocket=rocket,
            environment=environment,
            include_time_series=include_time_series,
        )

    @staticmethod
    def _run_analytical_placeholder(rocket: Rocket, environment: Environment, include_time_series: bool) -> dict[str, Any]:
        engine = rocket.engine
        thrust = engine.thrust
        mass = rocket.wet_mass
        burn_time = engine.burn_time or 1
        twr = thrust / (mass * G0)
        net_acceleration = max((thrust / mass) - G0, 0.0)
        burn_velocity = net_acceleration * burn_time
        powered_altitude = 0.5 * net_acceleration * burn_time**2
        coast_altitude = burn_velocity**2 / (2 * G0) if burn_velocity > 0 else 0.0
        apogee = max(powered_altitude + coast_altitude + environment.elevation, environment.elevation)
        relative_apogee = max(apogee - environment.elevation, 0.0)
        flight_duration = burn_time + (2 * sqrt((2 * relative_apogee) / G0) if relative_apogee > 0 else 0.0)
        max_acceleration = net_acceleration
        max_velocity = burn_velocity

        summary = {
            "apogee": round(apogee, 2),
            "max_velocity": round(max_velocity, 2),
            "max_acceleration": round(max_acceleration, 2),
            "flight_duration": round(flight_duration, 2),
        }

        time_series = {"altitude": [], "velocity": [], "acceleration": []}
        if include_time_series:
            steps = 10
            for index in range(steps + 1):
                ratio = index / steps
                t = round(flight_duration * ratio, 2)
                altitude = environment.elevation + max(relative_apogee * (1 - (2 * ratio - 1) ** 2), 0.0)
                velocity = max_velocity * max(1 - ratio, 0.0)
                acceleration = max_acceleration if t <= burn_time else -G0
                time_series["altitude"].append({"time": t, "value": round(altitude, 2)})
                time_series["velocity"].append({"time": t, "value": round(velocity, 2)})
                time_series["acceleration"].append({"time": t, "value": round(acceleration, 2)})

        return {
            "status": "SUCCESS",
            "summary": summary,
            "time_series": time_series,
            "raw_result": {
                "engine": "rocketpy-adapter-prototype",
                "rocketpy_environment": {
                    "latitude": environment.latitude,
                    "longitude": environment.longitude,
                    "elevation": environment.elevation,
                },
                "trajectory_model": "analytical-placeholder",
                "assumption": "RocketPy Environment is initialized; full RocketPy Flight requires motor curve and geometry fields not yet in MVP input.",
                "twr": round(twr, 4),
            },
        }
