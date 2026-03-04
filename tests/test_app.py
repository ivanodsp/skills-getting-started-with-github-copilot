"""
Tests for Mergington High School API
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """Sample activities data for testing"""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        }
    }


class TestRootEndpoint:
    """Test the root endpoint"""

    def test_root_redirect(self, client):
        """Test that root redirects to static/index.html"""
        # Arrange - No special setup needed

        # Act - Make request to root endpoint
        response = client.get("/")

        # Assert - Verify redirect behavior
        assert response.status_code == 200
        assert str(response.url).endswith("/static/index.html")


class TestActivitiesEndpoint:
    """Test the activities endpoints"""

    def test_get_activities(self, client, sample_activities):
        """Test getting all activities"""
        # Arrange - No special setup needed

        # Act - Request all activities
        response = client.get("/activities")

        # Assert - Verify response structure and data
        assert response.status_code == 200
        data = response.json()

        # Check that we get a dictionary
        assert isinstance(data, dict)

        # Check that activities have the expected structure
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_has_expected_activities(self, client):
        """Test that expected activities are present"""
        # Arrange - Define expected activities
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
            "Tennis Club", "Art Studio", "Drama Club", "Debate Team", "Music Theory Club"
        ]

        # Act - Request all activities
        response = client.get("/activities")

        # Assert - Verify all expected activities are present
        assert response.status_code == 200
        data = response.json()

        for activity in expected_activities:
            assert activity in data


class TestSignupEndpoint:
    """Test the signup functionality"""

    def test_signup_successful(self, client):
        """Test successful signup"""
        # Arrange - Set up test data
        email = "test@mergington.edu"
        activity = "Chess Club"

        # Act - Attempt to sign up for activity
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert - Verify successful signup
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_signup_activity_not_found(self, client):
        """Test signup with non-existent activity"""
        # Arrange - Set up test data with invalid activity
        email = "test@mergington.edu"
        activity = "NonExistent Activity"

        # Act - Attempt to sign up for non-existent activity
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert - Verify error response
        assert response.status_code == 404

        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_participant(self, client):
        """Test signup when student is already registered"""
        # Arrange - Use email that's already registered
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"

        # Act - Attempt to sign up again
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert - Verify duplicate signup is rejected
        assert response.status_code == 400

        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]

    def test_signup_with_special_characters(self, client):
        """Test signup with email containing special characters"""
        # Arrange - Set up email with special characters
        email = "test.user+tag@mergington.edu"
        activity = "Programming Class"

        # Act - Attempt to sign up with special character email
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert - Verify successful signup with special characters
        assert response.status_code == 200

        data = response.json()
        assert "message" in data


class TestUnregisterEndpoint:
    """Test the unregister functionality"""

    def test_unregister_successful(self, client):
        """Test successful unregister"""
        # Arrange - Use email that's already registered
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"

        # Act - Attempt to unregister from activity
        response = client.post(f"/activities/{activity}/unregister?email={email}")

        # Assert - Verify successful unregister
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_unregister_activity_not_found(self, client):
        """Test unregister with non-existent activity"""
        # Arrange - Set up test data with invalid activity
        email = "test@mergington.edu"
        activity = "NonExistent Activity"

        # Act - Attempt to unregister from non-existent activity
        response = client.post(f"/activities/{activity}/unregister?email={email}")

        # Assert - Verify error response
        assert response.status_code == 404

        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_participant_not_found(self, client):
        """Test unregister when student is not registered"""
        # Arrange - Use email that's not registered for this activity
        email = "notregistered@mergington.edu"
        activity = "Chess Club"

        # Act - Attempt to unregister non-registered student
        response = client.post(f"/activities/{activity}/unregister?email={email}")

        # Assert - Verify error response
        assert response.status_code == 404

        data = response.json()
        assert "detail" in data
        assert "Student not found" in data["detail"]


class TestActivityDataIntegrity:
    """Test that activity data remains consistent"""

    def test_participants_list_updated_after_signup(self, client):
        """Test that participants list is updated after signup"""
        # Arrange - Set up test data and get initial state
        email = "newstudent@mergington.edu"
        activity = "Tennis Club"

        # Get initial participants
        response = client.get("/activities")
        initial_data = response.json()
        initial_participants = initial_data[activity]["participants"].copy()

        # Act - Sign up new student
        client.post(f"/activities/{activity}/signup?email={email}")

        # Assert - Verify participants list was updated
        # Check participants again
        response = client.get("/activities")
        updated_data = response.json()
        updated_participants = updated_data[activity]["participants"]

        assert email in updated_participants
        assert len(updated_participants) == len(initial_participants) + 1

    def test_participants_list_updated_after_unregister(self, client):
        """Test that participants list is updated after unregister"""
        # Arrange - Set up test data and get initial state
        email = "alex@mergington.edu"  # Already in Tennis Club
        activity = "Tennis Club"

        # Get initial participants
        response = client.get("/activities")
        initial_data = response.json()
        initial_participants = initial_data[activity]["participants"].copy()

        # Act - Unregister existing student
        client.post(f"/activities/{activity}/unregister?email={email}")

        # Assert - Verify participants list was updated
        # Check participants again
        response = client.get("/activities")
        updated_data = response.json()
        updated_participants = updated_data[activity]["participants"]

        assert email not in updated_participants
        assert len(updated_participants) == len(initial_participants) - 1


class TestURLHandling:
    """Test URL encoding and special characters"""

    def test_activity_name_with_spaces(self, client):
        """Test handling activity names with spaces"""
        # Arrange - Set up test data with activity name containing spaces
        email = "test@mergington.edu"
        activity = "Programming Class"  # Has space

        # Act - Attempt to sign up for activity with spaces in name
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert - Verify successful handling of spaces in URL
        assert response.status_code == 200

    def test_email_with_special_chars_url_encoded(self, client):
        """Test emails with special characters are handled properly"""
        # Arrange - Set up email with special characters that need URL encoding
        email = "test@example.com"
        activity = "Art Studio"

        # URL encode the @ symbol
        encoded_email = "test%40example.com"

        # Act - Attempt to sign up with URL-encoded email
        response = client.post(f"/activities/{activity}/signup?email={encoded_email}")

        # Assert - Verify successful handling of URL-encoded characters
        assert response.status_code == 200