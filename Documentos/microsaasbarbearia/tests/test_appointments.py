import unittest
from datetime import date, time, timedelta
from app import create_app
from app.extensions import db
from app.models.barber_shop import BarberShop
from app.models.user import User
from app.models.barber import Barber
from app.models.client import Client
from app.models.service import Service
from app.models.appointment import Appointment
from app.services.appointment_service import AppointmentService


class TestAppointmentService(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        shop = BarberShop(name="Test Shop")
        db.session.add(shop)
        db.session.flush()

        user = User(
            barber_shop_id=shop.id,
            name="Admin",
            email="admin@test.com",
            role="admin",
        )
        user.set_password("test123")
        db.session.add(user)

        barber = Barber(barber_shop_id=shop.id, name="Joao")
        client = Client(barber_shop_id=shop.id, name="Maria", phone="11999999999")
        service = Service(barber_shop_id=shop.id, name="Corte", price=35.00, duration_minutes=30)
        db.session.add_all([barber, client, service])
        db.session.flush()

        self.shop_id = shop.id
        self.barber_id = barber.id
        self.client_id = client.id
        self.service_id = service.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_appointment_success(self):
        apt = Appointment(
            barber_shop_id=self.shop_id,
            barber_id=self.barber_id,
            client_id=self.client_id,
            service_id=self.service_id,
            date=date.today(),
            start_time=time(10, 0),
        )
        result, error = AppointmentService.create_appointment(apt)
        self.assertIsNotNone(result)
        self.assertIsNone(error)
        self.assertEqual(apt.end_time, time(10, 30))

    def test_create_appointment_conflict(self):
        apt1 = Appointment(
            barber_shop_id=self.shop_id,
            barber_id=self.barber_id,
            client_id=self.client_id,
            service_id=self.service_id,
            date=date.today(),
            start_time=time(10, 0),
        )
        AppointmentService.create_appointment(apt1)
        db.session.flush()

        apt2 = Appointment(
            barber_shop_id=self.shop_id,
            barber_id=self.barber_id,
            client_id=self.client_id,
            service_id=self.service_id,
            date=date.today(),
            start_time=time(10, 15),
        )
        result, error = AppointmentService.create_appointment(apt2)
        self.assertIsNotNone(error)

    def test_cancel_appointment(self):
        apt = Appointment(
            barber_shop_id=self.shop_id,
            barber_id=self.barber_id,
            client_id=self.client_id,
            service_id=self.service_id,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(10, 30),
        )
        db.session.add(apt)
        db.session.flush()

        success, error = AppointmentService.cancel_appointment(apt)
        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertEqual(apt.status, "cancelled")

    def test_cancel_already_cancelled(self):
        apt = Appointment(
            barber_shop_id=self.shop_id,
            barber_id=self.barber_id,
            client_id=self.client_id,
            service_id=self.service_id,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(10, 30),
            status="cancelled",
        )
        db.session.add(apt)
        db.session.flush()

        success, error = AppointmentService.cancel_appointment(apt)
        self.assertFalse(success)
        self.assertIsNotNone(error)

    def test_different_barbers_same_time(self):
        barber2 = Barber(barber_shop_id=self.shop_id, name="Carlos")
        db.session.add(barber2)
        db.session.flush()

        apt1 = Appointment(
            barber_shop_id=self.shop_id,
            barber_id=self.barber_id,
            client_id=self.client_id,
            service_id=self.service_id,
            date=date.today(),
            start_time=time(10, 0),
        )
        apt2 = Appointment(
            barber_shop_id=self.shop_id,
            barber_id=barber2.id,
            client_id=self.client_id,
            service_id=self.service_id,
            date=date.today(),
            start_time=time(10, 0),
        )
        r1, _ = AppointmentService.create_appointment(apt1)
        r2, _ = AppointmentService.create_appointment(apt2)
        self.assertIsNotNone(r1)
        self.assertIsNotNone(r2)


if __name__ == "__main__":
    unittest.main()
