from math import pi, sqrt
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
                date=RocketPyAdapter._rocketpy_date(environment_input.date),
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
    def _rocketpy_date(value: Any) -> tuple[int, int, int, int] | None:
        if value is None:
            return None
        return (value.year, value.month, value.day, 0)

    @staticmethod
    def _run_analytical_placeholder(rocket: Rocket, environment: Environment, include_time_series: bool) -> dict[str, Any]:
        engine = rocket.engine
        thrust_profile = RocketPyAdapter._resolve_thrust_profile(engine)
        thrust = thrust_profile["average_thrust"]
        max_thrust = thrust_profile["max_thrust"]
        mass = rocket.wet_mass
        burn_time = thrust_profile["burn_time"]
        twr = max_thrust / (mass * G0)
        net_acceleration = max((thrust / mass) - G0, 0.0)
        burn_velocity = net_acceleration * burn_time
        powered_altitude = 0.5 * net_acceleration * burn_time**2
        drag_loss_factor = RocketPyAdapter._drag_loss_factor(rocket)
        coast_altitude = (burn_velocity**2 / (2 * G0)) * drag_loss_factor if burn_velocity > 0 else 0.0
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
                "assumption": "RocketPy Environment is initialized; motor curve and geometry fields are captured for full RocketPy Flight wiring.",
                "thrust_profile": thrust_profile,
                "geometry": RocketPyAdapter._geometry_snapshot(rocket),
                "twr": round(twr, 4),
            },
        }

    @staticmethod
    def _resolve_thrust_profile(engine: Any) -> dict[str, Any]:
        curve = engine.motor_curve or []
        if len(curve) >= 2:
            points = sorted(
                [{"time": float(point["time"]), "thrust": float(point["thrust"])} for point in curve],
                key=lambda point: point["time"],
            )
            total_impulse = 0.0
            for left, right in zip(points, points[1:]):
                duration = right["time"] - left["time"]
                total_impulse += ((left["thrust"] + right["thrust"]) / 2) * duration
            burn_time = max(points[-1]["time"] - points[0]["time"], 0.001)
            return {
                "source": "motor_curve",
                "burn_time": round(burn_time, 4),
                "average_thrust": round(total_impulse / burn_time, 4),
                "max_thrust": round(max(point["thrust"] for point in points), 4),
                "total_impulse": round(total_impulse, 4),
                "points": points,
            }

        burn_time = engine.burn_time or 1
        total_impulse = engine.thrust * burn_time
        return {
            "source": "constant_thrust",
            "burn_time": round(burn_time, 4),
            "average_thrust": round(engine.thrust, 4),
            "max_thrust": round(engine.thrust, 4),
            "total_impulse": round(total_impulse, 4),
            "points": [
                {"time": 0.0, "thrust": round(engine.thrust, 4)},
                {"time": round(burn_time, 4), "thrust": round(engine.thrust, 4)},
            ],
        }

    @staticmethod
    def _drag_loss_factor(rocket: Rocket) -> float:
        if not rocket.diameter or not rocket.drag_coefficient:
            return 1.0

        reference_area = pi * (rocket.diameter / 2) ** 2
        drag_index = rocket.drag_coefficient * reference_area
        return max(0.55, min(1.0, 1 - drag_index * 0.08))

    @staticmethod
    def _geometry_snapshot(rocket: Rocket) -> dict[str, Any]:
        return {
            "diameter": rocket.diameter,
            "length": rocket.length,
            "drag_coefficient": rocket.drag_coefficient,
            "center_of_mass_position": rocket.center_of_mass_position,
            "motor_position": rocket.motor_position,
            "nose_length": rocket.nose_length,
            "nose_kind": rocket.nose_kind,
            "fin_count": rocket.fin_count,
            "fin_root_chord": rocket.fin_root_chord,
            "fin_tip_chord": rocket.fin_tip_chord,
            "fin_span": rocket.fin_span,
            "fin_position": rocket.fin_position,
        }
