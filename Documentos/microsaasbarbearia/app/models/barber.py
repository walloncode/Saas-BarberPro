from app.extensions import db


class Barber(db.Model):
    __tablename__ = "barbers"

    id = db.Column(db.Integer, primary_key=True)
    barber_shop_id = db.Column(db.Integer, db.ForeignKey("barber_shops.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)

    appointments = db.relationship("Appointment", backref="barber", lazy=True)

    def __repr__(self):
        return f"<Barber {self.name}>"
