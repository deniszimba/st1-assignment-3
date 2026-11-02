"Focused Stage 8 regression tests."

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def test_f8_01_practitioner_conflict_rule():
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)

    patients.register_patient("P1", "Alex Example")
    patients.register_patient("P2", "Sam Example")
    practitioners.register_practitioner("D1", "Taylor Example", "General")
    practitioners.register_practitioner("D2", "Morgan Example", "General")

    appointment_time = datetime(2026, 10, 1, 9, 0)

    first = appointments.book_appointment(
        "A1", "P1", "D1", appointment_time
    )

    with pytest.raises(ValueError):
        appointments.book_appointment(
            "A2", "P2", "D1", appointment_time
        )

    assert data_store.list_appointments() == [first]

    second = appointments.book_appointment(
        "A3", "P2", "D2", appointment_time
    )

    assert data_store.list_appointments() == [first, second]


def test_f8_02_cancelled_appointment_remains_retrievable():
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)

    patients.register_patient("P1", "Alex Example")
    practitioners.register_practitioner(
        "D1", "Taylor Example", "General"
    )

    appointment = appointments.book_appointment(
        "A1",
        "P1",
        "D1",
        datetime(2026, 10, 1, 9, 0),
    )

    cancelled = appointments.cancel_appointment("A1")

    assert cancelled is appointment
    assert appointment.status is AppointmentStatus.CANCELLED
    assert data_store.list_appointments() == [appointment]
    assert data_store.find_appointment("A1") is appointment
    assert appointments.find_appointment("A1") is appointment

    with pytest.raises(ValueError):
        appointments.cancel_appointment("A1")