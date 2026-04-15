from datetime import date, datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from ..database import get_session
from ..models import (
    Appointment,
    AppointmentStatus,
    CartItem,
    Doctor,
    Feedback,
    Medicine,
    MedicineRequest,
    Order,
    RequestStatus,
)

router = APIRouter(prefix="/overview", tags=["Dashboard"])


@router.get("")
def role_overview(db: Session = Depends(get_session)):
    today = datetime.now().date()
    last_7_days = today - timedelta(days=6)

    # Total Sales Today
    total_sales = (
        db.query(func.coalesce(func.sum(CartItem.price * CartItem.quantity), 0))
        .join(Order, CartItem.order_id == Order.id)
        .filter(func.date(Order.order_date) == today)
        .scalar()
    )

    total_medicines = db.query(Medicine).count()

    pending_requests = (
        db.query(MedicineRequest)
        .filter(MedicineRequest.status == RequestStatus.PENDING)
        .count()
    )

    # Appointments Today
    appointments_today = (
        db.query(Appointment).filter(Appointment.appointment_date == today).count()
    )

    # Completed Appointments Today (equivalent to 'visited')
    visited_today = (
        db.query(Appointment)
        .filter(
            Appointment.appointment_date == today,
            Appointment.status == AppointmentStatus.COMPLETED,
        )
        .count()
    )

    # Average rating
    avg_rating = db.query(func.avg(Feedback.rating)).scalar() or 0
    avg_rating = round(float(avg_rating), 1)

    # Sales for last 7 days
    sales_map = {(today - timedelta(days=i)): float(0) for i in range(7)}

    recent_orders: list = (
        db.query(
            func.date(Order.order_date).label("date"),
            func.coalesce(func.sum(CartItem.price * CartItem.quantity), 0).label(
                "daily_total"
            ),
        )
        .join(CartItem, CartItem.order_id == Order.id)
        .filter(Order.order_date >= datetime.combine(last_7_days, datetime.min.time()))
        .group_by(func.date(Order.order_date))
        .order_by(func.date(Order.order_date))
        .all()
    )

    for row in recent_orders:
        row_date = date.fromisoformat(row.date)
        if row_date in sales_map.keys():
            sales_map[row_date] = float(row.daily_total)

    sales_time = [
        {"date": d.strftime("%m-%d"), "total": sales_map[d]}
        for d in sorted(sales_map.keys())
    ]

    # Top 5 demanded medicines (Joining Order -> CartItem -> Medicine)
    medicine_demand = (
        db.query(Medicine.name, func.sum(CartItem.quantity).label("total_qty"))
        .join(CartItem, Medicine.id == CartItem.medicine_id)
        .group_by(Medicine.id)
        .order_by(func.sum(CartItem.quantity).desc())
        .limit(5)
        .all()
    )

    demand = [{"name": m.name[:15], "qty": int(m.total_qty)} for m in medicine_demand]

    # Inventory stats
    out_of_stock = db.query(Medicine).filter(Medicine.stock_quantity == 0).count()
    low_stock = (
        db.query(Medicine)
        .filter(Medicine.stock_quantity > 0, Medicine.stock_quantity <= 100)
        .count()
    )
    in_stock = db.query(Medicine).filter(Medicine.stock_quantity > 100).count()

    inventory = [
        {"name": "Out of Stock", "value": out_of_stock},
        {"name": "Low Stock", "value": low_stock},
        {"name": "In Stock", "value": in_stock},
    ]

    # Rating Distribution (Since mood/category aren't in your Feedback model)
    rating_data = (
        db.query(Feedback.rating, func.count(Feedback.id).label("count"))
        .group_by(Feedback.rating)
        .all()
    )

    rating_dist = [{"name": f"{r.rating} Stars", "count": r.count} for r in rating_data]

    # Doctor performance (Appointments)
    doctor_stats = (
        db.query(
            Doctor.name,
            func.count(Appointment.id).label("total"),
            func.sum(
                case(
                    (Appointment.status == AppointmentStatus.COMPLETED, 1),
                    else_=0,
                )
            ).label("completed"),
        )
        .join(Appointment)
        .group_by(Doctor.id, Doctor.name)  # include name in group_by
        .limit(10)
        .all()
    )

    doctor_visits = [
        {
            "name": d.name[:10],
            "visited": int(d.completed or 0),
            "notVisited": int(d.total - (d.completed or 0)),
        }
        for d in doctor_stats
    ]

    return {
        "stats": {
            "totalSales": float(total_sales),
            "totalMedicines": total_medicines,
            "pendingRequests": pending_requests,
            "appointmentsToday": appointments_today,
            "visitedToday": visited_today,
            "avgRating": avg_rating,
        },
        "charts": {
            "salesTime": sales_time,
            "demand": demand,
            "inventory": inventory,
            "ratingDistribution": rating_dist,
            "doctorVisits": doctor_visits,
        },
    }
