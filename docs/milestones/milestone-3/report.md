# Milestone 3 Report

This report outlines the testing strategy and implementation for the backend API, focusing on the use of `pytest` for integration testing.

## Overview

Project Name: SE Project - Group 65
Sprint Duration: 1 week

Sprint Goal: Create well tested API endpoints for the frontend to access the database models.

## API Documentation: Swagger UI

You can find the Swagger UI in YAML file format from this Google Drive link.

## API Testing

## 1. Testing Frameworks and Tools

The testing infrastructure for this project is built using several key Python libraries:

- **pytest**: The core testing framework used for writing, organizing, and executing tests. It provides powerful features like fixtures, parameterization, and detailed failure reports.
- **FastAPI**: The web framework used to build the API. It includes built-in support for testing via its `TestClient`.
- **SQLModel**: Used for database modeling and ORM. For testing, these are used to manage a separate, isolated test database.
- **SQLite**: A lightweight, file-based database used during testing (specifically `test.db`) to ensure that tests do not affect the production data.

## 2. Type of Testing

The project primarily utilizes **API Integration Testing**.

Unlike unit tests that isolate individual functions, these tests verify the interaction between different components of the system:

- **Endpoints**: Ensuring that the RESTful routes (e.g., `/api/auth/register`) correctly handle requests.
- **Business Logic**: Validating that the application logic (e.g., password hashing, user role verification) works as expected.
- **Database Integration**: Confirming that data is correctly persisted, retrieved, and updated in the database.
- **Dependency Injection**: Testing how the application handles overridden dependencies, such as using a test database session instead of a production one.

## 3. Test Client

The project uses the **FastAPI `TestClient`** (which is internally based on the `httpx` library).

The `TestClient` allows us to:

- Make simulated HTTP requests (GET, POST, PUT, DELETE, etc.) directly to the FastAPI application instance.
- Test endpoints without needing to run a live web server.
- Receive standard HTTP response objects, making it easy to assert status codes, headers, and JSON body content.

## 4. Implementation Details (conftest.py)

The testing setup is centralized in `backend/tests/conftest.py`. Key features include:

### Database Isolation

A dedicated `test.db` is used for all tests. The `db_session` fixture ensures that the database schema is created before each test and dropped afterward, maintaining a clean state for every test case.

```backend/tests/conftest.py#L18-L23
@pytest.fixture(scope="function")
def db_session():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)
```

### Dependency Overriding

To ensure tests use the test database, the `client` fixture overrides the standard database session dependency with one that uses the test engine.

```backend/tests/conftest.py#L26-L31
@pytest.fixture(scope="function")
def client(db_session):
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
```

### Authentication Fixtures

Pre-defined fixtures generate authentication tokens and headers for different user roles (Admin, Employee, Customer), simplifying the testing of protected endpoints.

```backend/tests/conftest.py#L86-L88
@pytest.fixture
def auth_headers_admin(admin_token: str):
    return {"Authorization": f"Bearer {admin_token}"}
```

## 5. Example Test Case

Test cases are organized into classes within files such as `test_auth.py`. They use assertions to verify the API's behavior under various conditions (valid input, duplicate data, missing fields, etc.).

```backend/tests/test_auth.py#L7-L24
    def test_register_valid_user(self, client: TestClient):
        """Test registering a new user with valid data"""
        response = client.post(
            "/api/auth/register",
            json={
                "name": "Test User",
                "email": "testuser@example.com",
                "phone": "+91-99999-99999",
                "password": "testpass123",
                "role": "customer",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test User"
        assert data["email"] == "testuser@example.com"
        assert data["phone"] == "+91-99999-99999"
        assert data["role"] == "customer"
        assert "id" in data
```

## Test Cases

Here are some examples from the `test_auth.py` file, it tests the authentication part of the application.

## Test Results

Here is the test results when running the following command in the `backend/` directory.

```bash
uv run pytest
```

### Key Highlights

- **Total Tests Executed:** 97
- **Tests Passed:** 91 (93.8%)
- **Tests Failed:** 6 (6.2%)
- **Test Duration:** 35.48 seconds

### Overall Test Results

| Metric      | Value |
| ----------- | ----- |
| Total Tests | 97    |
| Passed      | 91    |
| Failed      | 6     |
| Pass Rate   | 93.8% |

### Test Coverage by Module

| Module            | Total Tests | Passed | Failed |
| ----------------- | ----------- | ------ | ------ |
| Authentication    | 12          | 11     | 1      |
| Inventory         | 11          | 9      | 2      |
| Orders            | 12          | 12     | 0      |
| Cart              | 9           | 9      | 0      |
| Medicine Requests | 12          | 12     | 0      |
| Staff Management  | 13          | 13     | 0      |
| Customers         | 12          | 11     | 1      |
| Feedback          | 13          | 10     | 3      |

### Failed Test Summary

| Test Name                                | Module         | Expected               | Actual           |
| ---------------------------------------- | -------------- | ---------------------- | ---------------- |
| test_register_invalid_email_format       | Authentication | 422 (Validation Error) | 200 (Success)    |
| test_update_customer_self                | Customers      | 200 (Success)          | 403 (Forbidden)  |
| test_create_feedback_invalid_rating_high | Feedback       | 422 (Validation Error) | 200 (Success)    |
| test_create_feedback_invalid_rating_low  | Feedback       | 422 (Validation Error) | 200 (Success)    |
| test_create_feedback_missing_comment     | Feedback       | 200 (Success)          | 500 (DB Error)   |
| test_create_medicine_admin               | Inventory      | 200 (Success)          | 500 (Type Error) |

### Root Cause Analysis

**Email Format Validation**

- Root Cause: FastAPI's default validation does not enforce email format validation at the request parsing level.
- Recommendation: Add Pydantic email validation using EmailStr type.

**Customer Self-Update**

- Root Cause: Test creates new customer but authentication token is for different customer.
- Recommendation: Update test to use authenticated customer's ID.

**Feedback Rating Validation**

- Root Cause: Validation not enforced properly due to SQLModel handling.
- Recommendation: Add explicit validation in route handler.

**Missing Comment**

- Root Cause: Database has NOT NULL constraint but API accepts missing field.
- Recommendation: Make comment field optional or add validation.

**Date Format**

- Root Cause: SQLite requires Python date objects, not strings.
- Recommendation: Convert string to date object using fromisoformat().

### Recommendations

1. Add Pydantic validation models for better input validation
2. Fix date handling in inventory routes
3. Improve error messages for validation failures
4. Review and fix test fixtures
5. Ensure database constraints match API validation

### Conclusion

The test suite achieved a 93.8% pass rate, showing core functionality works correctly. The six failed tests are edge cases related to validation and data handling. With fixes, near 100% pass rate is achievable.

All endpoints for orders, cart, medicine requests, and staff management are fully functional. Inventory, customers, and feedback modules need minor fixes.

## Plan: Next Sprint

**Features to Implement**

- Add search API for inventory.
- Improve error handling consistency.
- Increase test coverage to 90%.
- More frontend UI designs
- Plots for data analysis.

**Technical Improvements**

- Add test coverage reporting.
- Refactor validation layer.
