from math import ceil, sqrt

from app.core.constants import G0
from app.core.exceptions import ResourceNotFoundError
from app.schemas.game import (
    GameEnginePreset,
    GameScoreBreakdown,
    GameWeatherPreset,
    LearningFeedback,
    MissionChallenge,
    SandboxRunRequest,
    SandboxRunResult,
)


class GameService:
    ENGINE_PRESETS = [
        GameEnginePreset(
            id="A",
            name="Engine A - Basic Booster",
            description="Low power engine for first 1 km challenge.",
            thrust=6500,
            isp=180,
            burn_time=3.2,
            propellant_mass=12,
            unlock_level=1,
        ),
        GameEnginePreset(
            id="B",
            name="Engine B - Medium Booster",
            description="Balanced classroom engine for 10 km class missions.",
            thrust=18000,
            isp=220,
            burn_time=5.5,
            propellant_mass=42,
            unlock_level=2,
        ),
        GameEnginePreset(
            id="C",
            name="Engine C - Advanced Sustainer",
            description="High efficiency engine for upper atmosphere missions.",
            thrust=52000,
            isp=270,
            burn_time=9,
            propellant_mass=130,
            unlock_level=3,
        ),
        GameEnginePreset(
            id="D",
            name="Engine D - Heavy Lift",
            description="Heavy engine for large payload and high target missions.",
            thrust=120000,
            isp=310,
            burn_time=14,
            propellant_mass=360,
            unlock_level=4,
        ),
    ]

    WEATHER_PRESETS = [
        GameWeatherPreset(
            id="clear",
            name="Clear",
            description="Low wind and stable air. Best for first launches.",
            wind_speed=2,
            turbulence=0.05,
            difficulty_multiplier=1.0,
        ),
        GameWeatherPreset(
            id="cloudy",
            name="Cloudy",
            description="Moderate atmosphere variation with small stability penalty.",
            wind_speed=6,
            turbulence=0.15,
            difficulty_multiplier=1.08,
        ),
        GameWeatherPreset(
            id="windy",
            name="Windy",
            description="Strong crosswind makes fin stability more important.",
            wind_speed=16,
            turbulence=0.35,
            difficulty_multiplier=1.25,
        ),
        GameWeatherPreset(
            id="storm",
            name="Storm",
            description="Extreme wind and turbulence. Very hard to fly safely.",
            wind_speed=28,
            turbulence=0.7,
            difficulty_multiplier=1.55,
        ),
    ]

    CHALLENGES = [
        MissionChallenge(
            id="reach-1km",
            title="Reach 1 Km",
            target_apogee=1000,
            reward="Basic Engine",
            level=1,
            description="Build a stable rocket that reaches 1 km apogee.",
        ),
        MissionChallenge(
            id="reach-10km",
            title="Reach 10 Km",
            target_apogee=10000,
            reward="Medium Engine",
            level=2,
            description="Balance thrust, fuel, payload, and drag to reach 10 km.",
        ),
        MissionChallenge(
            id="reach-50km",
            title="Reach 50 Km",
            target_apogee=50000,
            reward="Advanced Fuel Tank",
            level=3,
            description="Use efficient staging and stable fins for upper atmosphere flight.",
        ),
        MissionChallenge(
            id="reach-100km",
            title="Reach 100 Km",
            target_apogee=100000,
            reward="Large Payload Bay",
            level=4,
            description="Cross the Karman-line class target with advanced choices.",
        ),
    ]

    @staticmethod
    def list_engine_presets() -> list[GameEnginePreset]:
        return GameService.ENGINE_PRESETS

    @staticmethod
    def list_weather_presets() -> list[GameWeatherPreset]:
        return GameService.WEATHER_PRESETS

    @staticmethod
    def list_challenges() -> list[MissionChallenge]:
        return GameService.CHALLENGES

    @staticmethod
    def run_sandbox(payload: SandboxRunRequest) -> SandboxRunResult:
        engine = GameService._engine(payload.engine_preset)
        weather = GameService._weather(payload.weather_preset)
        challenge = GameService._challenge(payload.challenge_id) if payload.challenge_id else None
        target_apogee = challenge.target_apogee if challenge else None

        mass = GameService._mass_model(payload, engine)
        stability = GameService._stability_score(payload, weather)
        trajectory = GameService._trajectory(payload, engine, weather, mass, stability)
        failures = GameService._failures(payload, weather, mass, stability, trajectory, target_apogee)
        mission_success = (not failures) and (target_apogee is None or trajectory["apogee"] >= target_apogee)
        score_breakdown = GameService._score_breakdown(payload, mass, stability, trajectory, target_apogee, mission_success)
        score = GameService._total_score(score_breakdown)
        stars = max(1, min(5, ceil(score / 20))) if score > 0 else 0
        feedback = GameService._feedback(payload, failures, stability, trajectory, target_apogee, mission_success)

        return SandboxRunResult(
            mode=payload.mode,
            mission_success=mission_success,
            mission_status="SUCCESS" if mission_success else "FAILED",
            score=score,
            stars=stars,
            score_breakdown=score_breakdown,
            failures=failures,
            learning_feedback=feedback,
            summary={
                "apogee": round(trajectory["apogee"], 2),
                "max_velocity": round(trajectory["max_velocity"], 2),
                "max_acceleration": round(trajectory["max_acceleration"], 2),
                "flight_duration": round(trajectory["flight_duration"], 2),
                "target_apogee": target_apogee,
                "twr": round(trajectory["twr"], 3),
                "stability": round(stability, 2),
                "fuel_efficiency": round(trajectory["fuel_efficiency"], 2),
            },
            selected_configuration={
                "engine": engine.model_dump(),
                "weather": weather.model_dump(),
                "challenge": challenge.model_dump() if challenge else None,
                "rocket": {
                    "height": payload.rocket_height,
                    "diameter": payload.rocket_diameter,
                    "nose_cone": payload.nose_cone,
                    "fin_size": payload.fin_size,
                    "payload_mass": payload.payload_mass,
                    "fuel_stages": payload.fuel_stages,
                    "wet_mass": round(mass["wet_mass"], 2),
                    "dry_mass": round(mass["dry_mass"], 2),
                    "propellant_mass": round(mass["propellant_mass"], 2),
                },
            },
        )

    @staticmethod
    def _engine(engine_id: str) -> GameEnginePreset:
        for engine in GameService.ENGINE_PRESETS:
            if engine.id == engine_id:
                return engine
        raise ResourceNotFoundError("Engine preset not found")

    @staticmethod
    def _weather(weather_id: str) -> GameWeatherPreset:
        for weather in GameService.WEATHER_PRESETS:
            if weather.id == weather_id:
                return weather
        raise ResourceNotFoundError("Weather preset not found")

    @staticmethod
    def _challenge(challenge_id: str | None) -> MissionChallenge:
        for challenge in GameService.CHALLENGES:
            if challenge.id == challenge_id:
                return challenge
        raise ResourceNotFoundError("Mission challenge not found")

    @staticmethod
    def _mass_model(payload: SandboxRunRequest, engine: GameEnginePreset) -> dict:
        fin_mass = {"small": 2, "medium": 5, "large": 9}[payload.fin_size]
        nose_mass = {"short": 1.5, "medium": 2.5, "sharp": 4}[payload.nose_cone]
        stage_count = {"single": 1, "two": 2, "three": 3}[payload.fuel_stages]
        structure_mass = 8 + payload.rocket_height * 1.6 + payload.rocket_diameter * 9 + fin_mass + nose_mass
        propellant_mass = engine.propellant_mass * (0.9 + stage_count * 0.55)
        dry_mass = structure_mass + payload.payload_mass
        wet_mass = dry_mass + propellant_mass
        return {"dry_mass": dry_mass, "wet_mass": wet_mass, "propellant_mass": propellant_mass, "stage_count": stage_count}

    @staticmethod
    def _stability_score(payload: SandboxRunRequest, weather: GameWeatherPreset) -> float:
        fin_score = {"small": 35, "medium": 58, "large": 78}[payload.fin_size]
        nose_score = {"short": -4, "medium": 5, "sharp": 10}[payload.nose_cone]
        slenderness = payload.rocket_height / payload.rocket_diameter
        slenderness_penalty = max(0, (slenderness - 18) * 1.3)
        wind_penalty = weather.wind_speed * 1.1 + weather.turbulence * 18
        return max(0, min(100, fin_score + nose_score + payload.rocket_diameter * 2 - slenderness_penalty - wind_penalty))

    @staticmethod
    def _trajectory(
        payload: SandboxRunRequest,
        engine: GameEnginePreset,
        weather: GameWeatherPreset,
        mass: dict,
        stability: float,
    ) -> dict:
        stage_count = mass["stage_count"]
        stage_efficiency = {1: 1.0, 2: 1.38, 3: 1.72}[stage_count]
        nose_drag = {"short": 1.18, "medium": 1.0, "sharp": 0.88}[payload.nose_cone]
        fin_drag = {"small": 0.95, "medium": 1.0, "large": 1.12}[payload.fin_size]
        frontal_area = payload.rocket_diameter**2
        drag_factor = max(0.42, 1 - frontal_area * 0.028 * nose_drag * fin_drag)
        weather_factor = 1 / weather.difficulty_multiplier
        stability_factor = max(0.45, stability / 100)
        burn_time = engine.burn_time * (0.85 + stage_count * 0.18)
        twr = engine.thrust / (mass["wet_mass"] * G0)
        net_acceleration = max(engine.thrust / mass["wet_mass"] - G0, 0)
        burnout_velocity = net_acceleration * burn_time * drag_factor * stability_factor
        powered_altitude = 0.5 * net_acceleration * burn_time**2
        coast_altitude = burnout_velocity**2 / (2 * G0) if burnout_velocity > 0 else 0
        apogee = (powered_altitude + coast_altitude) * stage_efficiency * weather_factor
        flight_duration = burn_time + (2 * sqrt((2 * max(apogee, 0)) / G0) if apogee > 0 else 0)
        fuel_efficiency = apogee / max(mass["propellant_mass"], 1)
        return {
            "apogee": max(apogee, 0),
            "max_velocity": max(burnout_velocity, 0),
            "max_acceleration": max(net_acceleration, 0),
            "flight_duration": max(flight_duration, 0),
            "fuel_efficiency": fuel_efficiency,
            "twr": twr,
        }

    @staticmethod
    def _failures(
        payload: SandboxRunRequest,
        weather: GameWeatherPreset,
        mass: dict,
        stability: float,
        trajectory: dict,
        target_apogee: float | None,
    ) -> list[str]:
        failures = []
        if trajectory["twr"] <= 1:
            failures.append("ROCKET_TOO_HEAVY")
        if target_apogee is not None and trajectory["apogee"] < target_apogee:
            failures.append("FUEL_EXHAUSTED_BEFORE_TARGET")
        if stability < 45:
            failures.append("UNSTABLE_FLIGHT")
        if weather.id in {"windy", "storm"} and stability < 65:
            failures.append("STRONG_WIND")
        if trajectory["max_acceleration"] > 140 and payload.rocket_height / payload.rocket_diameter > 18:
            failures.append("STRUCTURAL_FAILURE")
        if payload.fuel_stages in {"two", "three"} and stability < 52:
            failures.append("STAGE_SEPARATION_FAILURE")
        if payload.payload_mass > mass["dry_mass"] * 0.35:
            failures.append("PAYLOAD_FAILURE")
        return failures

    @staticmethod
    def _score_breakdown(
        payload: SandboxRunRequest,
        mass: dict,
        stability: float,
        trajectory: dict,
        target_apogee: float | None,
        mission_success: bool,
    ) -> GameScoreBreakdown:
        success_score = 100 if mission_success else (min(100, trajectory["apogee"] / target_apogee * 100) if target_apogee else 65)
        efficiency_score = min(100, trajectory["fuel_efficiency"] / 220 * 100)
        payload_score = min(100, payload.payload_mass / max(mass["dry_mass"], 1) * 380)
        stability_score = stability
        return GameScoreBreakdown(
            mission_success=round(success_score, 2),
            fuel_efficiency=round(efficiency_score, 2),
            payload_delivery=round(payload_score, 2),
            stability=round(stability_score, 2),
        )

    @staticmethod
    def _total_score(score: GameScoreBreakdown) -> int:
        total = (
            score.mission_success * 0.4
            + score.fuel_efficiency * 0.25
            + score.payload_delivery * 0.2
            + score.stability * 0.15
        )
        return int(round(max(0, min(100, total))))

    @staticmethod
    def _feedback(
        payload: SandboxRunRequest,
        failures: list[str],
        stability: float,
        trajectory: dict,
        target_apogee: float | None,
        mission_success: bool,
    ) -> LearningFeedback:
        suggestions = []
        if "ROCKET_TOO_HEAVY" in failures:
            suggestions.append("Use a stronger engine preset or reduce payload mass.")
        if "FUEL_EXHAUSTED_BEFORE_TARGET" in failures:
            suggestions.append("Try a higher engine preset, more stages, or reduce drag.")
        if "UNSTABLE_FLIGHT" in failures:
            suggestions.append("Increase fin size or reduce rocket height-to-diameter ratio.")
        if "STRONG_WIND" in failures:
            suggestions.append("Use clear weather first, then test windy conditions after improving stability.")
        if "STRUCTURAL_FAILURE" in failures:
            suggestions.append("Reduce acceleration by choosing a less aggressive engine or wider rocket body.")
        if "PAYLOAD_FAILURE" in failures:
            suggestions.append("Payload is too large for this design; reduce payload or increase rocket capacity.")
        if not suggestions:
            if mission_success:
                suggestions.append("Try increasing payload or using less fuel while still reaching the target.")
            elif target_apogee:
                suggestions.append("You are close. Improve fuel efficiency or stability to reach the target.")
            else:
                suggestions.append("Sandbox run completed. Change one parameter at a time to observe cause and effect.")

        title = "Mission Complete" if mission_success else "Design Needs Improvement"
        message = (
            f"Apogee reached {trajectory['apogee']:.0f} m with stability {stability:.0f}/100."
            if payload.mode == "challenge"
            else "Sandbox result generated. No target is required in sandbox mode."
        )
        return LearningFeedback(title=title, message=message, suggestions=suggestions)
