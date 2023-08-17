from django.test import TestCase
from .models import Maintenance, MaintenanceType, MaintenanceSubType, Note
from accommodations.models import Room, Hostel
from accounts.models import Tenant


class MaintenanceTypeModelTest(TestCase):
    def setUp(self):
        self.maint_type = MaintenanceType.objects.create(name="Electrical")

    def test_maintenance_type_creation(self):
        self.assertEqual(MaintenanceType.objects.count(), 1)
        self.assertEqual(self.maint_type.name, "Electrical")


class MaintenanceSubTypeModelTest(TestCase):
    def setUp(self):
        self.maint_type = MaintenanceType.objects.create(name="Electrical")
        self.maint_subtype = MaintenanceSubType.objects.create(name="Socket")

    def test_maintenance_subtype_creation(self):
        self.assertEqual(MaintenanceSubType.objects.count(), 1)
        self.assertEqual(self.maint_subtype.name, "Socket")


class MaintenanceModelTest(TestCase):
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
            is_staff=True,
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
        self.maint_type = MaintenanceType.objects.create(name="Electrical")
        self.maint_subtype = MaintenanceSubType.objects.create(name="Socket")
        self.maintenance = Maintenance.objects.create(
            room=self.room,
            location="Location",
            type=self.maint_type,
            subtype=self.maint_subtype,
        )
        self.note = Note.objects.create(
            note="This is a note, I'm obviously testing the note creation",
            maintenance=self.maintenance,
            author=self.manager,
        )

    def test_maintenance_creation(self):
        self.assertEqual(Maintenance.objects.count(), 1)
        self.assertEqual(self.maintenance.location, "Location")
        self.assertEqual(self.maintenance.type, self.maint_type)
        self.assertEqual(self.maintenance.subtype, self.maint_subtype)

    def test_repair_id_creation(self):
        self.assertIsNotNone(self.maintenance.repair_id)
        self.assertTrue(self.maintenance.repair_id.startswith("REP"))

    def test_note_creation(self):
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(
            self.note.note, "This is a note, I'm obviously testing the note creation"
        )
        self.assertEqual(self.note.maintenance, self.maintenance)
        self.assertEqual(self.note.author, self.manager)
