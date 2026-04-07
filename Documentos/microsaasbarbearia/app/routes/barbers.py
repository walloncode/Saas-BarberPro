from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.decorators import tenant_required
from app.extensions import db
from app.models.barber import Barber

barbers_bp = Blueprint("barbers", __name__)


@barbers_bp.route("/barbeiros")
@login_required
@tenant_required
def index():
    shop_id = current_user.barber_shop_id
    barbers = Barber.query.filter_by(barber_shop_id=shop_id).all()
    return render_template("barbers/index.html", barbers=barbers)


@barbers_bp.route("/barbeiros/criar", methods=["POST"])
@login_required
@tenant_required
def create():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()

    if not name:
        flash("Nome e obrigatorio.", "danger")
        return redirect(url_for("barbers.index"))

    barber = Barber(
        barber_shop_id=current_user.barber_shop_id,
        name=name,
        phone=phone,
    )
    db.session.add(barber)
    db.session.commit()
    flash("Barbeiro criado com sucesso!", "success")
    return redirect(url_for("barbers.index"))


@barbers_bp.route("/barbeiros/<int:id>/editar", methods=["POST"])
@login_required
@tenant_required
def edit(id):
    barber = Barber.query.filter_by(
        id=id, barber_shop_id=current_user.barber_shop_id
    ).first_or_404()

    barber.name = request.form.get("name", "").strip()
    barber.phone = request.form.get("phone", "").strip()
    barber.is_active = request.form.get("is_active") == "on"

    if not barber.name:
        flash("Nome e obrigatorio.", "danger")
    else:
        db.session.commit()
        flash("Barbeiro atualizado!", "success")

    return redirect(url_for("barbers.index"))


@barbers_bp.route("/barbeiros/<int:id>/excluir", methods=["POST"])
@login_required
@tenant_required
def delete(id):
    barber = Barber.query.filter_by(
        id=id, barber_shop_id=current_user.barber_shop_id
    ).first_or_404()
    db.session.delete(barber)
    db.session.commit()
    flash("Barbeiro removido.", "info")
    return redirect(url_for("barbers.index"))
