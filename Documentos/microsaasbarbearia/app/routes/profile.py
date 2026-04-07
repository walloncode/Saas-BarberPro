import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.user import User
from app.models.barber_shop import BarberShop

profile_bp = Blueprint("profile", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@profile_bp.route("/perfil")
@login_required
def index():
    shop = BarberShop.query.get(current_user.barber_shop_id)
    return render_template("profile/index.html", shop=shop)


@profile_bp.route("/perfil/atualizar", methods=["POST"])
@login_required
def update():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")

    if name:
        current_user.name = name
    if email and email != current_user.email:
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("Email ja esta em uso.", "danger")
            return redirect(url_for("profile.index"))
        current_user.email = email

    if current_password and new_password:
        if not current_user.check_password(current_password):
            flash("Senha atual incorreta.", "danger")
            return redirect(url_for("profile.index"))
        if len(new_password) < 6:
            flash("Nova senha deve ter pelo menos 6 caracteres.", "danger")
            return redirect(url_for("profile.index"))
        current_user.set_password(new_password)
        flash("Senha atualizada!", "success")

    db.session.commit()

    # Profile photo upload
    file = request.files.get("photo")
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_dir = os.path.join(current_app.root_path, "..", "uploads", "avatars")
        os.makedirs(upload_dir, exist_ok=True)
        # User-specific filename
        ext = os.path.splitext(filename)[1]
        photo_filename = f"user_{current_user.id}{ext}"
        dest = os.path.join(upload_dir, photo_filename)
        file.save(dest)
        current_user.photo_url = f"/uploads/avatars/{photo_filename}"
        db.session.commit()

    if not (current_password and new_password):
        flash("Perfil atualizado!", "success")
    return redirect(url_for("profile.index"))


@profile_bp.route("/perfil/barbearia", methods=["POST"])
@login_required
def update_shop():
    shop = BarberShop.query.get(current_user.barber_shop_id)
    if not shop:
        flash("Barbearia nao encontrada.", "danger")
        return redirect(url_for("profile.index"))

    shop.name = request.form.get("shop_name", "").strip()
    shop.phone = request.form.get("shop_phone", "").strip()
    shop.email = request.form.get("shop_email", "").strip()
    shop.address = request.form.get("shop_address", "").strip()

    # Shop logo upload
    file = request.files.get("logo")
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_dir = os.path.join(current_app.root_path, "..", "uploads", "logos")
        os.makedirs(upload_dir, exist_ok=True)
        ext = os.path.splitext(filename)[1]
        logo_filename = f"shop_{shop.id}{ext}"
        dest = os.path.join(upload_dir, logo_filename)
        file.save(dest)
        shop.logo_url = f"/uploads/logos/{logo_filename}"

    db.session.commit()
    flash("Dados da barbearia atualizados!", "success")
    return redirect(url_for("profile.index"))
