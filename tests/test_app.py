from fastapi.testclient import TestClient

from src import app as app_module


def test_unregister_participant_removes_email_from_activity():
    client = TestClient(app_module.app)
    original_participants = list(app_module.activities["Chess Club"]["participants"])

    try:
        response = client.delete(
            "/activities/Chess Club/participants",
            params={"email": "michael@mergington.edu"},
        )

        assert response.status_code == 200
        assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]
        assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
    finally:
        app_module.activities["Chess Club"]["participants"] = original_participants
