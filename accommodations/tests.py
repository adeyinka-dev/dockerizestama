from django.test import TestCase
from accounts.models import Tenant
from .models import Hostel, Room


class HostelModelTest(TestCase):
    def setUp(self):
        self.manager = Tenant.objects.create(
            username="testuser",
            email="testuser@example.com",
            password="testpass1234",
            dob="2007-07-07",
            matric_num="12345678",
            faculty="CAD",
            department="Medicine",
            phone_number="12345678910",
        )
        self.hostel = Hostel.objects.create(
            name="Hostel A",
            address="123 Street",
            phone=1234567890,
            amenities="Wifi, Gym",
            manager=self.manager,
            room_count=10,
        )

    def test_hostel_creation(self):
        self.assertEqual(Hostel.objects.count(), 1)
        self.assertEqual(self.hostel.name, "Hostel A")
        self.assertEqual(self.hostel.address, "123 Street")
        self.assertEqual(self.hostel.phone, 1234567890)
        self.assertEqual(self.hostel.amenities, "Wifi, Gym")
        self.assertEqual(self.hostel.manager, self.manager)
        self.assertEqual(self.hostel.room_count, 10)

    def test_hostel_id_creation(self):
        self.assertIsNotNone(self.hostel.stama_id)
        self.assertTrue(self.hostel.stama_id.startswith("STM/HSE/"))


class RoomModelTest(TestCase):
    def setUp(self):
        self.manager = Tenant.objects.create(
            username="testuser",
            email="testuser@example.com",
            password="testpass1234",
            dob="2007-07-07",
            matric_num="12345678",
            faculty="CAD",
            department="Medicine",
            phone_number="12345678910",
        )
        self.hostel = Hostel.objects.create(
            name="Hostel A",
            address="123 Street",
            phone=1234567890,
            amenities="Wifi, Gym",
            manager=self.manager,
            room_count=10,
        )
        self.room = Room.objects.create(hostel=self.hostel, room_number="101")

    def test_room_creation(self):
        self.assertEqual(Room.objects.count(), 11)
        self.assertEqual(self.room.hostel, self.hostel)
        self.assertEqual(self.room.room_number, "101")

    def test_room_id_creation(self):
        self.assertIsNotNone(self.room.room_id)
        self.assertTrue(self.room.room_id.startswith(self.hostel.stama_id + "/RM/"))
