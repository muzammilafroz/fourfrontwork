import pytest
from fastapi.testclient import TestClient


class TestStaff:
    """Test cases for /api/staff endpoints"""

    def test_get_staff_admin(self, client: TestClient, auth_headers_admin):
        """Test admin can view all staff members"""
        response = client.get("/api/staff", headers=auth_headers_admin)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_staff_employee_forbidden(self, client: TestClient, auth_headers_employee):
        """Test employee cannot view staff list"""
        response = client.get("/api/staff", headers=auth_headers_employee)
        assert response.status_code == 403

    def test_get_staff_customer_forbidden(self, client: TestClient, auth_headers_customer):
        """Test customer cannot view staff list"""
        response = client.get("/api/staff", headers=auth_headers_customer)
        assert response.status_code == 403

    def test_get_staff_unauthenticated(self, client: TestClient):
        """Test getting staff without auth fails"""
        response = client.get("/api/staff")
        assert response.status_code == 401

    def test_get_staff_member_by_id_admin(self, client: TestClient, auth_headers_admin, db_session):
        """Test admin can get specific staff member by ID"""
        from app.models import User, UserRole
        staff = User(
            name="Staff Member",
            email="staff@test.com",
            phone="+91-90000-00005",
            role=UserRole.EMPLOYEE,
            hashed_password="hashed",
        )
        db_session.add(staff)
        db_session.commit()
        db_session.refresh(staff)

        response = client.get(f"/api/staff/{staff.id}", headers=auth_headers_admin)
        assert response.status_code == 200
        assert response.json()["email"] == "staff@test.com"

    def test_get_staff_member_not_found(self, client: TestClient, auth_headers_admin):
        """Test getting non-existent staff returns 404"""
        response = client.get("/api/staff/99999", headers=auth_headers_admin)
        assert response.status_code == 404

    def test_create_staff_admin(self, client: TestClient, auth_headers_admin):
        """Test admin can create new staff member"""
        response = client.post(
            "/api/staff",
            headers=auth_headers_admin,
            json={
                "name": "New Staff",
                "email": "newstaff@test.com",
                "phone": "+91-90000-00006",
                "role": "employee",
                "hashed_password": "hashedpassword",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newstaff@test.com"
        assert data["role"] == "employee"

    def test_create_staff_employee_forbidden(self, client: TestClient, auth_headers_employee):
        """Test employee cannot create staff"""
        response = client.post(
            "/api/staff",
            headers=auth_headers_employee,
            json={
                "name": "New Staff",
                "email": "newstaff@test.com",
                "phone": "+91-90000-00006",
                "role": "employee",
            },
        )
        assert response.status_code == 403

    def test_create_staff_customer_forbidden(self, client: TestClient, auth_headers_customer):
        """Test customer cannot create staff"""
        response = client.post(
            "/api/staff",
            headers=auth_headers_customer,
            json={
                "name": "New Staff",
                "email": "newstaff@test.com",
                "phone": "+91-90000-00006",
                "role": "employee",
            },
        )
        assert response.status_code == 403

    def test_update_staff_admin(self, client: TestClient, auth_headers_admin, db_session):
        """Test admin can update staff member"""
        from app.models import User, UserRole
        staff = User(
            name="Original Name",
            email="original@test.com",
            phone="+91-90000-00007",
            role=UserRole.EMPLOYEE,
            hashed_password="hashed",
        )
        db_session.add(staff)
        db_session.commit()
        db_session.refresh(staff)

        response = client.put(
            f"/api/staff/{staff.id}",
            headers=auth_headers_admin,
            json={"name": "Updated Name", "phone": "+91-90000-00008"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["phone"] == "+91-90000-00008"

    def test_update_staff_not_found(self, client: TestClient, auth_headers_admin):
        """Test updating non-existent staff returns 404"""
        response = client.put(
            "/api/staff/99999",
            headers=auth_headers_admin,
            json={"name": "Test"},
        )
        assert response.status_code == 404

    def test_delete_staff_admin(self, client: TestClient, auth_headers_admin, db_session):
        """Test admin can delete staff member"""
        from app.models import User, UserRole
        staff = User(
            name="To Delete",
            email="delete@test.com",
            phone="+91-90000-00009",
            role=UserRole.EMPLOYEE,
            hashed_password="hashed",
        )
        db_session.add(staff)
        db_session.commit()
        db_session.refresh(staff)

        response = client.delete(f"/api/staff/{staff.id}", headers=auth_headers_admin)
        assert response.status_code == 200
        assert response.json()["ok"] is True

    def test_delete_staff_employee_forbidden(self, client: TestClient, auth_headers_employee, db_session):
        """Test employee cannot delete staff"""
        from app.models import User, UserRole
        staff = User(
            name="Test Staff",
            email="testdelete@test.com",
            phone="+91-90000-00010",
            role=UserRole.EMPLOYEE,
            hashed_password="hashed",
        )
        db_session.add(staff)
        db_session.commit()
        db_session.refresh(staff)

        response = client.delete(f"/api/staff/{staff.id}", headers=auth_headers_employee)
        assert response.status_code == 403

    def test_delete_staff_customer_forbidden(self, client: TestClient, auth_headers_customer, db_session):
        """Test customer cannot delete staff"""
        from app.models import User, UserRole
        staff = User(
            name="Test Staff",
            email="testdelete2@test.com",
            phone="+91-90000-00011",
            role=UserRole.EMPLOYEE,
            hashed_password="hashed",
        )
        db_session.add(staff)
        db_session.commit()
        db_session.refresh(staff)

        response = client.delete(f"/api/staff/{staff.id}", headers=auth_headers_customer)
        assert response.status_code == 403