from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app.extensions import db
from app.models.appointment import Appointment
from app.models.client import Client
from app.models.barber import Barber
from app.models.payment import Payment
from app.utils.decorators import tenant_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
@tenant_required
def index():
    shop_id = get_shop_id()
    today = datetime.today().date()

    today_appointments = (
        Appointment.query.filter_by(barber_shop_id=shop_id, date=today, status="scheduled")
        .order_by(Appointment.start_time)
        .all()
    )

    today_revenue = (
        Payment.query.filter_by(barber_shop_id=shop_id, status="paid")
        .filter(Payment.paid_at >= datetime(today.year, today.month, today.day))
        .all()
    )
    total_revenue = sum(float(p.amount) for p in today_revenue)

    this_week = today - timedelta(days=today.weekday())
    new_clients = Client.query.filter(
        Client.barber_shop_id == shop_id, Client.created_at >= this_week
    ).count()

    active_barbers = Barber.query.filter_by(barber_shop_id=shop_id, is_active=True).count()

    # Chart data: last 7 days revenue
    chart_labels = []
    chart_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_label = day.strftime("%d/%m")
        day_payments = Payment.query.filter(
            Payment.barber_shop_id == shop_id,
            Payment.status == "paid",
            db.cast(Payment.paid_at, db.Date) == day,
        ).all()
        day_total = sum(float(p.amount) for p in day_payments)
        chart_labels.append(day_label)
        chart_data.append(day_total)

    return render_template(
        "dashboard/index.html",
        today_appointments=today_appointments,
        total_revenue=total_revenue,
        new_clients=new_clients,
        active_barbers=active_barbers,
        chart_labels=chart_labels,
        chart_data=chart_data,
    )


def get_shop_id():
    return current_user.barber_shop_id
