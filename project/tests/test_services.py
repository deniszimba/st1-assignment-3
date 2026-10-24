"""Stage 6 checks for the service lookup and cancellation operations."""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def patient_setup() -> tuple[SmartCareDataStore, PatientService]:
    """create a store with regi patient"""
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    patients.register_patient('P1', 'Alex Example')
    return data_store, patients


def practitioner_setup() -> tuple[SmartCareDataStore, PractitionerService]:
    """Create a fresh store with one synthetic registered practitioner."""
    data_store = SmartCareDataStore()
    practitioners = PractitionerService(data_store)
    practitioners.register_practitioner('D1', 'Taylor Example', 'General')
    return data_store, practitioners


def appointment_setup() -> tuple[
    SmartCareDataStore,
    AppointmentService,
    Appointment,
]:
    """Create a fresh store with one SCHEDULED synthetic appointment A1."""
    data_store = SmartCareDataStore()
    PatientService(data_store).register_patient('P1', 'Alex Example')
    PractitionerService(data_store).register_practitioner(
        'D1',
        'Taylor Example',
        'General',
    )
    appointments = AppointmentService(data_store)
    appointment = appointments.book_appointment(
        'A1',
        'P1',
        'D1',
        datetime(2026, 10, 1, 9, 0),
    )
    return data_store, appointments, appointment


# FR-02 Patient search 


def test_find_patient_returns_registered_object() -> None:
    """known ID returns the same stored Patient object."""
    data_store, patients = patient_setup()
    registered = data_store.find_patient('P1')
    found = patients.find_patient('P1')
    assert found is registered
    assert found.patient_id == 'P1'
    assert found.name == 'Alex Example'
    assert data_store.list_patients() == [registered]


def test_find_patient_trims_surrounding_spaces() -> None:
    """IDs are trimmed, so ' P1 ' finds the patient registered as P1."""
    data_store, patients = patient_setup()
    assert patients.find_patient('  P1  ') is data_store.find_patient('P1')


def test_find_patient_unknown_id_raises_lookup_error() -> None:
    """valid but unregistered ID reports absence."""
    data_store, patients = patient_setup()
    with pytest.raises(LookupError):
        patients.find_patient('P2')
    assert len(data_store.list_patients()) == 1


def test_find_patient_is_case_sensitive() -> None:
    """IDs are case-sensitive, unknown ID."""
    _, patients = patient_setup()
    with pytest.raises(LookupError):
        patients.find_patient('p1')


@pytest.mark.parametrize('bad_id', ['', '   ', None])
def test_find_patient_invalid_id_raises_value_error(bad_id) -> None:
    """blank or non-text IDs are invalid input, not missing records."""
    data_store, patients = patient_setup()
    with pytest.raises(ValueError):
        patients.find_patient(bad_id)
    assert len(data_store.list_patients()) == 1


# FR-03 supporting operation: practitioner lookup


def test_find_practitioner_returns_registered_object() -> None:
    """A known ID returns the same stored Practitioner object."""
    data_store, practitioners = practitioner_setup()
    registered = data_store.find_practitioner('D1')
    found = practitioners.find_practitioner('D1')
    assert found is registered
    assert found.practitioner_id == 'D1'
    assert found.name == 'Taylor Example'
    assert found.specialty == 'General'
    assert data_store.list_practitioners() == [registered]


def test_find_practitioner_trims_surrounding_spaces() -> None:
    """IDs are trimmed, so ' D1 ' finds the practitioner registered as D1."""
    data_store, practitioners = practitioner_setup()
    found = practitioners.find_practitioner('  D1  ')
    assert found is data_store.find_practitioner('D1')


def test_find_practitioner_unknown_id_raises_lookup_error() -> None:
    """A valid but unregistered ID reports absence."""
    data_store, practitioners = practitioner_setup()
    with pytest.raises(LookupError):
        practitioners.find_practitioner('D2')
    assert len(data_store.list_practitioners()) == 1


def test_find_practitioner_is_case_sensitive() -> None:
    """IDs are case-sensitive, so 'd1' is a different, unknown ID."""
    _, practitioners = practitioner_setup()
    with pytest.raises(LookupError):
        practitioners.find_practitioner('d1')


@pytest.mark.parametrize('bad_id', ['', '   ', None])
def test_find_practitioner_invalid_id_raises_value_error(bad_id) -> None:
    """Blank or non-text IDs are invalid input, not missing records."""
    data_store, practitioners = practitioner_setup()
    with pytest.raises(ValueError):
        practitioners.find_practitioner(bad_id)
    assert len(data_store.list_practitioners()) == 1


# FR-06 cancellation with FR-07 retained history 


def test_cancel_returns_same_object_with_cancelled_status() -> None:
    """AC-05.1: cancelling a SCHEDULED appointment changes its status."""
    _, appointments, appointment = appointment_setup()
    result = appointments.cancel_appointment('A1')
    assert result is appointment
    assert appointment.status is AppointmentStatus.CANCELLED


def test_cancelled_appointment_is_kept_in_history() -> None:
    """AC-05.2: the cancelled appointment is still stored, not deleted."""
    data_store, appointments, appointment = appointment_setup()
    appointments.cancel_appointment('A1')
    assert appointments.find_appointment('A1') is appointment
    assert data_store.list_appointments() == [appointment]
    assert appointment.patient is data_store.find_patient('P1')
    assert appointment.practitioner is data_store.find_practitioner('D1')
    assert appointment.date_time == datetime(2026, 10, 1, 9, 0)


def test_cancel_trims_surrounding_spaces() -> None:
    """IDs are trimmed, so ' A1 ' cancels the appointment stored as A1."""
    _, appointments, appointment = appointment_setup()
    assert appointments.cancel_appointment('  A1  ') is appointment
    assert appointment.status is AppointmentStatus.CANCELLED


def test_repeated_cancellation_rejected_without_change() -> None:
    """AC-05.3: a second cancellation is rejected and nothing changes."""
    data_store, appointments, appointment = appointment_setup()
    appointments.cancel_appointment('A1')
    with pytest.raises(ValueError):
        appointments.cancel_appointment('A1')
    assert appointment.status is AppointmentStatus.CANCELLED
    assert data_store.list_appointments() == [appointment]


def test_cancel_completed_appointment_rejected_without_change() -> None:
    """FR-06: only SCHEDULED can be cancelled, so COMPLETED is rejected."""
    data_store, appointments, _ = appointment_setup()
    completed = Appointment(
        'A2',
        data_store.find_patient('P1'),
        data_store.find_practitioner('D1'),
        datetime(2026, 9, 1, 9, 0),
        AppointmentStatus.COMPLETED,
    )
    data_store.add_appointment(completed)
    with pytest.raises(ValueError):
        appointments.cancel_appointment('A2')
    assert completed.status is AppointmentStatus.COMPLETED
    assert appointments.find_appointment('A2') is completed


@pytest.mark.parametrize('unknown_id', ['A9', 'a1'])
def test_cancel_unknown_id_raises_lookup_error(unknown_id) -> None:
    """Unknown IDs (including wrong case) raise LookupError, no change."""
    data_store, appointments, appointment = appointment_setup()
    with pytest.raises(LookupError):
        appointments.cancel_appointment(unknown_id)
    assert appointment.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [appointment]


@pytest.mark.parametrize('bad_id', ['', '   ', None])
def test_cancel_invalid_id_raises_value_error(bad_id) -> None:
    """Blank or non-text IDs raise ValueError and change nothing."""
    data_store, appointments, appointment = appointment_setup()
    with pytest.raises(ValueError):
        appointments.cancel_appointment(bad_id)
    assert appointment.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [appointment]


def test_cancel_changes_only_the_target_appointment() -> None:
    """Cancelling A1 leaves another SCHEDULED appointment untouched."""
    _, appointments, first = appointment_setup()
    second = appointments.book_appointment(
        'A2',
        'P1',
        'D1',
        datetime(2026, 10, 1, 10, 0),
    )
    appointments.cancel_appointment('A1')
    assert first.status is AppointmentStatus.CANCELLED
    assert second.status is AppointmentStatus.SCHEDULED

def test_register_patient_stores_valid_patient() -> None:
    # Create a new store and service.
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)

    # Register a patient.
    patient = patients.register_patient("P7", "Sam Example")

    # Check that the patient was stored.
    assert data_store.find_patient("P7") is patient
    assert data_store.list_patients() == [patient]

def test_duplicate_patient_id_is_rejected_without_change() -> None:
    # Register the original patient.
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    original = patients.register_patient("P1", "Alex Example")

    # Try to register the same ID again.
    with pytest.raises(ValueError):
        patients.register_patient(" P1 ", "Replacement Name")

    # Check that the original patient stayed unchanged.
    assert data_store.find_patient("P1") is original
    assert original.name == "Alex Example"
    assert data_store.list_patients() == [original]

def test_same_practitioner_exact_time_is_rejected() -> None:
    # Create the first appointment.
    data_store, appointments, original = appointment_setup()

    # Try the same practitioner at the same time.
    with pytest.raises(ValueError):
        appointments.book_appointment(
            "A2",
            "P1",
            "D1",
            datetime(2026, 10, 1, 9, 0),
        )

    # Check that only the original is stored.
    assert data_store.list_appointments() == [original]
    assert original.status is AppointmentStatus.SCHEDULED

def test_different_practitioner_same_time_is_allowed() -> None:
    # Create the first appointment.
    data_store, appointments, first = appointment_setup()

    # Register another practitioner.
    PractitionerService(data_store).register_practitioner(
        "D2",
        "Morgan Example",
        "General",
    )

    # Book the second practitioner at the same time.
    second = appointments.book_appointment(
        "A2",
        "P1",
        "D2",
        datetime(2026, 10, 1, 9, 0),
    )

    # Check that both appointments are stored.
    assert data_store.list_appointments() == [first, second]
    assert second.practitioner is data_store.find_practitioner("D2")

def test_cancelled_appointment_releases_practitioner_slot() -> None:
    # Create and cancel the first appointment.
    data_store, appointments, first = appointment_setup()
    appointments.cancel_appointment("A1")

    # Book the same practitioner at the same time.
    second = appointments.book_appointment(
        "A2",
        "P1",
        "D1",
        datetime(2026, 10, 1, 9, 0),
    )

    # Check both appointments.
    assert first.status is AppointmentStatus.CANCELLED
    assert second.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [first, second]
