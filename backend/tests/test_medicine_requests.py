import pytest
from fastapi.testclient import TestClient


class TestMedicineRequests:
    """Test cases for /api/medicine-requests endpoints"""

    def test_get_requests_admin(self, client: TestClient, auth_headers_admin):
        """Test admin can view all medicine requests"""
        response = client.get("/api/medicine-requests", headers=auth_headers_admin)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_requests_employee(self, client: TestClient, auth_headers_employee):
        """Test employee can view all medicine requests"""
        response = client.get("/api/medicine-requests", headers=auth_headers_employee)
        assert response.status_code == 200

    def test_get_requests_customer_only_own(self, client: TestClient, auth_headers_customer, db_session):
        """Test customer can only see their own requests"""
        from app.models import MedicineRequest
        request = MedicineRequest(
            medicine_name="Test Medicine",
            composition="Test composition",
            requested_by=1,
        )
        db_session.add(request)
        db_session.commit()

        response = client.get("/api/medicine-requests", headers=auth_headers_customer)
        assert response.status_code == 200
        requests = response.json()
        assert len(requests) == 1

    def test_get_requests_unauthenticated(self, client: TestClient):
        """Test getting requests without auth fails"""
        response = client.get("/api/medicine-requests")
        assert response.status_code == 401

    def test_get_request_by_id(self, client: TestClient, auth_headers_admin, db_session):
        """Test admin can get specific request by ID"""
        from app.models import MedicineRequest
        request = MedicineRequest(
            medicine_name="Paracetamol",
            composition="Paracetamol 500mg",
            requested_by=1,
        )
        db_session.add(request)
        db_session.commit()
        db_session.refresh(request)

        response = client.get(f"/api/medicine-requests/{request.id}", headers=auth_headers_admin)
        assert response.status_code == 200
        assert response.json()["medicine_name"] == "Paracetamol"

    def test_get_request_not_found(self, client: TestClient, auth_headers_admin):
        """Test getting non-existent request returns 404"""
        response = client.get("/api/medicine-requests/99999", headers=auth_headers_admin)
        assert response.status_code == 404

    def test_create_request_customer(self, client: TestClient, auth_headers_customer):
        """Test customer can create medicine request"""
        response = client.post(
            "/api/medicine-requests",
            headers=auth_headers_customer,
            json={
                "medicine_name": "New Medicine",
                "composition": "Active ingredients",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["medicine_name"] == "New Medicine"
        assert data["requested_by"] is not None

    def test_create_request_employee_forbidden(self, client: TestClient, auth_headers_employee):
        """Test employee cannot create medicine request"""
        response = client.post(
            "/api/medicine-requests",
            headers=auth_headers_employee,
            json={
                "medicine_name": "Test",
                "composition": "Test",
            },
        )
        assert response.status_code == 403

    def test_create_request_admin_forbidden(self, client: TestClient, auth_headers_admin):
        """Test admin cannot create medicine request"""
        response = client.post(
            "/api/medicine-requests",
            headers=auth_headers_admin,
            json={
                "medicine_name": "Test",
                "composition": "Test",
            },
        )
        assert response.status_code == 403

    def test_update_request_admin(self, client: TestClient, auth_headers_admin, db_session):
        """Test admin can update medicine request (approve/reject)"""
        from app.models import MedicineRequest
        request = MedicineRequest(
            medicine_name="Test Medicine",
            composition="Test",
            requested_by=1,
        )
        db_session.add(request)
        db_session.commit()
        db_session.refresh(request)

        response = client.put(
            f"/api/medicine-requests/{request.id}",
            headers=auth_headers_admin,
            json={"status": "approved"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "approved"

    def test_update_request_employee(self, client: TestClient, auth_headers_employee, db_session):
        """Test employee can update medicine request"""
        from app.models import MedicineRequest
        request = MedicineRequest(
            medicine_name="Test Medicine",
            composition="Test",
            requested_by=1,
        )
        db_session.add(request)
        db_session.commit()
        db_session.refresh(request)

        response = client.put(
            f"/api/medicine-requests/{request.id}",
            headers=auth_headers_employee,
            json={"status": "rejected"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "rejected"

    def test_update_request_customer_forbidden(self, client: TestClient, auth_headers_customer, db_session):
        """Test customer cannot update medicine request"""
        from app.models import MedicineRequest
        request = MedicineRequest(
            medicine_name="Test",
            composition="Test",
            requested_by=1,
        )
        db_session.add(request)
        db_session.commit()
        db_session.refresh(request)

        response = client.put(
            f"/api/medicine-requests/{request.id}",
            headers=auth_headers_customer,
            json={"status": "approved"},
        )
        assert response.status_code == 403

    def test_update_request_not_found(self, client: TestClient, auth_headers_admin):
        """Test updating non-existent request returns 404"""
        response = client.put(
            "/api/medicine-requests/99999",
            headers=auth_headers_admin,
            json={"status": "approved"},
        )
        assert response.status_code == 404