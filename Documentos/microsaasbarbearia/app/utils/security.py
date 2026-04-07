from flask import request, session, abort
from datetime import datetime, timedelta

LOGIN_ATTEMPT_KEY = "login_attempts"
LOGIN_LOCKOUT_KEY = "login_lockout"
MAX_ATTEMPTS = 5
LOCKOUT_MINUTES = 15


def security_headers(response):
    """Aplica headers de seguranca HTTP."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Cache-Control"] = "no-store"
    return response


def check_rate_limit(session_store):
    """Verifica se o usuario atingiu o limite de tentativas de login."""
    now = datetime.utcnow()
    lockout_time = session_store.get(LOGIN_LOCKOUT_KEY)

    if lockout_time:
        lockout_dt = datetime.fromisoformat(lockout_time)
        if now < lockout_dt + timedelta(minutes=LOCKOUT_MINUTES):
            remaining = (lockout_dt + timedelta(minutes=LOCKOUT_MINUTES) - now).seconds // 60
            return False, f"Muitas tentativas. Tente em {remaining} minutos."
        else:
            session_store.pop(LOGIN_LOCKOUT_KEY, None)
            session_store.pop(LOGIN_ATTEMPT_KEY, None)

    attempts = session_store.get(LOGIN_ATTEMPT_KEY, 0)
    if attempts >= MAX_ATTEMPTS:
        session_store[LOGIN_LOCKOUT_KEY] = now.isoformat()
        return False, f"Conta bloqueada por {LOCKOUT_MINUTES} minutos."

    session_store[LOGIN_ATTEMPT_KEY] = attempts + 1
    return True, ""


def record_failed_login(session_store):
    """Registra tentativa falha de login."""
    attempts = session_store.get(LOGIN_ATTEMPT_KEY, 0) + 1
    session_store[LOGIN_ATTEMPT_KEY] = attempts


def record_successful_login(session_store):
    """Limpa contadores de login apos sucesso."""
    session_store.pop(LOGIN_ATTEMPT_KEY, None)
    session_store.pop(LOGIN_LOCKOUT_KEY, None)
