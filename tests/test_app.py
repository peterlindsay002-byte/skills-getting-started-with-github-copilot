import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    """Test retrieving all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # We have 9 activities
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert "description" in data["Chess Club"]

def test_signup_successful():
    """Test successful signup for an activity"""
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "test@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]

    # Verify the participant was added
    response = client.get("/activities")
    activities = response.json()
    assert "test@mergington.edu" in activities["Chess Club"]["participants"]

def test_signup_duplicate():
    """Test preventing duplicate signup"""
    # First signup
    client.post("/activities/Soccer%20Team/signup?email=duplicate@mergington.edu")
    
    # Second signup should fail
    response = client.post("/activities/Soccer%20Team/signup?email=duplicate@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]

def test_signup_nonexistent_activity():
    """Test signup for non-existent activity"""
    response = client.post("/activities/NonExistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]

def test_unregister_successful():
    """Test successful unregister from an activity"""
    # First signup
    client.post("/activities/Basketball%20Club/signup?email=unregister@mergington.edu")
    
    # Then unregister
    response = client.delete("/activities/Basketball%20Club/signup?email=unregister@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"]

    # Verify the participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert "unregister@mergington.edu" not in activities["Basketball Club"]["participants"]

def test_unregister_not_signed_up():
    """Test unregister when not signed up"""
    response = client.delete("/activities/Gym%20Class/signup?email=notsigned@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"]

def test_unregister_nonexistent_activity():
    """Test unregister from non-existent activity"""
    response = client.delete("/activities/NonExistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]