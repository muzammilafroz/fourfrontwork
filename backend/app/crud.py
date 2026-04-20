import base64
import mimetypes
import uuid
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import desc, func
from sqlmodel import Session, select

from .auth import get_password_hash
from .models import (
    CartItem,
    Medicine,
    MedicineRequest,
    Order,
    User,
    UserCreate,
    UserRole,
    UserStatus,
)


def save_base64_image(base64_str: str, upload_dir: Path = Path("uploads")) -> str:
    upload_dir.mkdir(parents=True, exist_ok=True)

    header = ""
    base64_string = ""

    if "," in base64_str:
        header, base64_string = base64_str.split(",")

    image_data = base64.b64decode(base64_string)

    try:
        mime_type = header.split(":")[1].split(";")[0]
        extension = mimetypes.guess_extension(mime_type) or ".jpg"
    except Exception:
        extension = ".jpg"

    filename = f"{uuid.uuid4()}{extension}"
    file_path = upload_dir / filename

    with open(file_path, "wb") as f:
        f.write(image_data)

    return str(file_path)


def image_to_base64(file_path: str | Path) -> str:
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist")

    mime_type, _ = mimetypes.guess_type(file_path.name)
    mime_type = mime_type or "image/jpeg"

    with open(file_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime_type};base64,{encoded_string}"


def get_user_by_email(session: Session, email: str) -> User | None:
    query = select(User).where(User.email == email)
    return session.exec(query).first()


def create_user(session: Session, user_in: UserCreate):
    hashed_password = get_password_hash(user_in.password)

    user = User(
        name=user_in.name,
        email=user_in.email,
        phone=user_in.phone,
        hashed_password=hashed_password,
        role=user_in.role,
    )

    if user_in.role == UserRole.EMPLOYEE:
        user.status = UserStatus.INACTIVE

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_low_stock_medicines_db(session: Session, limit: int = 5):
    statement = (
        select(Medicine.name, Medicine.stock_quantity)
        .order_by(Medicine.stock_quantity.asc())
        .limit(limit)
    )
    return session.exec(statement).all()


def get_top_selling_medicines_db(session: Session, limit: int = 5):
    one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)

    total_sold = func.sum(CartItem.quantity).label("total_sold")

    statement = (
        select(Medicine.id, Medicine.name, total_sold)
        .join(CartItem)
        .join(Order)
        .where(Order.order_date >= one_week_ago)
        .group_by(Medicine.id, Medicine.name)
        .order_by(desc(total_sold))
        .limit(limit)
    )

    return session.exec(statement).all()


def get_frequent_requests_db(session: Session, min_requests: int = 3):
    """
    Returns medicine names requested at least `min_requests` times,
    along with their request counts.
    """
    statement = (
        select(
            MedicineRequest.medicine_name,
            func.count(MedicineRequest.id).label("request_count"),
        )
        .group_by(MedicineRequest.medicine_name)
        .having(func.count(MedicineRequest.id) >= min_requests)
        .order_by(desc("request_count"))
    )

    return session.exec(statement).all()


def get_expiring_medicines_db(session: Session, days_buffer: int = 30):
    """
    Returns (medicine_name, expiry_date) for medicines expiring soon.
    """
    today = date.today()
    expiry_threshold = today + timedelta(days=days_buffer)

    statement = (
        select(Medicine.name, Medicine.expiry_date)
        .where(
            Medicine.expiry_date >= today,
            Medicine.expiry_date <= expiry_threshold,
        )
        .order_by(Medicine.expiry_date)
    )

    return session.exec(statement).all()
