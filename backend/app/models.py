from datetime import date, datetime, time, timezone
from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


# --- Enums ---
class UserRole(str, Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"
    CUSTOMER = "customer"


class RequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"


class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


# --- Users ---
class UserBase(SQLModel):
    name: str
    email: str = Field(index=True, unique=True)
    phone: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    role: UserRole = Field(default=UserRole.CUSTOMER)

    # Relationships
    orders: List["Order"] = Relationship(
        back_populates="customer",
        sa_relationship_kwargs={"foreign_keys": "Order.customer_id"},
    )
    handled_orders: List["Order"] = Relationship(
        back_populates="employee",
        sa_relationship_kwargs={"foreign_keys": "Order.employee_id"},
    )
    requested_medicines: List["MedicineRequest"] = Relationship(
        back_populates="requester",
        sa_relationship_kwargs={"foreign_keys": "MedicineRequest.requested_by"},
    )
    handled_requests: List["MedicineRequest"] = Relationship(
        back_populates="handler",
        sa_relationship_kwargs={"foreign_keys": "MedicineRequest.handled_by"},
    )
    feedbacks: List["Feedback"] = Relationship(back_populates="customer")
    appointments: List["Appointment"] = Relationship(back_populates="customer")


class UserCreate(UserBase):
    name: str
    email: str
    phone: str
    password: str


class UserPublic(UserBase):
    id: int


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    email: str


# --- Medicines ---
class MedicineBase(SQLModel):
    name: str
    composition: str
    brand: str
    price: float
    stock_quantity: int
    expiry_date: date


class Medicine(MedicineBase, table=True):
    __tablename__ = "medicines"
    id: Optional[int] = Field(default=None, primary_key=True)

    cart_items: List["CartItem"] = Relationship(back_populates="medicine")


# --- Orders ---
class OrderBase(SQLModel):
    customer_name: str
    customer_phone: str
    total_price: float
    order_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Order(OrderBase, table=True):
    __tablename__ = "orders"
    id: Optional[int] = Field(default=None, primary_key=True)

    customer_id: int = Field(foreign_key="users.id")
    employee_id: Optional[int] = Field(default=None, foreign_key="users.id")

    # Relationships
    customer: User = Relationship(
        back_populates="orders",
        sa_relationship_kwargs={"foreign_keys": "Order.customer_id"},
    )
    employee: Optional[User] = Relationship(
        back_populates="handled_orders",
        sa_relationship_kwargs={"foreign_keys": "Order.employee_id"},
    )
    cart_items: List["CartItem"] = Relationship(back_populates="order")


# --- Cart Items ---
class CartItemBase(SQLModel):
    quantity: int
    price: float


class CartItem(CartItemBase, table=True):
    __tablename__ = "cart_items"
    id: Optional[int] = Field(default=None, primary_key=True)

    order_id: int = Field(foreign_key="orders.id")
    medicine_id: int = Field(foreign_key="medicines.id")

    # Relationships
    order: "Order" = Relationship(back_populates="cart_items")
    medicine: "Medicine" = Relationship(back_populates="cart_items")


# --- Medicine Requests ---
class MedicineRequestBase(SQLModel):
    medicine_name: str
    composition: str
    requested_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: RequestStatus = Field(default=RequestStatus.PENDING)


class MedicineRequest(MedicineRequestBase, table=True):
    __tablename__ = "medicine_requests"
    id: Optional[int] = Field(default=None, primary_key=True)

    requested_by: int = Field(foreign_key="users.id")
    handled_by: Optional[int] = Field(default=None, foreign_key="users.id")

    # Relationships
    requester: User = Relationship(
        back_populates="requested_medicines",
        sa_relationship_kwargs={"foreign_keys": "MedicineRequest.requested_by"},
    )
    handler: Optional[User] = Relationship(
        back_populates="handled_requests",
        sa_relationship_kwargs={"foreign_keys": "MedicineRequest.handled_by"},
    )


# --- Doctors ---
class DoctorBase(SQLModel):
    name: str
    specialization: str
    available_days: str
    available_time: str


class Doctor(DoctorBase, table=True):
    __tablename__ = "doctors"
    id: Optional[int] = Field(default=None, primary_key=True)

    appointments: List["Appointment"] = Relationship(back_populates="doctor")


# --- Appointments ---
class AppointmentBase(SQLModel):
    patient_name: str
    patient_phone: str
    appointment_date: date
    appointment_time: time
    status: AppointmentStatus = Field(default=AppointmentStatus.SCHEDULED)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    visit_fee: float


class Appointment(AppointmentBase, table=True):
    __tablename__ = "appointments"
    id: Optional[int] = Field(default=None, primary_key=True)

    doctor_id: int = Field(foreign_key="doctors.id")
    customer_id: int = Field(foreign_key="users.id")

    # Relationships
    doctor: Doctor = Relationship(back_populates="appointments")
    customer: User = Relationship(back_populates="appointments")


# --- Feedback ---
class FeedbackBase(SQLModel):
    rating: int = Field(ge=1, le=5)  # Added validation for 1-5 stars
    comment: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Feedback(FeedbackBase, table=True):
    __tablename__ = "feedbacks"
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="users.id")

    # Relationships
    customer: User = Relationship(back_populates="feedbacks")
