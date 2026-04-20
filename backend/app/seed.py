from datetime import date, datetime, time, timedelta, timezone

from sqlmodel import Session, select

from .crud import get_password_hash
from .database import engine
from .models import (
    Appointment,
    AppointmentStatus,
    CartItem,
    DiscountType,
    Doctor,
    Medicine,
    Order,
    User,
    UserRole,
)


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
                phone="1234567890",
                hashed_password=get_password_hash("anon"),
                role=UserRole.CUSTOMER,
            ),
            *customers,
            *employees,
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

        # Dummy medicines
        medicines = [
            Medicine(
                name="Dolo 650",
                composition="Paracetamol 650mg",
                brand="Micro Labs Ltd",
                supplier="Apollo Pharmacy",
                price=30.50,
                stock_quantity=50,
                expiry_date=date(2026, 5, 20),
            ),
            Medicine(
                name="Augmentin 625 Duo",
                composition="Amoxycillin 500mg + Clavulanic Acid 125mg",
                brand="GSK",
                supplier="MedPlus Health",
                price=201.50,
                stock_quantity=150,
                expiry_date=date(2027, 2, 15),
            ),
            Medicine(
                name="Azithral 500",
                composition="Azithromycin 500mg",
                brand="Alembic Pharmaceuticals",
                supplier="Entero Healthcare",
                price=119.50,
                stock_quantity=200,
                expiry_date=date(2026, 11, 10),
            ),
            Medicine(
                name="Pan 40",
                composition="Pantoprazole 40mg",
                brand="Alkem Laboratories",
                supplier="Wellness Forever",
                price=155.00,
                stock_quantity=300,
                expiry_date=date(2026, 8, 25),
            ),
            Medicine(
                name="Glycomet 500",
                composition="Metformin 500mg",
                brand="USV Pvt Ltd",
                supplier="Pharmarack Solutions",
                price=24.25,
                stock_quantity=60,
                expiry_date=date(2027, 1, 5),
            ),
            Medicine(
                name="Telma 40",
                composition="Telmisartan 40mg",
                brand="Glenmark Pharmaceuticals",
                supplier="Netmeds Marketplace",
                price=98.00,
                stock_quantity=250,
                expiry_date=date(2026, 12, 30),
            ),
            Medicine(
                name="Limcee",
                composition="Vitamin C (Ascorbic Acid) 500mg",
                brand="Abbott India",
                supplier="Tata 1mg",
                price=23.10,
                stock_quantity=100,
                expiry_date=date(2027, 6, 1),
            ),
            Medicine(
                name="Shelcal 500",
                composition="Calcium 500mg + Vitamin D3 250 IU",
                brand="Torrent Pharmaceuticals",
                supplier="Frank Ross Pharmacy",
                price=118.50,
                stock_quantity=400,
                expiry_date=date(2026, 9, 14),
            ),
            Medicine(
                name="Montair LC",
                composition="Montelukast 10mg + Levocetirizine 5mg",
                brand="Cipla",
                supplier="Meher Distributors",
                price=190.00,
                stock_quantity=180,
                expiry_date=date(2026, 4, 18),
            ),
            Medicine(
                name="Allegra 120mg",
                composition="Fexofenadine 120mg",
                brand="Sanofi India",
                supplier="Apollo Pharmacy",
                price=210.50,
                stock_quantity=120,
                expiry_date=date(2026, 10, 12),
            ),
            Medicine(
                name="Combiflam",
                composition="Ibuprofen 400mg + Paracetamol 325mg",
                brand="Sanofi India",
                supplier="MedPlus Health",
                price=45.25,
                stock_quantity=450,
                expiry_date=date(2027, 3, 20),
            ),
            Medicine(
                name="Omez 20",
                composition="Omeprazole 20mg",
                brand="Dr. Reddy's Laboratories",
                supplier="Entero Healthcare",
                price=58.00,
                stock_quantity=350,
                expiry_date=date(2026, 7, 11),
            ),
            Medicine(
                name="Becosules Z",
                composition="Vitamin B-Complex + Vitamin C + Zinc",
                brand="Pfizer",
                supplier="PharmEasy Supply",
                price=45.50,
                stock_quantity=250,
                expiry_date=date(2027, 5, 30),
            ),
            Medicine(
                name="Taxim-O 200",
                composition="Cefixime 200mg",
                brand="Alkem Laboratories",
                supplier="Wellness Forever",
                price=105.00,
                stock_quantity=220,
                expiry_date=date(2026, 1, 15),
            ),
            Medicine(
                name="Zifi 200",
                composition="Cefixime 200mg",
                brand="FDC Ltd",
                supplier="SastaSundar Ventures",
                price=108.00,
                stock_quantity=190,
                expiry_date=date(2026, 11, 22),
            ),
            Medicine(
                name="Liv.52 DS",
                composition="Himsra + Kasani (Herbal)",
                brand="Himalaya Wellness",
                supplier="Himalaya Retail Store",
                price=170.00,
                stock_quantity=150,
                expiry_date=date(2027, 8, 1),
            ),
            Medicine(
                name="Atarax 25mg",
                composition="Hydroxyzine 25mg",
                brand="Dr. Reddy's Laboratories",
                supplier="Vardhman Pharma",
                price=85.00,
                stock_quantity=140,
                expiry_date=date(2026, 12, 10),
            ),
            Medicine(
                name="Moxikind-CV 625",
                composition="Amoxicillin 500mg + Potassium Clavulanate 125mg",
                brand="Mankind Pharma",
                supplier="Apollo Pharmacy",
                price=195.00,
                stock_quantity=280,
                expiry_date=date(2026, 6, 15),
            ),
            Medicine(
                name="Arkamine",
                composition="Clonidine 100mcg",
                brand="Unichem Laboratories",
                supplier="MedPlus Health",
                price=65.50,
                stock_quantity=100,
                expiry_date=date(2027, 4, 1),
            ),
            Medicine(
                name="Voveran SR 100",
                composition="Diclofenac 100mg",
                brand="Novartis India",
                supplier="Frank Ross Pharmacy",
                price=95.00,
                stock_quantity=120,
                expiry_date=date(2026, 9, 30),
            ),
            Medicine(
                name="Neurobion Forte",
                composition="Vitamin B-Complex + Vitamin B12",
                brand="Procter & Gamble (P&G)",
                supplier="Tata 1mg",
                price=34.50,
                stock_quantity=380,
                expiry_date=date(2027, 12, 15),
            ),
            Medicine(
                name="Okacet",
                composition="Cetirizine 10mg",
                brand="Cipla",
                supplier="Netmeds Marketplace",
                price=18.50,
                stock_quantity=30,
                expiry_date=date(2026, 3, 12),
            ),
            Medicine(
                name="Pantocid 40",
                composition="Pantoprazole 40mg",
                brand="Sun Pharma",
                supplier="Entero Healthcare",
                price=160.00,
                stock_quantity=320,
                expiry_date=date(2026, 11, 1),
            ),
            Medicine(
                name="Revital H",
                composition="Multivitamins + Minerals + Ginseng",
                brand="Sun Pharma",
                supplier="Wellness Forever",
                price=110.00,
                stock_quantity=120,
                expiry_date=date(2026, 10, 20),
            ),
            Medicine(
                name="Saridon",
                composition="Paracetamol + Propyphenazone + Caffeine",
                brand="Piramal Pharma",
                supplier="PharmEasy Supply",
                price=42.00,
                stock_quantity=180,
                expiry_date=date(2027, 2, 28),
            ),
            Medicine(
                name="Vertin 16",
                composition="Betahistine 16mg",
                brand="Abbott India",
                supplier="MedPlus Health",
                price=175.00,
                stock_quantity=150,
                expiry_date=date(2026, 5, 5),
            ),
            Medicine(
                name="Eldoper",
                composition="Loperamide 2mg",
                brand="Micro Labs Ltd",
                supplier="Apollo Pharmacy",
                price=22.50,
                stock_quantity=540,
                expiry_date=date(2026, 12, 31),
            ),
            Medicine(
                name="Deriphyllin",
                composition="Etofylline 77mg + Theophylline 23mg",
                brand="Zydus Lifesciences",
                supplier="Entero Healthcare",
                price=15.00,
                stock_quantity=50,
                expiry_date=date(2027, 1, 10),
            ),
            Medicine(
                name="Orofer XT",
                composition="Ferrous Ascorbate + Folic Acid",
                brand="Emcure Pharmaceuticals",
                supplier="Meher Distributors",
                price=178.00,
                stock_quantity=220,
                expiry_date=date(2026, 8, 15),
            ),
            Medicine(
                name="Calpol 500",
                composition="Paracetamol 500mg",
                brand="GSK",
                supplier="Tata 1mg",
                price=15.50,
                stock_quantity=0,
                expiry_date=date(2027, 11, 20),
            ),
        ]

        session.add_all(medicines)
        session.commit()

        if not all([c.id for c in customers]):
            print("DB Error")
            return None

        orders = [
            Order(
                customer_name="Sakshi",
                customer_phone="9980620823",
                order_date=datetime.now(timezone.utc) - timedelta(days=6),
                customer_id=users[1].id,
                employee_id=employees[0].id,
            ),
            Order(
                customer_name=customers[0].name,
                customer_phone=customers[0].phone,
                order_date=datetime.now(timezone.utc) - timedelta(days=5),
                customer_id=customers[0].id,
                employee_id=employees[0].id,
            ),
            Order(
                customer_name=customers[1].name,
                customer_phone=customers[1].phone,
                order_date=datetime.now(timezone.utc) - timedelta(days=4),
                customer_id=customers[2].id,
                employee_id=employees[1].id,
                discount_type=DiscountType.FIXED,
                discount_value=4,
            ),
            Order(
                customer_name="Aman",
                customer_phone="9890928815",
                order_date=datetime.now(timezone.utc) - timedelta(days=3),
                customer_id=users[1].id,
                employee_id=employees[0].id,
            ),
            Order(
                customer_name="Rakesh",
                customer_phone="8820920811",
                order_date=datetime.now(timezone.utc) - timedelta(days=2),
                customer_id=users[1].id,
                employee_id=employees[1].id,
            ),
            Order(
                customer_name=customers[2].name,
                customer_phone=customers[2].phone,
                order_date=datetime.now(timezone.utc) - timedelta(days=1),
                customer_id=customers[2].id,
                employee_id=employees[0].id,
                discount_type=DiscountType.PERCENTAGE,
                discount_value=5,
            ),
            Order(
                customer_name="Esha",
                customer_phone="8991826817",
                order_date=datetime.now(timezone.utc) - timedelta(days=0),
                customer_id=users[1].id,
                employee_id=employees[1].id,
            ),
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
            CartItem(
                order_id=orders[1].id,
                medicine_id=medicines[2].id,
                quantity=2,
                price=medicines[2].price,
            ),
            CartItem(
                order_id=orders[1].id,
                medicine_id=medicines[3].id,
                quantity=1,
                price=medicines[3].price,
            ),
            CartItem(
                order_id=orders[2].id,
                medicine_id=medicines[4].id,
                quantity=6,
                price=medicines[4].price,
            ),
            CartItem(
                order_id=orders[3].id,
                medicine_id=medicines[5].id,
                quantity=2,
                price=medicines[5].price,
            ),
            CartItem(
                order_id=orders[3].id,
                medicine_id=medicines[6].id,
                quantity=3,
                price=medicines[6].price,
            ),
            CartItem(
                order_id=orders[4].id,
                medicine_id=medicines[7].id,
                quantity=4,
                price=medicines[7].price,
            ),
            CartItem(
                order_id=orders[5].id,
                medicine_id=medicines[8].id,
                quantity=3,
                price=medicines[8].price,
            ),
            CartItem(
                order_id=orders[6].id,
                medicine_id=medicines[9].id,
                quantity=1,
                price=medicines[9].price,
            ),
            CartItem(
                order_id=orders[6].id,
                medicine_id=medicines[10].id,
                quantity=1,
                price=medicines[10].price,
            ),
        ]
        session.add_all(items)
        session.commit()

        appointments = [
            Appointment(
                doctor_id=doctors[0].id,
                visit_fee=doctors[0].consultation_fee,
                customer_id=customers[0].id,
                patient_name=customers[0].name,
                patient_phone=customers[0].phone,
                appointment_date=datetime.now(timezone.utc) - timedelta(days=6),
                appointment_time=time(10, 0),
                status=AppointmentStatus.COMPLETED,
            ),
            Appointment(
                doctor_id=doctors[1].id,
                visit_fee=doctors[1].consultation_fee,
                customer_id=customers[1].id,
                patient_name=customers[1].name,
                patient_phone=customers[1].phone,
                appointment_date=datetime.now(timezone.utc) + timedelta(days=1),
                appointment_time=time(14, 0),
            ),
            Appointment(
                doctor_id=doctors[2].id,
                visit_fee=doctors[2].consultation_fee,
                customer_id=customers[2].id,
                patient_name=customers[2].name,
                patient_phone=customers[2].phone,
                appointment_date=datetime.now(timezone.utc) - timedelta(days=1),
                appointment_time=time(12, 0),
                status=AppointmentStatus.COMPLETED,
            ),
        ]

        session.add_all(appointments)
        session.commit()

        print("Dummy data inserted.")
