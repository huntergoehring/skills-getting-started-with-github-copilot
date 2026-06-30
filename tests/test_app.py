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
