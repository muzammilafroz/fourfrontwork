import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from main import app
from app.database import get_session
from app.models import User, UserRole
from app.auth import get_password_hash


TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})


def override_get_session():
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="function")
def db_session():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def client(db_session):
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def admin_user(db_session: Session):
    user = User(
        name="Admin User",
        email="admin@test.com",
        phone="+91-90000-00001",
        role=UserRole.ADMIN,
        hashed_password=get_password_hash("admin123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def employee_user(db_session: Session):
    user = User(
        name="Employee User",
        email="employee@test.com",
        phone="+91-90000-00002",
        role=UserRole.EMPLOYEE,
        hashed_password=get_password_hash("employee123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def customer_user(db_session: Session):
    user = User(
        name="Customer User",
        email="customer@test.com",
        phone="+91-90000-00003",
        role=UserRole.CUSTOMER,
        hashed_password=get_password_hash("customer123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def admin_token(client: TestClient, admin_user: User):
    response = client.post(
        "/api/auth/login",
        data={"username": "admin@test.com", "password": "admin123"},
    )
    return response.json()["access_token"]


@pytest.fixture
def employee_token(client: TestClient, employee_user: User):
    response = client.post(
        "/api/auth/login",
        data={"username": "employee@test.com", "password": "employee123"},
    )
    return response.json()["access_token"]


@pytest.fixture
def customer_token(client: TestClient, customer_user: User):
    response = client.post(
        "/api/auth/login",
        data={"username": "customer@test.com", "password": "customer123"},
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers_admin(admin_token: str):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def auth_headers_employee(employee_token: str):
    return {"Authorization": f"Bearer {employee_token}"}


@pytest.fixture
def auth_headers_customer(customer_token: str):
    return {"Authorization": f"Bearer {customer_token}"}