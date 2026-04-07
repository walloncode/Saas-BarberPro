from app.extensions import db
from datetime import datetime


class BarberShop(db.Model):
    __tablename__ = "barber_shops"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.String(200))
    logo_url = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship("User", backref="barber_shop", lazy=True)
    clients = db.relationship("Client", backref="barber_shop", lazy=True)
    barbers = db.relationship("Barber", backref="barber_shop", lazy=True)
    services = db.relationship("Service", backref="barber_shop", lazy=True)
    appointments = db.relationship("Appointment", backref="barber_shop", lazy=True)
    payments = db.relationship("Payment", backref="barber_shop", lazy=True)

    def __repr__(self):
        return f"<BarberShop {self.name}>"
