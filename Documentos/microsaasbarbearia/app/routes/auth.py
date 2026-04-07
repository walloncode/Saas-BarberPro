from flask import Blueprint, render_template, redirect, url_for, request, flash, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User
from app.models.barber_shop import BarberShop
from app.utils.security import check_rate_limit, record_failed_login, record_successful_login

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        allowed, message = check_rate_limit(session)
        if not allowed:
            flash(message, "danger")
            return render_template("auth/login.html"), 429

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password) and user.is_active:
            record_successful_login(session)
            login_user(user)
            session["barber_shop_id"] = user.barber_shop_id
            flash("Login realizado com sucesso!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard.index"))

        record_failed_login(session)
        flash("Email ou senha invalidos.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        shop_name = request.form.get("shop_name", "").strip()
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not all([shop_name, name, email, password]):
            flash("Preencha todos os campos.", "danger")
            return render_template("auth/register.html"), 400

        if password != confirm:
            flash("As senhas nao coincidem.", "danger")
            return render_template("auth/register.html"), 400

        if len(password) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "danger")
            return render_template("auth/register.html"), 400

        if User.query.filter_by(email=email).first():
            flash("Este email ja esta em uso.", "danger")
            return render_template("auth/register.html"), 400

        shop = BarberShop(name=shop_name, email=email)
        db.session.add(shop)
        db.session.flush()

        user = User(
            barber_shop_id=shop.id,
            name=name,
            email=email,
            role="admin",
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        session["barber_shop_id"] = shop.id
        flash("Barbearia e conta criadas com sucesso!", "success")
        return redirect(url_for("dashboard.index"))

    return render_template("auth/register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("barber_shop_id", None)
    flash("Logout realizado.", "info")
    return redirect(url_for("auth.login"))
