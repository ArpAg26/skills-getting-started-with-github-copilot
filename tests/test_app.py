from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture
def restore_chess_participants():
    original_participants = deepcopy(app_module.activities["Chess Club"]["participants"])
    yield
    app_module.activities["Chess Club"]["participants"] = original_participants


def test_unregister_participant_removes_email_from_activity(client, restore_chess_participants):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email not in app_module.activities["Chess Club"]["participants"]
    assert response.json()["message"] == f"Removed {email} from Chess Club"
