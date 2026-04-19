from langchain_core.tools import tool
from sqlmodel import Session

from .crud import get_low_stock_medicines_db, get_top_selling_medicines_db
from .database import engine


@tool
def get_low_stock_medicines() -> str:
    """Returns a readable list of low stock medicines."""
    with Session(engine) as session:
        medicines = get_low_stock_medicines_db(session)

        if not medicines:
            return "No medicines are low on stock."

        return "\n".join(f"{m.name} (Stock: {m.stock_quantity})" for m in medicines)


@tool
def get_top_selling_medicines(limit: int = 5):
    """Returns the top N selling medicines based on quantity sold in the last 7 days."""
    try:
        with Session(engine) as session:
            results = get_top_selling_medicines_db(session, limit)

            return [
                {
                    "medicine_id": mid,
                    "name": name,
                    "total_sold": int(total or 0),
                }
                for mid, name, total in results
            ]
    except Exception as e:
        return {"error": str(e)}
