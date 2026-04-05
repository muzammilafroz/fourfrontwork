from datetime import date, datetime, time, timezone
from enum import Enum
from typing import List, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Enums
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


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


# Users
class UserBase(SQLModel):
    name: str
    # email: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    phone: str
    role: UserRole = Field(default=UserRole.CUSTOMER)
    status: UserStatus = Field(default=UserStatus.ACTIVE)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

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
    prescriptions: List["Prescription"] = Relationship(back_populates="customer")


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: int


# JavaScript Web Token (JWT)
class Token(SQLModel):
    access_token: str
    token_type: str


class TokenPublic(Token):
    user: UserPublic


# Medicines
class MedicineBase(SQLModel):
    name: str
    composition: str
    brand: str
    price: float
    stock_quantity: int
    expiry_date: date


class Medicine(MedicineBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cart_items: List["CartItem"] = Relationship(back_populates="medicine")


# Orders
class OrderBase(SQLModel):
    customer_name: str
    customer_phone: str
    total_price: float
    order_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Order(OrderBase, table=True):
    id: int = Field(default=None, primary_key=True)

    customer_id: int = Field(foreign_key="user.id")
    employee_id: Optional[int] = Field(default=None, foreign_key="user.id")

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


# Cart Items
class CartItemBase(SQLModel):
    quantity: int
    price: float


class CartItem(CartItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    order_id: int = Field(foreign_key="order.id")
    medicine_id: int = Field(foreign_key="medicine.id")

    # Relationships
    order: "Order" = Relationship(back_populates="cart_items")
    medicine: "Medicine" = Relationship(back_populates="cart_items")


# Medicine Requests
class MedicineRequestBase(SQLModel):
    medicine_name: str
    composition: str
    requested_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: RequestStatus = Field(default=RequestStatus.PENDING)


class MedicineRequest(MedicineRequestBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    requested_by: int = Field(foreign_key="user.id")
    handled_by: Optional[int] = Field(default=None, foreign_key="user.id")

    # Relationships
    requester: User = Relationship(
        back_populates="requested_medicines",
        sa_relationship_kwargs={"foreign_keys": "MedicineRequest.requested_by"},
    )
    handler: Optional[User] = Relationship(
        back_populates="handled_requests",
        sa_relationship_kwargs={"foreign_keys": "MedicineRequest.handled_by"},
    )


# Appointments
class AppointmentCreate(SQLModel):
    patient_name: str
    patient_phone: str
    doctor_id: int

    appointment_date: date
    appointment_time: time


class AppointmentBase(SQLModel):
    patient_name: str
    patient_phone: str
    appointment_date: date
    appointment_time: time
    status: AppointmentStatus = Field(default=AppointmentStatus.SCHEDULED)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    visit_fee: float


class Appointment(AppointmentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    doctor_id: int = Field(foreign_key="doctor.id")
    customer_id: int = Field(foreign_key="user.id")

    # Relationships
    doctor: "Doctor" = Relationship(back_populates="appointments")
    customer: User = Relationship(back_populates="appointments")


class AppointmentPublic(AppointmentBase):
    id: int
    doctor_id: int
    customer_id: int
    doctor: Optional["DoctorPublic"] = None


# Doctors
class DoctorBase(SQLModel):
    name: str
    specialization: str
    available_days: str
    available_time: str
    consultation_fee: float


class Doctor(DoctorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    appointments: List["Appointment"] = Relationship(back_populates="doctor")


class DoctorPublic(DoctorBase):
    id: int
    # appointments: List[AppointmentPublic] = []


# Feedback
class FeedbackBase(SQLModel):
    rating: int = Field(ge=1, le=5)  # Added validation for 1-5 stars
    comment: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Feedback(FeedbackBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="user.id")
    # Relationships
    customer: User = Relationship(back_populates="feedbacks")


# Message
class Message(SQLModel):
    detail: str


# Medication
class MedicationBase(SQLModel):
    name: str
    dosage: str
    frequency: str
    duration: Optional[str] = None


class Medication(MedicationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prescription_id: Optional[int] = Field(default=None, foreign_key="prescription.id")
    prescription: Optional["Prescription"] = Relationship(back_populates="medications")


class MedicationPublic(MedicationBase):
    id: int


# Prescription
class PrescriptionCreate(SQLModel):
    image_base64: str


class PrescriptionBase(SQLModel):
    doctor_name: Optional[str] = None
    date: Optional[str] = None
    diagnosis: Optional[str] = None
    summary: Optional[str] = None
    image_path: str = ""
    image_base64: Optional[str] = None


class Prescription(PrescriptionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    customer: "User" = Relationship(back_populates="prescriptions")
    medications: List[Medication] = Relationship(back_populates="prescription")


class PrescriptionPublic(PrescriptionBase):
    id: int
    customer_id: int
    created_at: datetime
    medications: List[MedicationPublic] = []
