import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    original_state = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_state)


def test_unregister_participant_removes_them_from_activity():
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert unregister_response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert unregister_response.json()["message"] == f"Unregistered {email} from {activity_name}"


def test_signup_rejects_duplicate_participant():
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_fails_for_unknown_activity():
    client = TestClient(app)

    response = client.post("/activities/Unknown Activity/signup?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_fails_for_non_participant():
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
