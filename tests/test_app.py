from urllib.parse import quote

from src.app import activities


def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant(client):
    email = "teststudent@mergington.edu"
    activity_name = "Chess Club"
    encoded_activity = quote(activity_name, safe="")

    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    updated = client.get("/activities").json()
    assert email in updated[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]
    encoded_activity = quote(activity_name, safe="")

    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_nonexistent_activity_returns_404(client):
    response = client.post("/activities/Nonexistent%20Club/signup", params={"email": "claire@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
