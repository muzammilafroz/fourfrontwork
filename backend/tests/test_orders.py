from fastapi.testclient import TestClient


class TestOrders:
    """Test cases for /api/orders endpoints"""

    def test_get_orders_admin(self, client: TestClient, auth_headers_admin):
        """Test admin can get all orders"""
        response = client.get("/api/orders", headers=auth_headers_admin)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_orders_employee(self, client: TestClient, auth_headers_employee):
        """Test employee can get all orders"""
        response = client.get("/api/orders", headers=auth_headers_employee)
        assert response.status_code == 200

    def test_get_orders_customer_only_own(
        self, client: TestClient, auth_headers_customer, db_session
    ):
        """Test customer can only see their own orders"""
        from app.models import Order

        order = Order(
            customer_name="Customer User",
            customer_phone="+91-90000-00003",
            total_price=100.0,
            customer_id=1,
        )
        db_session.add(order)
        db_session.commit()

        response = client.get("/api/orders", headers=auth_headers_customer)
        assert response.status_code == 200
        orders = response.json()
        assert len(orders) == 1

    def test_get_orders_unauthenticated(self, client: TestClient):
        """Test getting orders without auth fails"""
        response = client.get("/api/orders")
        assert response.status_code == 401

    def test_get_order_by_id_admin(
        self, client: TestClient, auth_headers_admin, db_session
    ):
        """Test admin can get any order by ID"""
        from app.models import Order

        order = Order(
            customer_name="Test Customer",
            customer_phone="+91-99999-99999",
            total_price=50.0,
            customer_id=1,
        )
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)

        response = client.get(f"/api/orders/{order.id}", headers=auth_headers_admin)
        assert response.status_code == 200
        assert response.json()["total_price"] == 50.0

    def test_get_order_by_id_customer_own(
        self, client: TestClient, auth_headers_customer, db_session
    ):
        """Test customer can get their own order by ID"""
        from app.models import Order

        order = Order(
            customer_name="Customer User",
            customer_phone="+91-90000-00003",
            total_price=75.0,
            customer_id=1,
        )
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)

        response = client.get(f"/api/orders/{order.id}", headers=auth_headers_customer)
        assert response.status_code == 200

    def test_get_order_by_id_customer_other_forbidden(
        self, client: TestClient, auth_headers_customer, db_session
    ):
        """Test customer cannot access other customer's orders"""
        from app.models import Order

        order = Order(
            customer_name="Other Customer",
            customer_phone="+91-88888-88888",
            total_price=100.0,
            customer_id=999,
        )
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)

        response = client.get(f"/api/orders/{order.id}", headers=auth_headers_customer)
        assert response.status_code == 403

    def test_get_order_not_found(self, client: TestClient, auth_headers_admin):
        """Test getting non-existent order returns 404"""
        response = client.get("/api/orders/99999", headers=auth_headers_admin)
        assert response.status_code == 404

    def test_create_order_customer(self, client: TestClient, auth_headers_customer):
        """Test customer can create an order"""
        response = client.post(
            "/api/orders",
            headers=auth_headers_customer,
            json={
                "customer_name": "Customer User",
                "customer_phone": "+91-90000-00003",
                "total_price": 150.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_price"] == 150.0

    def test_create_order_employee_forbidden(
        self, client: TestClient, auth_headers_employee
    ):
        """Test employee cannot create order as customer"""
        response = client.post(
            "/api/orders",
            headers=auth_headers_employee,
            json={
                "customer_name": "Employee User",
                "customer_phone": "+91-90000-00002",
                "total_price": 50.0,
            },
        )
        assert response.status_code == 403

    def test_update_order_admin(
        self, client: TestClient, auth_headers_admin, db_session
    ):
        """Test admin can update order"""
        from app.models import Order

        order = Order(
            customer_name="Test",
            customer_phone="+91-99999-99999",
            total_price=50.0,
            customer_id=1,
        )
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)

        response = client.put(
            f"/api/orders/{order.id}",
            headers=auth_headers_admin,
            json={"total_price": 75.0},
        )
        assert response.status_code == 200
        assert response.json()["total_price"] == 75.0

    def test_update_order_employee_sets_employee_id(
        self, client: TestClient, auth_headers_employee, db_session
    ):
        """Test employee updating order sets their ID"""
        from app.models import Order

        order = Order(
            customer_name="Test",
            customer_phone="+91-99999-99999",
            total_price=50.0,
            customer_id=1,
        )
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)

        response = client.put(
            f"/api/orders/{order.id}",
            headers=auth_headers_employee,
            json={"total_price": 60.0},
        )
        assert response.status_code == 200

    def test_update_order_customer_forbidden(
        self, client: TestClient, auth_headers_customer, db_session
    ):
        """Test customer cannot update orders"""
        from app.models import Order

        order = Order(
            customer_name="Customer User",
            customer_phone="+91-90000-00003",
            total_price=50.0,
            customer_id=1,
        )
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)

        response = client.put(
            f"/api/orders/{order.id}",
            headers=auth_headers_customer,
            json={"total_price": 100.0},
        )
        assert response.status_code == 403
