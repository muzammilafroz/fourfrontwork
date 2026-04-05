import pytest
from fastapi.testclient import TestClient


class TestCarts:
    """Test cases for /api/carts endpoints"""

    def test_get_cart_items_authenticated(self, client: TestClient, auth_headers_customer):
        """Test authenticated user can get cart items"""
        response = client.get("/api/carts", headers=auth_headers_customer)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_cart_items_unauthenticated(self, client: TestClient):
        """Test getting cart without auth fails"""
        response = client.get("/api/carts")
        assert response.status_code == 401

    def test_get_cart_item_by_id(self, client: TestClient, auth_headers_customer, db_session):
        """Test getting a specific cart item"""
        from app.models import Order, CartItem
        order = Order(
            customer_name="Customer User",
            customer_phone="+91-90000-00003",
            total_price=100.0,
            customer_id=1,
        )
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)

        cart_item = CartItem(
            order_id=order.id,
            medicine_id=1,
            quantity=2,
            price=10.0,
        )
        db_session.add(cart_item)
        db_session.commit()
        db_session.refresh(cart_item)

        response = client.get(f"/api/carts/{cart_item.id}", headers=auth_headers_customer)
        assert response.status_code == 200

    def test_get_cart_item_not_found(self, client: TestClient, auth_headers_customer):
        """Test getting non-existent cart item returns 404"""
        response = client.get("/api/carts/99999", headers=auth_headers_customer)
        assert response.status_code == 404

    def test_create_cart_item(self, client: TestClient, auth_headers_customer, db_session):
        """Test customer can add item to cart"""
        from app.models import Order
        order = Order(
            customer_name="Customer User",
            customer_phone="+91-90000-00003",
            total_price=0.0,
            customer_id=1,
        )
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)

        response = client.post(
            "/api/carts",
            headers=auth_headers_customer,
            json={
                "order_id": order.id,
                "medicine_id": 1,
                "quantity": 3,
                "price": 15.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["quantity"] == 3
        assert data["price"] == 15.0

    def test_create_cart_item_order_not_found(self, client: TestClient, auth_headers_customer):
        """Test adding cart item with non-existent order fails"""
        response = client.post(
            "/api/carts",
            headers=auth_headers_customer,
            json={
                "order_id": 99999,
                "medicine_id": 1,
                "quantity": 1,
                "price": 10.0,
            },
        )
        assert response.status_code == 404

    def test_create_cart_item_unauthorized(self, client: TestClient, auth_headers_employee, db_session):
        """Test employee cannot add cart items to others' orders"""
        from app.models import Order
        order = Order(
            customer_name="Customer User",
            customer_phone="+91-90000-00003",
            total_price=0.0,
            customer_id=999,
        )
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)

        response = client.post(
            "/api/carts",
            headers=auth_headers_employee,
            json={
                "order_id": order.id,
                "medicine_id": 1,
                "quantity": 1,
                "price": 10.0,
            },
        )
        assert response.status_code == 403

    def test_update_cart_item(self, client: TestClient, auth_headers_customer, db_session):
        """Test customer can update their cart item"""
        from app.models import Order, CartItem
        order = Order(
            customer_name="Customer User",
            customer_phone="+91-90000-00003",
            total_price=0.0,
            customer_id=1,
        )
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)

        cart_item = CartItem(
            order_id=order.id,
            medicine_id=1,
            quantity=1,
            price=10.0,
        )
        db_session.add(cart_item)
        db_session.commit()
        db_session.refresh(cart_item)

        response = client.put(
            f"/api/carts/{cart_item.id}",
            headers=auth_headers_customer,
            json={"quantity": 5},
        )
        assert response.status_code == 200
        assert response.json()["quantity"] == 5

    def test_delete_cart_item(self, client: TestClient, auth_headers_customer, db_session):
        """Test customer can delete their cart item"""
        from app.models import Order, CartItem
        order = Order(
            customer_name="Customer User",
            customer_phone="+91-90000-00003",
            total_price=0.0,
            customer_id=1,
        )
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)

        cart_item = CartItem(
            order_id=order.id,
            medicine_id=1,
            quantity=1,
            price=10.0,
        )
        db_session.add(cart_item)
        db_session.commit()
        db_session.refresh(cart_item)

        response = client.delete(f"/api/carts/{cart_item.id}", headers=auth_headers_customer)
        assert response.status_code == 200
        assert response.json()["ok"] is True