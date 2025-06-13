from enum import Enum
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


# Admin Model
class Admin(models.Model):
    """
    The Admin model
    """

    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=20, unique=True)
    name = fields.CharField(max_length=50)
    password_hash = fields.CharField(max_length=128)
    email = fields.CharField(max_length=50, unique=True)

    class Meta:
        # table = "admin"
        exclude = ["password_hash"]


# ENUM for patient gender
class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


# Patiend Model
class Patient(models.Model):
    """
    The Patient model
    """

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    phone = fields.CharField(max_length=50, unique=True)
    dob = fields.DateField()
    gender = fields.CharEnumField(GenderEnum)
    address = fields.CharField(max_length=255)
    emergency_person = fields.CharField(max_length=255)
    emergency_relation = fields.CharField(max_length=255)
    emergency_number = fields.CharField(max_length=255)

    class Meta:
        exclude = []


# Digital health record Model
class Records(models.Model):
    id = fields.IntField(primary_key=True)
    patient_id = fields.ForeignKeyField(
        "models.Patient",
        related_name="records",
        on_delete=fields.CASCADE,
        on_update=fields.CASCADE,
    )
    doctor_id = fields.ForeignKeyField(
        "models.Doctor", related_name="records", null=True
    )
    reason = fields.TextField()
    record_data = fields.CharField(max_length=255)

    class Meta:
        exclude = []


# Doctor Model
class Doctor(models.Model):
    """
    The Doctor model
    """

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    phone = fields.CharField(max_length=50, unique=True)
    specialization = fields.CharField(max_length=255)

    class Meta:
        exclude = []


# Receptionist Model
class Receptionist(models.Model):
    """
    The Receptionist model
    """

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    phone = fields.CharField(max_length=50, unique=True)

    class Meta:
        exclude = []


# create enum for appointment status
class AppointmentStatusEnum(str, Enum):
    PENDING = "PENDING"
    BOOKED = "BOOKED"
    DONE = "DONE"
    REJECTED = "REJECTED"


# Appointment Model
class Appointment(models.Model):
    """
    The Appointment Model
    """

    id = fields.IntField(primary_key=True)
    patient_id = fields.ForeignKeyField(
        "models.Patient",
        related_name="appointments",
        on_delete=fields.CASCADE,
        on_update=fields.CASCADE,
    )
    doctor_id = fields.ForeignKeyField(
        "models.Doctor",
        related_name="appointments",
        on_delete=fields.CASCADE,
        on_update=fields.CASCADE,
    )
    receptionist_id = fields.ForeignKeyField(
        "models.Receptionist",
        related_name="appointments",
        on_delete=fields.CASCADE,
        on_update=fields.CASCADE,
        null=True,
    )
    slot_id = fields.ForeignKeyField(
        "models.Slot",
        related_name="appointments",
        on_delete=fields.CASCADE,
        on_update=fields.CASCADE,
    )
    appointment_date = fields.DateField()
    reschedule_date = fields.DateField(null=True)
    status = fields.CharEnumField(AppointmentStatusEnum, default=AppointmentStatusEnum.PENDING)
    record_ids = fields.JSONField(default=list)
    reason = fields.TextField()

    class Meta:
        exclude = []


# Slot Model
class Slot(models.Model):
    """
    The Slot Model
    """

    id = fields.IntField(primary_key=True)
    doctor_id = fields.ForeignKeyField("models.Doctor", related_name="slots")
    available = fields.BooleanField()
    slot_time = fields.CharField(max_length=255)
    day = fields.CharField(max_length=3)

    class Meta:
        exclude = []

# Prescription Model
class Prescription(models.Model):
    """
    The Prescription Model
    """
    id = fields.IntField(primary_key=True)
    appointment_id = fields.ForeignKeyField("models.Appointment", related_name="prescription")
    observation = fields.TextField()
    medication = fields.TextField()
    advise = fields.TextField()
    test = fields.TextField()

    class Meta:
        exclude = []


Admin_Pydantic = pydantic_model_creator(Admin)
Patient_Pydantic = pydantic_model_creator(Patient)
Records_Pydantic = pydantic_model_creator(Records)
Doctor_Pydantic = pydantic_model_creator(Doctor)
Receptionist_Pydantic = pydantic_model_creator(Receptionist)
Appointment_Pydantic = pydantic_model_creator(Appointment)
Slot_Pydantic = pydantic_model_creator(Slot)

AdminType = Admin_Pydantic
PatientType = Patient_Pydantic
RecordsType = Records_Pydantic
DoctorType = Doctor_Pydantic
ReceptionistType = Receptionist_Pydantic
AppointmentType = Appointment_Pydantic
SlotType = Slot_Pydantic
