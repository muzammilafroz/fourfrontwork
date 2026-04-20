from fastapi.testclient import TestClient


class TestFeedback:
    """Test cases for /api/feedback endpoints"""

    def test_get_feedback_admin(self, client: TestClient, auth_headers_admin):
        """Test admin can view all feedback"""
        response = client.get("/api/feedback", headers=auth_headers_admin)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_feedback_employee(self, client: TestClient, auth_headers_employee):
        """Test employee can view all feedback"""
        response = client.get("/api/feedback", headers=auth_headers_employee)
        assert response.status_code == 200

    def test_get_feedback_customer_only_own(
        self, client: TestClient, auth_headers_customer, db_session
    ):
        """Test customer can only see their own feedback"""
        from app.models import Feedback

        feedback = Feedback(
            rating=5,
            comment="Great service!",
            customer_id=1,
        )
        db_session.add(feedback)
        db_session.commit()

        response = client.get("/api/feedback", headers=auth_headers_customer)
        assert response.status_code == 200
        feedbacks = response.json()
        assert len(feedbacks) == 1

    def test_get_feedback_unauthenticated(self, client: TestClient):
        """Test getting feedback without auth fails"""
        response = client.get("/api/feedback")
        assert response.status_code == 401

    def test_get_feedback_by_id_admin(
        self, client: TestClient, auth_headers_admin, db_session
    ):
        """Test admin can get specific feedback by ID"""
        from app.models import Feedback

        feedback = Feedback(
            rating=4,
            comment="Good service",
            customer_id=1,
        )
        db_session.add(feedback)
        db_session.commit()
        db_session.refresh(feedback)

        response = client.get(
            f"/api/feedback/{feedback.id}", headers=auth_headers_admin
        )
        assert response.status_code == 200
        assert response.json()["rating"] == 4

    def test_get_feedback_by_id_customer_own(
        self, client: TestClient, auth_headers_customer, db_session
    ):
        """Test customer can get their own feedback"""
        from app.models import Feedback

        feedback = Feedback(
            rating=5,
            comment="My feedback",
            customer_id=1,
        )
        db_session.add(feedback)
        db_session.commit()
        db_session.refresh(feedback)

        response = client.get(
            f"/api/feedback/{feedback.id}", headers=auth_headers_customer
        )
        assert response.status_code == 200

    def test_get_feedback_by_id_customer_other_forbidden(
        self, client: TestClient, auth_headers_customer, db_session
    ):
        """Test customer cannot view other customers' feedback"""
        from app.models import Feedback

        feedback = Feedback(
            rating=3,
            comment="Other's feedback",
            customer_id=999,
        )
        db_session.add(feedback)
        db_session.commit()
        db_session.refresh(feedback)

        response = client.get(
            f"/api/feedback/{feedback.id}", headers=auth_headers_customer
        )
        assert response.status_code == 403

    def test_get_feedback_not_found(self, client: TestClient, auth_headers_admin):
        """Test getting non-existent feedback returns 404"""
        response = client.get("/api/feedback/99999", headers=auth_headers_admin)
        assert response.status_code == 404

    def test_create_feedback_customer(self, client: TestClient, auth_headers_customer):
        """Test customer can create feedback"""
        response = client.post(
            "/api/feedback",
            headers=auth_headers_customer,
            json={
                "rating": 5,
                "comment": "Excellent service!",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["rating"] == 5
        assert data["comment"] == "Excellent service!"
        assert data["customer_id"] is not None

    def test_create_feedback_admin_forbidden(
        self, client: TestClient, auth_headers_admin
    ):
        """Test admin cannot create feedback"""
        response = client.post(
            "/api/feedback",
            headers=auth_headers_admin,
            json={
                "rating": 4,
                "comment": "Test feedback",
            },
        )
        assert response.status_code == 403

    def test_create_feedback_employee_forbidden(
        self, client: TestClient, auth_headers_employee
    ):
        """Test employee cannot create feedback"""
        response = client.post(
            "/api/feedback",
            headers=auth_headers_employee,
            json={
                "rating": 4,
                "comment": "Test feedback",
            },
        )
        assert response.status_code == 403
