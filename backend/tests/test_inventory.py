from datetime import date

from fastapi.testclient import TestClient


class TestInventory:
    """Test cases for /api/inventory endpoints"""

    def test_get_inventory_authenticated(self, client: TestClient, auth_headers_admin):
        """Test getting inventory list with authentication"""
        response = client.get("/api/inventory", headers=auth_headers_admin)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_inventory_unauthenticated(self, client: TestClient):
        """Test getting inventory without authentication fails"""
        response = client.get("/api/inventory")
        assert response.status_code == 401

    def test_get_medicine_by_id(
        self, client: TestClient, auth_headers_admin, db_session
    ):
        """Test getting a specific medicine by ID"""
        from app.models import Medicine

        medicine = Medicine(
            name="Paracetamol 500mg",
            composition="Paracetamol",
            brand="Crocin",
            supplier="ABC Supplier",
            price=18.0,
            stock_quantity=100,
            expiry_date=date(2026, 12, 31),
        )
        db_session.add(medicine)
        db_session.commit()
        db_session.refresh(medicine)

        response = client.get(
            f"/api/inventory/{medicine.id}", headers=auth_headers_admin
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Paracetamol 500mg"
        assert data["brand"] == "Crocin"

    def test_get_medicine_not_found(self, client: TestClient, auth_headers_admin):
        """Test getting non-existent medicine returns 404"""
        response = client.get("/api/inventory/99999", headers=auth_headers_admin)
        assert response.status_code == 404

    def test_create_medicine_employee_forbidden(
        self, client: TestClient, auth_headers_employee
    ):
        """Test employee cannot create medicine"""
        response = client.post(
            "/api/inventory",
            headers=auth_headers_employee,
            json={
                "name": "Test Medicine",
                "composition": "Test",
                "brand": "Test",
                "price": 10.0,
                "stock_quantity": 10,
                "expiry_date": "2026-06-30",
            },
        )
        assert response.status_code == 403

    def test_create_medicine_customer_forbidden(
        self, client: TestClient, auth_headers_customer
    ):
        """Test customer cannot create medicine"""
        response = client.post(
            "/api/inventory",
            headers=auth_headers_customer,
            json={
                "name": "Test Medicine",
                "composition": "Test",
                "brand": "Test",
                "price": 10.0,
                "stock_quantity": 10,
                "expiry_date": "2026-06-30",
            },
        )
        assert response.status_code == 403

    def test_update_medicine_admin(
        self, client: TestClient, auth_headers_admin, db_session
    ):
        """Test admin can update medicine"""
        from app.models import Medicine

        medicine = Medicine(
            name="Original Name",
            composition="Test",
            brand="Test",
            supplier="ABC Supplier",
            price=10.0,
            stock_quantity=10,
            expiry_date=date(2026, 6, 30),
        )
        db_session.add(medicine)
        db_session.commit()
        db_session.refresh(medicine)

        response = client.put(
            f"/api/inventory/{medicine.id}",
            headers=auth_headers_admin,
            json={"name": "Updated Name", "stock_quantity": 20},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["stock_quantity"] == 20

    def test_update_medicine_not_found(self, client: TestClient, auth_headers_admin):
        """Test updating non-existent medicine returns 404"""
        response = client.put(
            "/api/inventory/99999",
            headers=auth_headers_admin,
            json={"name": "Test"},
        )
        assert response.status_code == 404

    def test_delete_medicine_admin(
        self, client: TestClient, auth_headers_admin, db_session
    ):
        """Test admin can delete medicine"""
        from app.models import Medicine

        medicine = Medicine(
            name="To Delete",
            composition="Test",
            brand="Test",
            supplier="Test Supplier",
            price=10.0,
            stock_quantity=10,
            expiry_date=date(2026, 6, 30),
        )
        db_session.add(medicine)
        db_session.commit()
        db_session.refresh(medicine)

        response = client.delete(
            f"/api/inventory/{medicine.id}", headers=auth_headers_admin
        )
        assert response.status_code == 200
        assert response.json()["ok"] is True

    def test_delete_medicine_employee_forbidden(
        self, client: TestClient, auth_headers_employee, db_session
    ):
        """Test employee cannot delete medicine"""
        from app.models import Medicine

        medicine = Medicine(
            name="Test",
            composition="Test",
            brand="Test",
            supplier="Test Supplier",
            price=10.0,
            stock_quantity=10,
            expiry_date=date(2026, 6, 30),
        )
        db_session.add(medicine)
        db_session.commit()
        db_session.refresh(medicine)

        response = client.delete(
            f"/api/inventory/{medicine.id}", headers=auth_headers_employee
        )
        assert response.status_code == 403
