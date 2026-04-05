from fastapi.testclient import TestClient


class TestAuthRegister:
    """Test cases for /api/auth/register endpoint"""

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

    def test_register_duplicate_email(self, client: TestClient, customer_user):
        """Test registering with existing email fails"""
        response = client.post(
            "/api/auth/register",
            json={
                "name": "Another User",
                "email": "customer@test.com",
                "phone": "+91-88888-88888",
                "password": "password123",
                "role": "customer",
            },
        )
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_register_missing_name(self, client: TestClient):
        """Test registering without name fails"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "noname@example.com",
                "phone": "+91-88888-88888",
                "password": "password123",
                "role": "customer",
            },
        )
        assert response.status_code == 422

    def test_register_missing_email(self, client: TestClient):
        """Test registering without email fails"""
        response = client.post(
            "/api/auth/register",
            json={
                "name": "Test User",
                "phone": "+91-88888-88888",
                "password": "password123",
                "role": "customer",
            },
        )
        assert response.status_code == 422

    def test_register_invalid_email_format(self, client: TestClient):
        """Test registering with invalid email format fails"""
        response = client.post(
            "/api/auth/register",
            json={
                "name": "Test User",
                "email": "not-an-email",
                "phone": "+91-88888-88888",
                "password": "password123",
                "role": "customer",
            },
        )
        assert response.status_code == 422


class TestAuthLogin:
    """Test cases for /api/auth/login endpoint"""

    def test_login_valid_credentials(self, client: TestClient, customer_user):
        """Test login with valid credentials returns token"""
        response = client.post(
            "/api/auth/login",
            data={"username": "customer@test.com", "password": "customer123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == "customer@test.com"

    def test_login_invalid_password(self, client: TestClient, customer_user):
        """Test login with wrong password fails"""
        response = client.post(
            "/api/auth/login",
            data={"username": "customer@test.com", "password": "wrongpassword"},
        )
        assert response.status_code == 400
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_nonexistent_user(self, client: TestClient):
        """Test login with non-existent user fails"""
        response = client.post(
            "/api/auth/login",
            data={"username": "nonexistent@test.com", "password": "password123"},
        )
        assert response.status_code == 400

    def test_login_missing_username(self, client: TestClient):
        """Test login without username fails"""
        response = client.post(
            "/api/auth/login",
            data={"password": "password123"},
        )
        assert response.status_code == 422

    def test_login_missing_password(self, client: TestClient):
        """Test login without password fails"""
        response = client.post(
            "/api/auth/login",
            data={"username": "test@test.com"},
        )
        assert response.status_code == 422
