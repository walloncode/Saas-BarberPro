from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from app.utils.decorators import tenant_required
from app.extensions import db
from app.models.client import Client
from app.services.export_service import export_clients_csv

clients_bp = Blueprint("clients", __name__)


@clients_bp.route("/clientes")
@login_required
@tenant_required
def index():
    shop_id = current_user.barber_shop_id
    search = request.args.get("q", "").strip()
    query = Client.query.filter_by(barber_shop_id=shop_id, is_active=True)
    if search:
        query = query.filter(Client.name.ilike(f"%{search}%"))
    clients = query.order_by(Client.created_at.desc()).all()
    return render_template("clients/index.html", clients=clients, search=search)


@clients_bp.route("/clientes/criar", methods=["POST"])
@login_required
@tenant_required
def create():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    cpf = request.form.get("cpf", "").strip()

    if not name:
        flash("Nome e obrigatorio.", "danger")
        return redirect(url_for("clients.index"))

    client = Client(
        barber_shop_id=current_user.barber_shop_id,
        name=name,
        phone=phone,
        email=email,
        cpf=cpf,
    )
    db.session.add(client)
    db.session.commit()
    flash("Cliente criado com sucesso!", "success")
    return redirect(url_for("clients.index"))


@clients_bp.route("/clientes/<int:id>/editar", methods=["POST"])
@login_required
@tenant_required
def edit(id):
    client = Client.query.filter_by(
        id=id, barber_shop_id=current_user.barber_shop_id
    ).first_or_404()

    client.name = request.form.get("name", "").strip()
    client.phone = request.form.get("phone", "").strip()
    client.email = request.form.get("email", "").strip()
    client.cpf = request.form.get("cpf", "").strip()
    client.notes = request.form.get("notes", "").strip()

    if not client.name:
        flash("Nome e obrigatorio.", "danger")
    else:
        db.session.commit()
        flash("Cliente atualizado!", "success")

    return redirect(url_for("clients.index"))


@clients_bp.route("/clientes/<int:id>/excluir", methods=["POST"])
@login_required
@tenant_required
def delete(id):
    client = Client.query.filter_by(
        id=id, barber_shop_id=current_user.barber_shop_id
    ).first_or_404()
    db.session.delete(client)
    db.session.commit()
    flash("Cliente removido.", "info")
    return redirect(url_for("clients.index"))


@clients_bp.route("/clientes/<int:id>/toggle-status", methods=["POST"])
@login_required
@tenant_required
def toggle_status(id):
    client = Client.query.filter_by(
        id=id, barber_shop_id=current_user.barber_shop_id
    ).first_or_404()

    client.is_active = not client.is_active
    db.session.commit()

    status = "ativado" if client.is_active else "desativado"
    flash(f"Cliente {status}.", "info")
    return redirect(url_for("clients.index"))


@clients_bp.route("/clientes/exportar")
@login_required
@tenant_required
def export_csv():
    clients = Client.query.filter_by(
        barber_shop_id=current_user.barber_shop_id
    ).order_by(Client.name).all()
    csv_data = export_clients_csv(clients)
    resp = make_response(csv_data)
    resp.headers["Content-Type"] = "text/csv; charset=utf-8"
    resp.headers["Content-Disposition"] = "attachment; filename=clientes.csv"
    return resp
