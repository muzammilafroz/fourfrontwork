from sqlmodel import Session, select

from .crud import get_password_hash
from .database import engine
from .models import Doctor, User, UserRole


def seed_data():
    with Session(engine) as session:
        # Prevent duplicate seeding
        existing_user = session.exec(select(User)).first()
        if existing_user:
            print("Database already seeded.")
            return

        # Dummy users
        users = [
            User(
                name="Admin",
                email="admin@medease.com",
                phone="1234567890",
                hashed_password=get_password_hash("admin"),
                role=UserRole.ADMIN,
            ),
            User(
                name="Yogi Kumar",
                email="yogi@gmail.com",
                phone="9827283360",
                hashed_password=get_password_hash("yogi"),
                role=UserRole.CUSTOMER,
            ),
            User(
                name="Anjali Sharma",
                email="anjali@gmail.com",
                phone="8869626614",
                hashed_password=get_password_hash("anjali"),
                role=UserRole.EMPLOYEE,
            ),
        ]

        session.add_all(users)
        session.commit()

        # Dummy doctors
        doctors = [
            Doctor(
                name="Dr. Arjun Mehta",
                specialization="Cardiologist",
                available_days="Monday, Wednesday, Friday",
                available_time="10:00 AM - 2:00 PM",
                consultation_fee=1200.00,
            ),
            Doctor(
                name="Dr. Priya Sharma",
                specialization="Dermatologist",
                available_days="Tuesday, Thursday",
                available_time="11:00 AM - 4:00 PM",
                consultation_fee=800.00,
            ),
            Doctor(
                name="Dr. Rohan Verma",
                specialization="Orthopedic Surgeon",
                available_days="Monday - Saturday",
                available_time="9:00 AM - 1:00 PM",
                consultation_fee=1000.00,
            ),
            Doctor(
                name="Dr. Sneha Iyer",
                specialization="Pediatrician",
                available_days="Monday - Friday",
                available_time="10:30 AM - 3:30 PM",
                consultation_fee=600.00,
            ),
            Doctor(
                name="Dr. Kabir Singh",
                specialization="Neurologist",
                available_days="Wednesday, Friday, Sunday",
                available_time="12:00 PM - 6:00 PM",
                consultation_fee=1500.00,
            ),
        ]

        session.add_all(doctors)
        session.commit()

        print("Dummy data inserted.")
