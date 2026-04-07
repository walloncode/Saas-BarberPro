from flask import Blueprint, request, jsonify
from flask_login import login_user
from datetime import datetime
from app.extensions import db
from app.models.user import User
from app.models.appointment import Appointment
from app.models.client import Client
from app.models.service import Service
from app.services.appointment_service import AppointmentService

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/login", methods=["POST"])
def api_login():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email e senha sao obrigatorios."}), 400

    user = User.query.filter_by(email=data["email"]).first()

    if user and user.check_password(data["password"]):
        login_user(user)
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        })

    return jsonify({"error": "Credenciais invalidas."}), 401


@api_bp.route("/appointments", methods=["GET"])
def api_appointments_list():
    from flask_login import current_user
    if not current_user.is_authenticated:
        return jsonify({"error": "Nao autenticado"}), 401

    shop_id = current_user.barber_shop_id
    apts = Appointment.query.filter_by(barber_shop_id=shop_id).all()
    return jsonify([{
        "id": a.id,
        "client": a.client.name,
        "barber": a.barber.name,
        "service": a.service.name,
        "date": a.date.strftime("%Y-%m-%d"),
        "start_time": a.start_time.strftime("%H:%M"),
        "status": a.status,
    } for a in apts])


@api_bp.route("/appointments", methods=["POST"])
def api_appointments_create():
    from flask_login import current_user
    if not current_user.is_authenticated:
        return jsonify({"error": "Nao autenticado"}), 401

    data = request.get_json()
    if not all(k in data for k in ("barber_id", "client_id", "service_id", "date", "start_time")):
        return jsonify({"error": "Campos obrigatorios faltando."}), 400

    service = Service.query.filter_by(
        id=data["service_id"], barber_shop_id=current_user.barber_shop_id
    ).first()
    if not service:
        return jsonify({"error": "Servico nao encontrado."}), 404

    date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    start_time = datetime.strptime(data["start_time"], "%H:%M").time()

    appointment = Appointment(
        barber_shop_id=current_user.barber_shop_id,
        barber_id=data["barber_id"],
        client_id=data["client_id"],
        service_id=data["service_id"],
        user_id=current_user.id,
        date=date,
        start_time=start_time,
    )

    result, error = AppointmentService.create_appointment(appointment)
    if error:
        return jsonify({"error": error}), 409

    db.session.commit()
    return jsonify({"id": result.id, "message": "Agendamento criado."}), 201


@api_bp.route("/appointments/<int:id>", methods=["DELETE"])
def api_appointments_delete(id):
    from flask_login import current_user
    if not current_user.is_authenticated:
        return jsonify({"error": "Nao autenticado"}), 401

    appointment = Appointment.query.filter_by(
        id=id, barber_shop_id=current_user.barber_shop_id
    ).first_or_404()

    success, error = AppointmentService.cancel_appointment(appointment)
    db.session.commit()

    if error:
        return jsonify({"error": error}), 400

    return jsonify({"message": "Agendamento cancelado."})


@api_bp.route("/clients", methods=["GET"])
def api_clients_list():
    from flask_login import current_user
    if not current_user.is_authenticated:
        return jsonify({"error": "Nao autenticado"}), 401

    clients = Client.query.filter_by(
        barber_shop_id=current_user.barber_shop_id
    ).all()

    return jsonify([{
        "id": c.id,
        "name": c.name,
        "phone": c.phone,
        "email": c.email,
        "visits_count": c.visits_count,
    } for c in clients])


@api_bp.route("/clients", methods=["POST"])
def api_clients_create():
    from flask_login import current_user
    if not current_user.is_authenticated:
        return jsonify({"error": "Nao autenticado"}), 401

    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "Nome e obrigatorio."}), 400

    client = Client(
        barber_shop_id=current_user.barber_shop_id,
        name=data["name"],
        phone=data.get("phone"),
        email=data.get("email"),
        cpf=data.get("cpf"),
    )
    db.session.add(client)
    db.session.commit()
    return jsonify({"id": client.id, "message": "Cliente criado."}), 201
