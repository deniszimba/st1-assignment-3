"""Stage 7 domain tests."""

from datetime import datetime, timezone

import pytest

# Import the SmartCare domain classes
from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)


def make_appointment(
    status: AppointmentStatus = AppointmentStatus.SCHEDULED,
) -> Appointment:
    # Create a patient
    patient = Patient("P1", "Alex Example")

    # Create a practitioner
    practitioner = Practitioner("D1", "Taylor Example", "General")

    # Create an appointment
    return Appointment(
        "A1",
        patient,
        practitioner,
        datetime(2026, 10, 1, 9, 0),
        status,
    )

def test_blank_patient_id_is_rejected() -> None:
    # Check that a blank patient ID is rejected.
    with pytest.raises(ValueError):
        Patient("   ", "Alex Example")

def test_practitioner_rejects_blank_required_fields() -> None:
    # Check a blank ID.
    with pytest.raises(ValueError):
        Practitioner("   ", "Taylor Example", "General")

    # Check a blank name.
    with pytest.raises(ValueError):
        Practitioner("D1", "   ", "General")

    # Check a blank specialty.
    with pytest.raises(ValueError):
        Practitioner("D1", "Taylor Example", "   ")

def test_new_appointment_starts_scheduled() -> None:
    # Create a valid appointment.
    appointment = make_appointment()

    # Check its starting values.
    assert appointment.appointment_id == "A1"
    assert appointment.patient.patient_id == "P1"
    assert appointment.practitioner.practitioner_id == "D1"
    assert appointment.date_time == datetime(2026, 10, 1, 9, 0)
    assert appointment.status is AppointmentStatus.SCHEDULED

def test_cancel_changes_status() -> None:
    # Create and cancel an appointment.
    appointment = make_appointment()
    appointment.cancel()

    # Check the new status.
    assert appointment.status is AppointmentStatus.CANCELLED

def test_repeated_cancel_is_rejected_without_change() -> None:
    # Cancel the appointment once.
    appointment = make_appointment()
    appointment.cancel()

    # Try to cancel it again.
    with pytest.raises(ValueError):
        appointment.cancel()

    # Check that it stays cancelled.
    assert appointment.status is AppointmentStatus.CANCELLED

def test_completed_appointment_cannot_be_cancelled() -> None:
    # Create a completed appointment.
    appointment = make_appointment(AppointmentStatus.COMPLETED)

    # Try to cancel it.
    with pytest.raises(ValueError):
        appointment.cancel()

    # Check that it stays completed.
    assert appointment.status is AppointmentStatus.COMPLETED

def test_appointment_rejects_invalid_values() -> None:
    patient = Patient("P1", "Alex Example")
    practitioner = Practitioner("D1", "Taylor Example", "General")
    when = datetime(2026, 10, 1, 9, 0)

    # Check an invalid patient.
    with pytest.raises(ValueError):
        Appointment("A1", "not a patient", practitioner, when)

    # Check an invalid practitioner.
    with pytest.raises(ValueError):
        Appointment("A1", patient, "not a practitioner", when)

    # Check an invalid date.
    with pytest.raises(ValueError):
        Appointment("A1", patient, practitioner, "not a date")

    # Check an invalid status.
    with pytest.raises(ValueError):
        Appointment("A1", patient, practitioner, when, "scheduled")


def test_valid_patient_stores_trimmed_values() -> None:
    """T7-D08: a valid Patient keeps its trimmed ID and name."""
    patient = Patient("  P1  ", "  Alex Example  ")
    assert patient.patient_id == "P1"
    assert patient.name == "Alex Example"


def test_valid_practitioner_stores_trimmed_values() -> None:
    """T7-D09: a valid Practitioner keeps its trimmed ID, name and specialty."""
    practitioner = Practitioner("  D1  ", "  Taylor Example  ", "  General  ")
    assert practitioner.practitioner_id == "D1"
    assert practitioner.name == "Taylor Example"
    assert practitioner.specialty == "General"


@pytest.mark.parametrize("bad_name", ["", "   "])
def test_blank_patient_name_is_rejected(bad_name) -> None:
    """T7-D10: a blank or spaces-only patient name raises ValueError."""
    with pytest.raises(ValueError):
        Patient("P1", bad_name)


@pytest.mark.parametrize(
    "bad_time",
    [
        datetime(2026, 10, 1, 9, 0, 30),
        datetime(2026, 10, 1, 9, 0, 0, 500),
        datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc),
    ],
)
def test_appointment_rejects_seconds_or_timezone(bad_time) -> None:
    """T7-D11: only a local naive datetime at minute precision is valid."""
    patient = Patient("P1", "Alex Example")
    practitioner = Practitioner("D1", "Taylor Example", "General")
    with pytest.raises(ValueError):
        Appointment("A1", patient, practitioner, bad_time)
