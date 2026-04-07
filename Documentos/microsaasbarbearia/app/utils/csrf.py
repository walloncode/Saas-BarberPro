"""CSRF utilities for use without full FlaskForm classes."""
from flask import session, request, current_app, abort
from flask_wtf.csrf import generate_csrf, validate_csrf
from itsdangerous import BadData


def csrf_field():
    """Returns the HTML hidden input with CSRF token."""
    token = generate_csrf()
    return f'<input type="hidden" name="csrf_token" value="{token}">'


def validate_request_csrf():
    """Validates CSRF token from form data."""
    token = request.form.get("csrf_token")
    if not token:
        abort(403, description="CSRF token missing.")

    try:
        validate_csrf(token)
    except BadData:
        abort(403, description="Invalid CSRF token.")
