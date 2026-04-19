from langchain_core.tools import tool
from sqlmodel import Session

from .crud import (
    get_expiring_medicines_db,
    get_frequent_requests_db,
    get_low_stock_medicines_db,
    get_top_selling_medicines_db,
)
from .database import engine


@tool
def get_low_stock_medicines() -> str:
    """Returns a readable list of low stock medicines."""
    try:
        with Session(engine) as session:
            medicines = get_low_stock_medicines_db(session)

            if not medicines:
                return "No medicines are low on stock."

            return "\n".join(f"{name} (Stock: {stock})" for name, stock in medicines)
    except Exception as e:
        return f"Error fetching low stock medicines: {str(e)}"


@tool
def get_top_selling_medicines(limit: int = 5):
    """Returns the top N selling medicines based on quantity sold in the last 7 days."""
    try:
        with Session(engine) as session:
            results = get_top_selling_medicines_db(session, limit)

            if not results:
                return "No sales found in the last 7 days."

            lines = ["Top selling medicines (last 7 days):"]
            for i, (_, name, total) in enumerate(results, start=1):
                lines.append(f"{i}. {name} — {int(total or 0)} units sold")

            return "\n".join(lines)

    except Exception as e:
        return f"Error fetching top selling medicines: {str(e)}"


@tool
def get_frequent_requests(min_requests: int = 3) -> str:
    """
    Returns a human-readable string of frequently requested medicines.
    """
    try:
        with Session(engine) as session:
            results = get_frequent_requests_db(session, min_requests)

        if not results:
            return "No frequently requested medicines found."

        lines = [
            f"{idx + 1}. {name} — {count} requests"
            for idx, (name, count) in enumerate(results)
        ]

        return "Frequently requested medicines:\n" + "\n".join(lines)

    except Exception as e:
        return f"Error fetching frequent requests: {str(e)}"


@tool
def get_expiring_medicines(days_buffer: int = 30) -> str:
    """
    Returns a human-readable string of medicines expiring soon.
    """
    try:
        with Session(engine) as session:
            results = get_expiring_medicines_db(session, days_buffer)

        if not results:
            return f"No medicines expiring in the next {days_buffer} days."

        lines = [
            f"{idx + 1}. {name} — expires on {expiry_date}"
            for idx, (name, expiry_date) in enumerate(results)
        ]

        return f"Medicines expiring in the next {days_buffer} days:\n" + "\n".join(
            lines
        )

    except Exception as e:
        return f"Error fetching expiring medicines: {str(e)}"
