from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app.utils.decorators import tenant_required
from app.extensions import db
from app.models.appointment import Appointment
from app.models.client import Client
from app.models.barber import Barber
from app.models.service import Service
from app.services.appointment_service import AppointmentService

appointments_bp = Blueprint("appointments", __name__)


@appointments_bp.route("/agendamentos")
@login_required
@tenant_required
def index():
    shop_id = current_user.barber_shop_id
    date_filter = request.args.get("date")
    query = Appointment.query.filter_by(barber_shop_id=shop_id)

    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
            query = query.filter_by(date=filter_date)
        except ValueError:
            pass

    appointments = (
        query.order_by(Appointment.date.desc(), Appointment.start_time.desc()).all()
    )
    clients = Client.query.filter_by(barber_shop_id=shop_id, is_active=True).all()
    barbers = Barber.query.filter_by(barber_shop_id=shop_id, is_active=True).all()
    services = Service.query.filter_by(barber_shop_id=shop_id, is_active=True).all()
    return render_template(
        "appointments/index.html",
        appointments=appointments,
        clients=clients,
        barbers=barbers,
        services=services,
    )


@appointments_bp.route("/agendamentos/criar", methods=["POST"])
@login_required
@tenant_required
def create():
    barber_id = request.form.get("barber_id", type=int)
    client_id = request.form.get("client_id", type=int)
    service_id = request.form.get("service_id", type=int)
    date_str = request.form.get("date")
    time_str = request.form.get("start_time")

    if not all([barber_id, client_id, service_id, date_str, time_str]):
        flash("Preencha todos os campos.", "danger")
        return redirect(url_for("appointments.index"))

    service = Service.query.filter_by(
        id=service_id, barber_shop_id=current_user.barber_shop_id
    ).first_or_404()

    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    start_time = datetime.strptime(time_str, "%H:%M").time()

    appointment = Appointment(
        barber_shop_id=current_user.barber_shop_id,
        barber_id=barber_id,
        client_id=client_id,
        service_id=service_id,
        user_id=current_user.id,
        date=date,
        start_time=start_time,
    )

    result, error = AppointmentService.create_appointment(appointment)
    if error:
        flash(error, "danger")
    else:
        db.session.commit()
        flash("Agendamento criado com sucesso!", "success")

    return redirect(url_for("appointments.index"))


@appointments_bp.route("/agendamentos/<int:id>/cancelar", methods=["POST"])
@login_required
@tenant_required
def cancel(id):
    appointment = Appointment.query.filter_by(
        id=id, barber_shop_id=current_user.barber_shop_id
    ).first_or_404()

    success, error = AppointmentService.cancel_appointment(appointment)
    db.session.commit()

    if error:
        flash(error, "warning")
    else:
        flash("Agendamento cancelado.", "info")

    return redirect(url_for("appointments.index"))
