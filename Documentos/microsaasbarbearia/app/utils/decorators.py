from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user


def tenant_required(f):
    """Garante que o usuario pertence a uma barbearia ativa."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        if not current_user.barber_shop_id:
            flash("Usuario nao possui uma barbearia associada.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def role_required(required_role):
    """Restringe acesso por papel: admin."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role != required_role:
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator
