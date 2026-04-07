from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.decorators import tenant_required
from app.extensions import db
from app.models.service import Service

services_bp = Blueprint("services", __name__)


@services_bp.route("/servicos")
@login_required
@tenant_required
def index():
    items = Service.query.filter_by(
        barber_shop_id=current_user.barber_shop_id
    ).order_by(Service.name).all()
    return render_template("services/index.html", services=items)


@services_bp.route("/servicos/criar", methods=["POST"])
@login_required
@tenant_required
def create():
    name = request.form.get("name", "").strip()
    price = request.form.get("price", type=float)
    duration = request.form.get("duration_minutes", type=int)

    if not name or price is None or duration is None:
        flash("Preencha todos os campos.", "danger")
        return redirect(url_for("services.index"))

    if price < 0 or duration <= 0:
        flash("Preco e duracao devem ser validos.", "danger")
        return redirect(url_for("services.index"))

    service = Service(
        barber_shop_id=current_user.barber_shop_id,
        name=name,
        price=price,
        duration_minutes=duration,
    )
    db.session.add(service)
    db.session.commit()
    flash("Servico criado!", "success")
    return redirect(url_for("services.index"))


@services_bp.route("/servicos/<int:id>/editar", methods=["POST"])
@login_required
@tenant_required
def edit(id):
    service = Service.query.filter_by(
        id=id, barber_shop_id=current_user.barber_shop_id
    ).first_or_404()

    service.name = request.form.get("name", "").strip()
    price = request.form.get("price", type=float)
    duration = request.form.get("duration_minutes", type=int)

    if price is not None and duration is not None:
        service.price = price
        service.duration_minutes = duration
        service.is_active = request.form.get("is_active") == "on"

        db.session.commit()
        flash("Servico atualizado!", "success")
    else:
        flash("Preencha todos os campos.", "danger")

    return redirect(url_for("services.index"))


@services_bp.route("/servicos/<int:id>/excluir", methods=["POST"])
@login_required
@tenant_required
def delete(id):
    service = Service.query.filter_by(
        id=id, barber_shop_id=current_user.barber_shop_id
    ).first_or_404()
    db.session.delete(service)
    db.session.commit()
    flash("Servico removido.", "info")
    return redirect(url_for("services.index"))
