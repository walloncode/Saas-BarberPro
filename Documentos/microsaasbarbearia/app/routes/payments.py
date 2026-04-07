from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from datetime import datetime
from app.utils.decorators import tenant_required
from app.extensions import db
from app.models.payment import Payment
from app.models.appointment import Appointment
from app.services.mercadopago import create_preference, handle_webhook

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
    pending = (
        Appointment.query.filter_by(
            barber_shop_id=current_user.barber_shop_id, status="scheduled"
        )
        .order_by(Appointment.date.desc(), Appointment.start_time.desc())
        .all()
    )
    return render_template(
        "payments/index.html",
        payments=payments,
        pending_appointments=pending,
    )


@payments_bp.route("/pagamentos/registrar", methods=["POST"])
@login_required
@tenant_required
def create():
    appointment_id = request.form.get("appointment_id", type=int)
    method = request.form.get("method", "cash")

    if not appointment_id:
        flash("Selecione um agendamento.", "warning")
        return redirect(url_for("payments.index"))

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


@payments_bp.route("/pagamentos/criar-checkout", methods=["POST"])
@login_required
@tenant_required
def create_checkout():
    """Create a Mercado Pago checkout preference and redirect to payment."""
    appointment_id = request.form.get("appointment_id", type=int)

    appointment = Appointment.query.filter_by(
        id=appointment_id, barber_shop_id=current_user.barber_shop_id
    ).first_or_404()

    try:
        base_url = request.host_url.rstrip("/")
        preference = create_preference(
            items=[{
                "title": f"Servico: {appointment.service.name}",
                "unit_price": float(appointment.service.price),
                "quantity": 1,
            }],
            back_urls={
                "success": f"{base_url}/pagamentos/sucesso",
                "failure": f"{base_url}/pagamentos/falha",
                "pending": f"{base_url}/pagamentos",
            },
            metadata={
                "appointment_id": appointment_id,
                "barber_shop_id": current_user.barber_shop_id,
                "user_id": current_user.id,
            },
        )
        return redirect(preference["init_point"])
    except Exception as e:
        current_app.logger.error(f"Erro ao criar checkout MP: {e}")
        flash("Erro ao criar pagamento online.", "danger")
        return redirect(url_for("payments.index"))


@payments_bp.route("/pagamentos/sucesso")
@login_required
def success():
    flash("Pagamento aprovado com sucesso!", "success")
    return redirect(url_for("payments.index"))


@payments_bp.route("/pagamentos/falha")
@login_required
def failure():
    flash("Pagamento nao aprovado. Tente novamente.", "danger")
    return redirect(url_for("payments.index"))


@payments_bp.route("/webhook/mercadopago", methods=["POST"])
def webhook_mercadopago():
    """Receive Mercado Pago webhook notifications (no auth/CSRF)."""
    data = request.get_json() or request.form.to_dict()

    try:
        result = handle_webhook(data)
        if result and result["status"] == "approved":
            payment_id = result["payment_id"]

            existing = Payment.query.filter_by(
                mercadopago_id=str(payment_id)
            ).first()
            if existing:
                return jsonify({"status": "ok"}), 200

            metadata = result.get("metadata", {})
            payment = Payment(
                barber_shop_id=metadata.get("barber_shop_id", 0),
                amount=result.get("transaction_amount", 0),
                method="mercadopago",
                status="paid",
                paid_at=datetime.utcnow(),
                mercadopago_id=str(payment_id),
            )
            db.session.add(payment)
            db.session.commit()
            return jsonify({"status": "ok"}), 200

        return jsonify({"status": "ignored"}), 200
    except Exception as e:
        current_app.logger.error(f"Erro no webhook MP: {e}")
        return jsonify({"status": "error"}), 500
