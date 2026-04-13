from datetime import date

from sqlmodel import Session, select

from .crud import get_password_hash
from .database import engine
from .models import CartItem, Doctor, Medicine, Order, User, UserRole


def seed_data():
    with Session(engine) as session:
        # Prevent duplicate seeding
        existing_user = session.exec(select(User)).first()
        if existing_user:
            print("Database already seeded.")
            return

        # Dummy users
        customers = [
            User(
                name="Yogi Kumar",
                email="yogi.kumar@gmail.com",
                phone="9827283360",
                hashed_password=get_password_hash("yogi"),
                role=UserRole.CUSTOMER,
            ),
            User(
                name="Rahul Verma",
                email="rahul.verma@gmail.com",
                phone="9012345678",
                hashed_password=get_password_hash("rahul"),
                role=UserRole.CUSTOMER,
            ),
            User(
                name="Sneha Patel",
                email="sneha.patel@yahoo.com",
                phone="9123456780",
                hashed_password=get_password_hash("sneha"),
                role=UserRole.CUSTOMER,
            ),
        ]
        employees = [
            User(
                name="Anjali Sharma",
                email="anjali.sharma@medease.com",
                phone="8869626614",
                hashed_password=get_password_hash("anjali"),
                role=UserRole.EMPLOYEE,
            ),
            User(
                name="Priya Nair",
                email="priya.nair@medease.com",
                phone="9345678123",
                hashed_password=get_password_hash("priya"),
                role=UserRole.EMPLOYEE,
            ),
        ]
        users = [
            User(
                name="Admin",
                email="admin@medease.com",
                phone="1234567890",
                hashed_password=get_password_hash("admin"),
                role=UserRole.ADMIN,
            ),
            User(
                name="Anonymous",
                email="anonymous@gmail.com",
                phone="0000000000",
                hashed_password=get_password_hash("anon"),
                role=UserRole.CUSTOMER,
            ),
            *customers,
            *employees,
        ]

        session.add_all(users)
        session.commit()

        session.refresh(users[0])
        session.refresh(users[1])
        session.refresh(users[4])

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

        # Dummy medicines
        medicines = [
            Medicine(
                name="Dolo 650",
                composition="Paracetamol 650mg",
                brand="Micro Labs Ltd",
                price=30.50,
                stock_quantity=50,
                expiry_date=date(2026, 5, 20),
            ),
            Medicine(
                name="Augmentin 625 Duo",
                composition="Amoxycillin 500mg + Clavulanic Acid 125mg",
                brand="GSK",
                price=201.50,
                stock_quantity=150,
                expiry_date=date(2027, 2, 15),
            ),
            Medicine(
                name="Azithral 500",
                composition="Azithromycin 500mg",
                brand="Alembic Pharmaceuticals",
                price=119.50,
                stock_quantity=200,
                expiry_date=date(2026, 11, 10),
            ),
            Medicine(
                name="Pan 40",
                composition="Pantoprazole 40mg",
                brand="Alkem Laboratories",
                price=155.00,
                stock_quantity=300,
                expiry_date=date(2026, 8, 25),
            ),
            Medicine(
                name="Glycomet 500",
                composition="Metformin 500mg",
                brand="USV Pvt Ltd",
                price=24.25,
                stock_quantity=60,
                expiry_date=date(2027, 1, 5),
            ),
            Medicine(
                name="Telma 40",
                composition="Telmisartan 40mg",
                brand="Glenmark Pharmaceuticals",
                price=98.00,
                stock_quantity=250,
                expiry_date=date(2026, 12, 30),
            ),
            Medicine(
                name="Limcee",
                composition="Vitamin C (Ascorbic Acid) 500mg",
                brand="Abbott India",
                price=23.10,
                stock_quantity=100,
                expiry_date=date(2027, 6, 1),
            ),
            Medicine(
                name="Shelcal 500",
                composition="Calcium 500mg + Vitamin D3 250 IU",
                brand="Torrent Pharmaceuticals",
                price=118.50,
                stock_quantity=400,
                expiry_date=date(2026, 9, 14),
            ),
            Medicine(
                name="Montair LC",
                composition="Montelukast 10mg + Levocetirizine 5mg",
                brand="Cipla",
                price=190.00,
                stock_quantity=180,
                expiry_date=date(2026, 4, 18),
            ),
            Medicine(
                name="Allegra 120mg",
                composition="Fexofenadine 120mg",
                brand="Sanofi India",
                price=210.50,
                stock_quantity=120,
                expiry_date=date(2026, 10, 12),
            ),
            Medicine(
                name="Combiflam",
                composition="Ibuprofen 400mg + Paracetamol 325mg",
                brand="Sanofi India",
                price=45.25,
                stock_quantity=450,
                expiry_date=date(2027, 3, 20),
            ),
            Medicine(
                name="Omez 20",
                composition="Omeprazole 20mg",
                brand="Dr. Reddy's Laboratories",
                price=58.00,
                stock_quantity=350,
                expiry_date=date(2026, 7, 11),
            ),
            Medicine(
                name="Becosules Z",
                composition="Vitamin B-Complex + Vitamin C + Zinc",
                brand="Pfizer",
                price=45.50,
                stock_quantity=500,
                expiry_date=date(2027, 5, 30),
            ),
            Medicine(
                name="Taxim-O 200",
                composition="Cefixime 200mg",
                brand="Alkem Laboratories",
                price=105.00,
                stock_quantity=220,
                expiry_date=date(2026, 1, 15),
            ),
            Medicine(
                name="Zifi 200",
                composition="Cefixime 200mg",
                brand="FDC Ltd",
                price=108.00,
                stock_quantity=190,
                expiry_date=date(2026, 11, 22),
            ),
            Medicine(
                name="Liv.52 DS",
                composition="Himsra + Kasani (Herbal)",
                brand="Himalaya Wellness",
                price=170.00,
                stock_quantity=150,
                expiry_date=date(2027, 8, 1),
            ),
            Medicine(
                name="Atarax 25mg",
                composition="Hydroxyzine 25mg",
                brand="Dr. Reddy's Laboratories",
                price=85.00,
                stock_quantity=140,
                expiry_date=date(2026, 12, 10),
            ),
            Medicine(
                name="Moxikind-CV 625",
                composition="Amoxicillin 500mg + Potassium Clavulanate 125mg",
                brand="Mankind Pharma",
                price=195.00,
                stock_quantity=280,
                expiry_date=date(2026, 6, 15),
            ),
            Medicine(
                name="Arkamine",
                composition="Clonidine 100mcg",
                brand="Unichem Laboratories",
                price=65.50,
                stock_quantity=100,
                expiry_date=date(2027, 4, 1),
            ),
            Medicine(
                name="Voveran SR 100",
                composition="Diclofenac 100mg",
                brand="Novartis India",
                price=95.00,
                stock_quantity=200,
                expiry_date=date(2026, 9, 30),
            ),
            Medicine(
                name="Neurobion Forte",
                composition="Vitamin B-Complex + Vitamin B12",
                brand="Procter & Gamble (P&G)",
                price=34.50,
                stock_quantity=800,
                expiry_date=date(2027, 12, 15),
            ),
            Medicine(
                name="Okacet",
                composition="Cetirizine 10mg",
                brand="Cipla",
                price=18.50,
                stock_quantity=600,
                expiry_date=date(2026, 3, 12),
            ),
            Medicine(
                name="Pantocid 40",
                composition="Pantoprazole 40mg",
                brand="Sun Pharma",
                price=160.00,
                stock_quantity=320,
                expiry_date=date(2026, 11, 1),
            ),
            Medicine(
                name="Revital H",
                composition="Multivitamins + Minerals + Ginseng",
                brand="Sun Pharma",
                price=110.00,
                stock_quantity=200,
                expiry_date=date(2026, 10, 20),
            ),
            Medicine(
                name="Saridon",
                composition="Paracetamol + Propyphenazone + Caffeine",
                brand="Piramal Pharma",
                price=42.00,
                stock_quantity=1000,
                expiry_date=date(2027, 2, 28),
            ),
            Medicine(
                name="Vertin 16",
                composition="Betahistine 16mg",
                brand="Abbott India",
                price=175.00,
                stock_quantity=150,
                expiry_date=date(2026, 5, 5),
            ),
            Medicine(
                name="Eldoper",
                composition="Loperamide 2mg",
                brand="Micro Labs Ltd",
                price=22.50,
                stock_quantity=400,
                expiry_date=date(2026, 12, 31),
            ),
            Medicine(
                name="Deriphyllin",
                composition="Etofylline 77mg + Theophylline 23mg",
                brand="Zydus Lifesciences",
                price=15.00,
                stock_quantity=500,
                expiry_date=date(2027, 1, 10),
            ),
            Medicine(
                name="Orofer XT",
                composition="Ferrous Ascorbate + Folic Acid",
                brand="Emcure Pharmaceuticals",
                price=178.00,
                stock_quantity=220,
                expiry_date=date(2026, 8, 15),
            ),
            Medicine(
                name="Calpol 500",
                composition="Paracetamol 500mg",
                brand="GSK",
                price=15.50,
                stock_quantity=900,
                expiry_date=date(2027, 11, 20),
            ),
        ]

        session.add_all(medicines)
        session.commit()
        session.refresh(medicines[0])
        session.refresh(medicines[1])

        orders = [
            Order(
                customer_name=customers[1].name,
                customer_phone=customers[1].phone,
                customer_id=customers[1].id,
                employee_id=employees[0].id,
            )
        ]
        session.add_all(orders)
        session.commit()

        items = [
            CartItem(
                order_id=orders[0].id,
                medicine_id=medicines[0].id,
                quantity=2,
                price=medicines[0].price,
            ),
            CartItem(
                order_id=orders[0].id,
                medicine_id=medicines[1].id,
                quantity=1,
                price=medicines[1].price,
            ),
        ]
        session.add_all(items)
        session.commit()

        print("Dummy data inserted.")
