
"""Additional Stage 9 tests following the GitHub Copilot review."""

import sys
from datetime import datetime

import main as app_entry

from smartcare.console import run_menu
from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def test_service_filters_completed_appointments():
    store = SmartCareDataStore()
    patient = PatientService(store).register_patient(
        "P1", "Alex Example"
    )
    practitioner = PractitionerService(store).register_practitioner(
        "D1", "Taylor Example", "General"
    )

    completed = Appointment(
        "A1",
        patient,
        practitioner,
        datetime(2026, 10, 1, 9, 0),
        AppointmentStatus.COMPLETED,
    )
    store.add_appointment(completed)

    service = AppointmentService(store)

    result = service.list_practitioner_appointments(
        " D1 ", AppointmentStatus.COMPLETED
    )

    assert len(result) == 1
    assert result[0] is completed
    assert service.list_practitioner_appointments(
        "D1", AppointmentStatus.SCHEDULED
    ) == []
    assert service.list_practitioner_appointments("D1") == [completed]


def test_console_displays_appointments_in_sorted_order(
    monkeypatch, capsys
):
    inputs = iter([
        "1", "P1", "Alex Example",
        "3", "D1", "Taylor Example", "General",
        "5", "A2", "P1", "D1", "2026-10-01 10:00",
        "5", "A1", "P1", "D1", "2026-10-01 09:00",
        "8", "D1", "",
        "0",
    ])

    monkeypatch.setattr(
        "builtins.input", lambda prompt: next(inputs)
    )

    run_menu()
    output = capsys.readouterr().out

    listing = output.split("Practitioner appointments:", 1)[1]

    assert "A1: P1 with D1" in listing
    assert "A2: P1 with D1" in listing
    assert listing.index("A1:") < listing.index("A2:")


def test_interactive_entry_point(monkeypatch):
    calls = []

    monkeypatch.setattr(
        app_entry, "run_menu", lambda: calls.append("menu")
    )
    monkeypatch.setattr(
        app_entry, "run_demo", lambda: calls.append("demo")
    )
    monkeypatch.setattr(
        sys, "argv", ["main.py", "--interactive"]
    )

    app_entry.main()

    assert calls == ["menu"]


def test_default_demo_entry_point(monkeypatch):
    calls = []

    monkeypatch.setattr(
        app_entry, "run_menu", lambda: calls.append("menu")
    )
    monkeypatch.setattr(
        app_entry, "run_demo", lambda: calls.append("demo")
    )
    monkeypatch.setattr(sys, "argv", ["main.py"])

    app_entry.main()

    assert calls == ["demo"]
