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


def test_mission_engine_rocket_simulation_e2e(client):
    mission = create_mission(client)
    engine = create_engine(client)
    rocket = create_rocket(client, mission["id"], engine["id"])
    simulation = run_simulation(client, mission["id"], rocket["id"])

    assert simulation["status"] == "SUCCESS"
    assert simulation["summary"]["apogee"] > 0
    assert len(simulation["time_series"]["altitude"]) > 0

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
