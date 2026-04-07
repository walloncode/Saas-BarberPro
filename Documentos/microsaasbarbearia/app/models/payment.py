from app.extensions import db
from datetime import datetime

PAYMENT_METHODS = ("cash", "card", "pix")
PAYMENT_STATUSES = ("pending", "paid", "refunded")


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    barber_shop_id = db.Column(db.Integer, db.ForeignKey("barber_shops.id"), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    method = db.Column(db.String(20), nullable=False, default="cash")
    status = db.Column(db.String(20), nullable=False, default="pending")
    paid_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointment = db.relationship("Appointment", backref="payment")

    def __repr__(self):
        return f"<Payment {self.status} - {self.amount}>"
