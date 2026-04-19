import base64
import mimetypes
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import desc, func, select
from sqlmodel import Session, select

from .auth import get_password_hash
from .models import CartItem, Medicine, Order, User, UserCreate, UserRole, UserStatus


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
    statement = select(Medicine).order_by(Medicine.stock_quantity.asc()).limit(limit)
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
