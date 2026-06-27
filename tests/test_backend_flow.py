def assert_success(response, status_code=200):
    assert response.status_code == status_code
    payload = response.json()
    assert payload["success"] is True
    return payload


def create_mission(client, name="Test Mission"):
    return assert_success(
        client.post("/api/v1/missions", json={"name": name, "description": "Backend test mission"}),
        201,
    )["data"]


def create_engine(client, name="Test Engine"):
    return assert_success(
        client.post(
            "/api/v1/engines",
            json={
                "name": name,
                "thrust": 5000,
                "isp": 210,
                "burn_time": 4.5,
                "propellant_mass": 12.5,
                "motor_curve": [
                    {"time": 0, "thrust": 0},
                    {"time": 0.5, "thrust": 4500},
                    {"time": 2.5, "thrust": 5200},
                    {"time": 4.5, "thrust": 0},
                ],
                "nozzle_radius": 0.035,
                "throat_radius": 0.012,
            },
        ),
        201,
    )["data"]


def create_rocket(client, mission_id, engine_id, name="Test Rocket", wet_mass=50):
    return assert_success(
        client.post(
            f"/api/v1/missions/{mission_id}/rockets",
            json={
                "name": name,
                "wet_mass": wet_mass,
                "dry_mass": 30,
                "payload_mass": 5,
                "engine_id": engine_id,
                "diameter": 0.18,
                "length": 1.8,
                "drag_coefficient": 0.75,
                "center_of_mass_position": 0.9,
                "motor_position": 1.4,
                "nose_length": 0.35,
                "nose_kind": "vonKarman",
                "fin_count": 4,
                "fin_root_chord": 0.22,
                "fin_tip_chord": 0.1,
                "fin_span": 0.12,
                "fin_position": 1.55,
            },
        ),
        201,
    )["data"]


def run_simulation(client, mission_id, rocket_id):
    return assert_success(
        client.post(
            "/api/v1/simulations/run",
            json={
                "mission_id": mission_id,
                "rocket_id": rocket_id,
                "environment": {
                    "latitude": -6.2,
                    "longitude": 106.8,
                    "elevation": 12,
                    "date": "2026-06-27",
                },
                "options": {"store_result": True, "include_time_series": True},
            },
        )
    )["data"]


def test_health_and_dashboard_empty(client):
    health = assert_success(client.get("/api/v1/health"))
    assert health["data"]["status"] == "healthy"

    dashboard = assert_success(client.get("/api/v1/dashboard/summary"))
    assert dashboard["data"]["total_missions"] == 0
    assert dashboard["data"]["best_apogee"]["value"] is None


def test_cors_preflight_for_frontend(client):
    response = client.options(
        "/api/v1/dashboard/summary",
        headers={
            "Origin": "http://127.0.0.1:3000",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:3000"


def test_mission_search_for_frontend(client):
    create_mission(client, name="Alpha Search Mission")
    create_mission(client, name="Beta Flight")

    result = assert_success(client.get("/api/v1/missions?page=1&limit=10&search=Alpha"))

    assert result["meta"]["total"] == 1
    assert result["data"][0]["name"] == "Alpha Search Mission"


def test_mission_engine_rocket_simulation_e2e(client):
    mission = create_mission(client)
    engine = create_engine(client)
    rocket = create_rocket(client, mission["id"], engine["id"])
    simulation = run_simulation(client, mission["id"], rocket["id"])

    assert simulation["status"] == "SUCCESS"
    assert simulation["summary"]["apogee"] > 0
    assert len(simulation["time_series"]["altitude"]) > 0
    assert simulation["raw_result"]["thrust_profile"]["source"] == "motor_curve"
    assert simulation["raw_result"]["geometry"]["fin_count"] == 4

    detail = assert_success(client.get(f"/api/v1/simulations/{simulation['id']}"))
    assert detail["data"]["id"] == simulation["id"]

    dashboard = assert_success(client.get("/api/v1/dashboard/summary"))
    assert dashboard["data"]["total_missions"] == 1
    assert dashboard["data"]["total_engines"] == 1
    assert dashboard["data"]["total_rockets"] == 1
    assert dashboard["data"]["total_simulations"] == 1
    assert dashboard["data"]["best_apogee"]["simulation_id"] == simulation["id"]


def test_calculator_result_storage(client):
    mission = create_mission(client)
    engine = create_engine(client)
    rocket = create_rocket(client, mission["id"], engine["id"])

    result = assert_success(
        client.post(
            "/api/v1/calculators/delta-v",
            json={
                "isp": 210,
                "wet_mass": 50,
                "dry_mass": 30,
                "mission_id": mission["id"],
                "rocket_id": rocket["id"],
                "store_result": True,
            },
        )
    )["data"]

    assert "stored_result_id" in result

    history = assert_success(client.get(f"/api/v1/calculators/results?mission_id={mission['id']}"))
    assert len(history["data"]) == 1
    assert history["data"][0]["id"] == result["stored_result_id"]


def test_simulation_comparison(client):
    mission = create_mission(client)
    engine = create_engine(client)
    rocket_a = create_rocket(client, mission["id"], engine["id"], name="Rocket A", wet_mass=50)
    rocket_b = create_rocket(client, mission["id"], engine["id"], name="Rocket B", wet_mass=45)
    simulation_a = run_simulation(client, mission["id"], rocket_a["id"])
    simulation_b = run_simulation(client, mission["id"], rocket_b["id"])

    comparison = assert_success(
        client.post(
            "/api/v1/simulations/compare",
            json={"simulation_ids": [simulation_a["id"], simulation_b["id"]]},
        )
    )["data"]

    assert len(comparison["items"]) == 2
    assert comparison["best_result"]["highest_apogee_simulation_id"] in {
        simulation_a["id"],
        simulation_b["id"],
    }
    assert len(comparison["differences"]) == 1


def test_business_rule_errors(client):
    mission = create_mission(client)
    engine = create_engine(client)

    bad_rocket = client.post(
        f"/api/v1/missions/{mission['id']}/rockets",
        json={
            "name": "Bad Rocket",
            "wet_mass": 50,
            "dry_mass": 30,
            "payload_mass": 31,
            "engine_id": engine["id"],
        },
    )
    assert bad_rocket.status_code == 400
    assert bad_rocket.json()["error"]["code"] == "BUSINESS_RULE_ERROR"

    invalid_uuid = client.post(
        "/api/v1/simulations/run",
        json={"mission_id": "bad", "rocket_id": "bad"},
    )
    assert invalid_uuid.status_code == 422
    assert invalid_uuid.json()["error"]["code"] == "VALIDATION_ERROR"


def test_game_education_presets_and_sandbox(client):
    challenges = assert_success(client.get("/api/v1/game/challenges"))["data"]
    engines = assert_success(client.get("/api/v1/game/engine-presets"))["data"]
    weather = assert_success(client.get("/api/v1/game/weather-presets"))["data"]

    assert len(challenges) >= 4
    assert [engine["id"] for engine in engines] == ["A", "B", "C", "D"]
    assert {item["id"] for item in weather} == {"clear", "cloudy", "windy", "storm"}

    result = assert_success(
        client.post(
            "/api/v1/game/sandbox/run",
            json={
                "mode": "challenge",
                "challenge_id": "reach-1km",
                "rocket_height": 12,
                "rocket_diameter": 0.8,
                "nose_cone": "medium",
                "fin_size": "medium",
                "payload_mass": 10,
                "engine_preset": "B",
                "fuel_stages": "single",
                "weather_preset": "clear",
            },
        )
    )["data"]

    assert result["summary"]["apogee"] > 0
    assert 0 <= result["score"] <= 100
    assert 0 <= result["stars"] <= 5
    assert "learning_feedback" in result
    assert "selected_configuration" in result


def test_game_failure_feedback(client):
    result = assert_success(
        client.post(
            "/api/v1/game/sandbox/run",
            json={
                "mode": "challenge",
                "challenge_id": "reach-10km",
                "rocket_height": 50,
                "rocket_diameter": 0.5,
                "nose_cone": "short",
                "fin_size": "small",
                "payload_mass": 100,
                "engine_preset": "A",
                "fuel_stages": "single",
                "weather_preset": "storm",
            },
        )
    )["data"]

    assert result["mission_success"] is False
    assert len(result["failures"]) > 0
    assert len(result["learning_feedback"]["suggestions"]) > 0
