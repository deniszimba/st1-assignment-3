
"""Stage 9 tests for SmartCare services and interactive workflows."""

from datetime import datetime

import pytest

from smartcare.console import parse_date_time, run_menu
from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


@pytest.fixture
def system():
    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)
    appointments = AppointmentService(store)

    patient = patients.register_patient("P1", "Alex Example")
    d1 = practitioners.register_practitioner(
        "D1", "Taylor Example", "General"
    )
    d2 = practitioners.register_practitioner(
        "D2", "Morgan Example", "General"
    )
    return store, patients, practitioners, appointments, patient, d1, d2


def test_complete_service_workflow(system):
    store, patients, practitioners, service, patient, d1, d2 = system
    when = datetime(2026, 10, 1, 9, 0)

    assert patients.find_patient("P1") is patient
    assert practitioners.find_practitioner("D1") is d1

    a1 = service.book_appointment("A1", "P1", "D1", when)
    assert a1.patient is patient
    assert a1.practitioner is d1

    with pytest.raises(ValueError):
        service.book_appointment("A2", "P1", "D1", when)

    assert store.list_appointments() == [a1]
    assert store.find_appointment("A2") is None

    a2 = service.book_appointment("A2", "P1", "D2", when)
    assert a2.practitioner is d2

    assert service.cancel_appointment("A1") is a1
    assert a1.status is AppointmentStatus.CANCELLED
    assert service.find_appointment("A1") is a1

    assert service.list_practitioner_appointments("D1") == [a1]
    assert service.list_practitioner_appointments(
        "D1", AppointmentStatus.SCHEDULED
    ) == []
    assert service.list_practitioner_appointments(
        "D1", AppointmentStatus.CANCELLED
    ) == [a1]

    a3 = service.book_appointment("A3", "P1", "D1", when)

    assert service.list_practitioner_appointments("D1") == [a1, a3]
    assert service.list_practitioner_appointments(
        "D1", AppointmentStatus.SCHEDULED
    ) == [a3]
    assert service.list_practitioner_appointments("D2") == [a2]
    assert store.list_appointments() == [a1, a2, a3]


def test_listing_validation_and_empty_results(system):
    store, _, _, service, _, _, _ = system

    first = service.list_practitioner_appointments("D1")
    second = service.list_practitioner_appointments(" D1 ")

    assert first == []
    assert second == []
    assert first is not second

    with pytest.raises(LookupError):
        service.list_practitioner_appointments("UNKNOWN")

    for invalid_id in ("", "   ", None, 123):
        with pytest.raises(ValueError):
            service.list_practitioner_appointments(invalid_id)

    for invalid_status in ("scheduled", 42):
        with pytest.raises(ValueError):
            service.list_practitioner_appointments("D1", invalid_status)

    assert store.list_appointments() == []


def test_invalid_booking_preserves_state(system):
    store, _, _, service, _, _, _ = system
    when = datetime(2026, 10, 1, 9, 0)
    original = service.book_appointment("A1", "P1", "D1", when)

    with pytest.raises(LookupError):
        service.book_appointment("A2", "UNKNOWN", "D1", when)

    with pytest.raises(ValueError):
        service.book_appointment("A2", "P1", "D1", when)

    assert store.list_appointments() == [original]
    assert store.find_appointment("A2") is None
    assert original.status is AppointmentStatus.SCHEDULED

    later = datetime(2026, 10, 1, 10, 0)
    created = service.book_appointment("A2", "P1", "D1", later)

    assert store.list_appointments() == [original, created]


def run_scripted_menu(monkeypatch, capsys, entries):
    """Exercise the real console with reproducible user inputs."""
    responses = iter(entries)
    monkeypatch.setattr("builtins.input", lambda prompt: next(responses))
    run_menu()
    return capsys.readouterr().out


def test_console_complete_workflow(monkeypatch, capsys):
    output = run_scripted_menu(
        monkeypatch,
        capsys,
        [
            "1", "P1", "Alex Example",
            "2", "P1",
            "3", "D1", "Taylor Example", "General",
            "4", "D1",
            "3", "D2", "Morgan Example", "General",
            "5", "A1", "P1", "D1", "2026-10-01 09:00",
            "5", "A2", "P1", "D1", "2026-10-01 09:00",
            "7", "A2",
            "5", "A2", "P1", "D2", "2026-10-01 09:00",
            "6", "A1",
            "7", "A1",
            "8", "D1", "",
            "8", "D1", "scheduled",
            "5", "A3", "P1", "D1", "2026-10-01 09:00",
            "8", "D1", "",
            "0",
        ],
    )

    assert "Patient registered: P1" in output
    assert "Patient found: P1" in output
    assert "Practitioner registered: D1" in output
    assert "Practitioner found: D1" in output
    assert "Practitioner registered: D2" in output
    assert "Practitioner already has a SCHEDULED appointment" in output
    assert "Error: Appointment not found" in output
    assert "A2: P1 with D2" in output
    assert "A1: P1 with D1, 2026-10-01 09:00, cancelled" in output
    assert "No matching appointments found." in output
    assert "A3: P1 with D1" in output
    assert "Goodbye!" in output


def test_console_error_recovery(monkeypatch, capsys):
    output = run_scripted_menu(
        monkeypatch,
        capsys,
        [
            "99",
            "1", " ", "Missing ID",
            "1", "P1", "Alex Example",
            "1", "P1", "Duplicate",
            "3", "D1", "Taylor Example", "General",
            "5", "A5", "P1", "UNKNOWN", "2026-10-01 09:00",
            "7", "A5",
            "5", "A5", "P1", "D1", "not-a-date",
            "5", "A5", "P1", "D1", "2026-13-01 09:00",
            "5", "A5", "P1", "D1", "2026-10-01 09:00",
            "6", "A5",
            "6", "A5",
            "8", "D1", "invalid-status",
            "8", "D1", "",
            "0",
        ],
    )

    assert "Invalid menu choice" in output
    assert "Error: Patient ID cannot be blank" in output
    assert "Error: Patient ID already exists" in output
    assert "Error: Practitioner not found" in output
    assert "Error: Appointment not found" in output
    assert "Use date/time format YYYY-MM-DD HH:MM" in output
    assert "Invalid calendar date/time" in output
    assert "A5: P1 with D1" in output
    assert "Only SCHEDULED appointments may be cancelled" in output
    assert "Status must be scheduled, cancelled" in output
    assert "A5: P1 with D1, 2026-10-01 09:00, cancelled" in output
    assert "Goodbye!" in output


def test_strict_date_time_parser():
    assert parse_date_time("2026-10-01 09:00") == datetime(
        2026, 10, 1, 9, 0
    )

    for invalid in (
        "2026-10-01",
        "2026-10-01 9:00",
        "2026-13-01 09:00",
        "2026-02-30 09:00",
    ):
        with pytest.raises(ValueError):
            parse_date_time(invalid)
