from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def restore_activities():
    original_state = deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original_state)


def test_get_activities_returns_activity_catalog(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert expected_activity in payload
    assert payload[expected_activity]["max_participants"] == 12


def test_signup_adds_participant_to_activity(client):
    # Arrange
    email = "new.student@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in app_module.activities["Chess Club"]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    duplicate_email = "michael@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": duplicate_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_email(client):
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


def test_unknown_activity_returns_404(client):
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
