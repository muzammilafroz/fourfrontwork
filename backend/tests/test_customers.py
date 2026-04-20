from fastapi.testclient import TestClient


class TestCustomers:
    """Test cases for /api/customers endpoints"""

    def test_get_customers_admin(
        self, client: TestClient, auth_headers_admin, db_session
    ):
        """Test admin can view all customers"""
        from app.models import User, UserRole

        customer = User(
            name="Test Customer",
            email="testcustomer@test.com",
            phone="+91-90000-00020",
            role=UserRole.CUSTOMER,
            hashed_password="hashed",
        )
        db_session.add(customer)
        db_session.commit()

        response = client.get("/api/customers", headers=auth_headers_admin)
        assert response.status_code == 200
        customers = response.json()
        assert len(customers) >= 1

    def test_get_customers_employee(self, client: TestClient, auth_headers_employee):
        """Test employee can view all customers"""
        response = client.get("/api/customers", headers=auth_headers_employee)
        assert response.status_code == 200

    def test_get_customers_customer_forbidden(
        self, client: TestClient, auth_headers_customer
    ):
        """Test customer cannot view all customers"""
        response = client.get("/api/customers", headers=auth_headers_customer)
        assert response.status_code == 403

    def test_get_customers_unauthenticated(self, client: TestClient):
        """Test getting customers without auth fails"""
        response = client.get("/api/customers")
        assert response.status_code == 401

    def test_get_customer_by_id_admin(
        self, client: TestClient, auth_headers_admin, db_session
    ):
        """Test admin can get specific customer by ID"""
        from app.models import User, UserRole

        customer = User(
            name="Specific Customer",
            email="specific@test.com",
            phone="+91-90000-00021",
            role=UserRole.CUSTOMER,
            hashed_password="hashed",
        )
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)

        response = client.get(
            f"/api/customers/{customer.id}", headers=auth_headers_admin
        )
        assert response.status_code == 200
        assert response.json()["email"] == "specific@test.com"

    def test_get_customer_by_id_employee(
        self, client: TestClient, auth_headers_employee, db_session
    ):
        """Test employee can get specific customer by ID"""
        from app.models import User, UserRole

        customer = User(
            name="Employee View Customer",
            email="employeeview@test.com",
            phone="+91-90000-00022",
            role=UserRole.CUSTOMER,
            hashed_password="hashed",
        )
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)

        response = client.get(
            f"/api/customers/{customer.id}", headers=auth_headers_employee
        )
        assert response.status_code == 200

    def test_get_customer_by_id_customer_own(
        self, client: TestClient, auth_headers_customer
    ):
        """Test customer can view their own profile"""
        # Customer ID is 1 based on fixture
        response = client.get("/api/customers/1", headers=auth_headers_customer)
        assert response.status_code == 200

    def test_get_customer_by_id_customer_other_forbidden(
        self, client: TestClient, auth_headers_customer, db_session
    ):
        """Test customer cannot view other customers' profiles"""
        from app.models import User, UserRole

        customer = User(
            name="Other Customer",
            email="other@test.com",
            phone="+91-90000-00023",
            role=UserRole.CUSTOMER,
            hashed_password="hashed",
        )
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)

        response = client.get(
            f"/api/customers/{customer.id}", headers=auth_headers_customer
        )
        assert response.status_code == 403

    def test_get_customer_not_found(self, client: TestClient, auth_headers_admin):
        """Test getting non-existent customer returns 404"""
        response = client.get("/api/customers/99999", headers=auth_headers_admin)
        assert response.status_code == 404

    def test_update_customer_admin(
        self, client: TestClient, auth_headers_admin, db_session
    ):
        """Test admin can update customer"""
        from app.models import User, UserRole

        customer = User(
            name="Original Name",
            email="originalcust@test.com",
            phone="+91-90000-00024",
            role=UserRole.CUSTOMER,
            hashed_password="hashed",
        )
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)

        response = client.put(
            f"/api/customers/{customer.id}",
            headers=auth_headers_admin,
            json={"name": "Updated Name", "phone": "+91-90000-00025"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Name"

    def test_update_customer_other_forbidden(
        self, client: TestClient, auth_headers_customer, db_session
    ):
        """Test customer cannot update other customers"""
        from app.models import User, UserRole

        customer = User(
            name="Other Customer",
            email="othercust@test.com",
            phone="+91-90000-00027",
            role=UserRole.CUSTOMER,
            hashed_password="hashed",
        )
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)

        response = client.put(
            f"/api/customers/{customer.id}",
            headers=auth_headers_customer,
            json={"name": "Hacked Name"},
        )
        assert response.status_code == 403

    def test_update_customer_not_found(self, client: TestClient, auth_headers_admin):
        """Test updating non-existent customer returns 404"""
        response = client.put(
            "/api/customers/99999",
            headers=auth_headers_admin,
            json={"name": "Test"},
        )
        assert response.status_code == 404
