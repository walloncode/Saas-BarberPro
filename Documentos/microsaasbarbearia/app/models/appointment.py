from app.extensions import db
from datetime import datetime, time, timedelta


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    barber_shop_id = db.Column(db.Integer, db.ForeignKey("barber_shops.id"), nullable=False)
    barber_id = db.Column(db.Integer, db.ForeignKey("barbers.id"), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default="scheduled")
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def calculate_end_time(self):
        """Calcula o end_time com base no start_time e duracao do servico."""
        dt_start = datetime.combine(self.date, self.start_time)
        dt_end = dt_start + timedelta(minutes=self.service.duration_minutes)
        self.end_time = dt_end.time()

    def __repr__(self):
        return f"<Appointment {self.client_id} on {self.date} {self.start_time}>"
