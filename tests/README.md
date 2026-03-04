# Tests Directory

This directory contains comprehensive tests for the Mergington High School API backend.

## Test Structure

- `test_app.py` - Main test file containing all API endpoint tests
- `__init__.py` - Package initialization

## Testing Pattern

All tests follow the **AAA (Arrange-Act-Assert)** pattern for clarity and maintainability:

- **Arrange**: Set up test data and preconditions
- **Act**: Execute the code being tested
- **Assert**: Verify the expected outcomes

Example:
```python
def test_signup_successful(self, client):
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
```

## Test Coverage

The tests cover:

### Endpoints Tested
- `GET /` - Root redirect
- `GET /activities` - Get all activities
- `POST /activities/{activity}/signup` - Student signup
- `POST /activities/{activity}/unregister` - Student unregister

### Test Categories
- **Root Endpoint Tests** - Verify redirect behavior
- **Activities Endpoint Tests** - Test data retrieval and structure
- **Signup Endpoint Tests** - Test registration functionality
- **Unregister Endpoint Tests** - Test deregistration functionality
- **Data Integrity Tests** - Verify data consistency after operations
- **URL Handling Tests** - Test special characters and encoding

## Running Tests

### Prerequisites
Make sure you have installed the test dependencies:
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest tests/
```

### Run with Verbose Output
```bash
pytest tests/ -v
```

### Run Specific Test Class
```bash
pytest tests/test_app.py::TestSignupEndpoint -v
```

### Run Specific Test Method
```bash
pytest tests/test_app.py::TestSignupEndpoint::test_signup_successful -v
```

## Test Configuration

Tests are configured via `pytest.ini` in the project root:
- Test discovery in `tests/` directory
- Verbose output by default
- Short traceback format

## Test Fixtures

- `client` - FastAPI TestClient instance
- `sample_activities` - Sample activity data for testing

## Adding New Tests

When adding new tests:

1. Add test methods to appropriate test classes in `test_app.py`
2. Follow naming convention: `test_descriptive_name`
3. Use descriptive docstrings
4. Test both success and error cases
5. Verify data integrity after operations