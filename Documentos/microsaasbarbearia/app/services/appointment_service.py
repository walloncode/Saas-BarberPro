from datetime import datetime, timedelta
from app.extensions import db
from app.models.appointment import Appointment
from app.models.service import Service


class AppointmentService:
    """Regras de negocio para agendamentos."""

    @staticmethod
    def check_availability(barber_id, date, start_time, appointment_id=None):
        """Verifica se o barbeiro esta disponivel no horario informado."""
        query = Appointment.query.filter_by(
            barber_id=barber_id,
            date=date,
            status="scheduled",
        )
        if appointment_id:
            query = query.filter(Appointment.id != appointment_id)

        conflicts = query.all()
        conflict_start = _time_to_minutes(start_time)

        for apt in conflicts:
            apt_start = _time_to_minutes(apt.start_time)
            apt_end = _time_to_minutes(apt.end_time)

            if apt_start < conflict_start < apt_end or \
               apt_start <= conflict_start < apt_end or \
               conflict_start <= apt_start < apt_end:
                return False

        return True

    @staticmethod
    def calculate_end_time(start_time, duration_minutes):
        """Calcula horario final com base na duracao do servico."""
        dt_start = datetime.combine(datetime.today(), start_time)
        dt_end = dt_start + timedelta(minutes=duration_minutes)
        return dt_end.time()

    @staticmethod
    def create_appointment(appointment):
        """Cria agendamento com validacao de conflito."""
        if not AppointmentService.check_availability(
            appointment.barber_id, appointment.date, appointment.start_time
        ):
            return None, "Horario indisponivel. O barbeiro ja possui agendamento neste periodo."

        service = db.session.get(Service, appointment.service_id)
        if not service:
            return None, "Servico nao encontrado."

        appointment.end_time = AppointmentService.calculate_end_time(
            appointment.start_time, service.duration_minutes
        )
        db.session.add(appointment)
        db.session.flush()
        return appointment, None

    @staticmethod
    def cancel_appointment(appointment):
        """Cancela um agendamento existente."""
        if appointment.status == "cancelled":
            return False, "Agendamento ja esta cancelado."

        appointment.status = "cancelled"
        db.session.flush()
        return True, None

    @staticmethod
    def get_todays_appointments(shop_id):
        """Retorna agendamentos de hoje para uma barbearia."""
        return (
            Appointment.query.filter_by(
                barber_shop_id=shop_id,
                date=datetime.today().date(),
                status="scheduled",
            )
            .order_by(Appointment.start_time)
            .all()
        )


def _time_to_minutes(t):
    """Converte time para minutos desde 00:00."""
    return t.hour * 60 + t.minute
