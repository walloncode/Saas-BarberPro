from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app.utils.decorators import tenant_required
from app.extensions import db
from app.models.payment import Payment
from app.models.appointment import Appointment

payments_bp = Blueprint("payments", __name__)


@payments_bp.route("/pagamentos")
@login_required
@tenant_required
def index():
    payments = (
        Payment.query.filter_by(barber_shop_id=current_user.barber_shop_id)
        .order_by(Payment.created_at.desc())
        .all()
    )
    return render_template("payments/index.html", payments=payments)


@payments_bp.route("/pagamentos/registrar", methods=["POST"])
@login_required
@tenant_required
def create():
    appointment_id = request.form.get("appointment_id", type=int)
    method = request.form.get("method", "cash")

    appointment = Appointment.query.filter_by(
        id=appointment_id, barber_shop_id=current_user.barber_shop_id
    ).first_or_404()

    payment = Payment(
        barber_shop_id=current_user.barber_shop_id,
        appointment_id=appointment_id,
        amount=appointment.service.price,
        method=method,
        status="paid",
        paid_at=datetime.utcnow(),
    )
    db.session.add(payment)
    appointment.status = "completed"
    appointment.client.visits_count += 1
    db.session.commit()
    flash("Pagamento registrado!", "success")
    return redirect(url_for("payments.index"))


@payments_bp.route("/pagamentos/<int:id>/estornar", methods=["POST"])
@login_required
@tenant_required
def refund(id):
    payment = Payment.query.filter_by(
        id=id, barber_shop_id=current_user.barber_shop_id
    ).first_or_404()

    if payment.status == "paid":
        payment.status = "refunded"
        db.session.commit()
        flash("Pagamento estornado.", "warning")
    else:
        flash("Não foi possivel estornar.", "danger")

    return redirect(url_for("payments.index"))
