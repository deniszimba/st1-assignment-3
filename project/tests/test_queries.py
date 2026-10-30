
"""Stage 9 tests for pure appointment queries."""

from datetime import datetime

import pytest

import smartcare.queries as queries
from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.queries import appointment_sort_key, select_appointments


@pytest.fixture
def sample_appointments():
    patient = Patient("P1", "Alex Example")
    d1 = Practitioner("D1", "Taylor Example", "General")
    d2 = Practitioner("D2", "Morgan Example", "General")

    morning = datetime(2026, 10, 1, 9, 0)
    later = datetime(2026, 10, 1, 10, 0)

    a1 = Appointment("A1", patient, d1, morning, AppointmentStatus.COMPLETED)
    a2 = Appointment("A2", patient, d1, morning, AppointmentStatus.CANCELLED)
    a3 = Appointment("A3", patient, d1, later, AppointmentStatus.SCHEDULED)
    a4 = Appointment("A4", patient, d2, morning, AppointmentStatus.SCHEDULED)

    return [a3, a4, a2, a1], (a1, a2, a3, a4)


def test_sort_key_uses_datetime_then_id(sample_appointments):
    _, (a1, _, _, _) = sample_appointments

    assert appointment_sort_key(a1) == (
        datetime(2026, 10, 1, 9, 0),
        "A1",
    )


def test_only_requested_practitioner_and_order(sample_appointments):
    source, (a1, a2, a3, _) = sample_appointments

    result = select_appointments(source, "D1")

    assert result == [a1, a2, a3]
    assert all(a.practitioner.practitioner_id == "D1" for a in result)


@pytest.mark.parametrize(
    "status,expected_id",
    [
        (AppointmentStatus.SCHEDULED, "A3"),
        (AppointmentStatus.CANCELLED, "A2"),
        (AppointmentStatus.COMPLETED, "A1"),
    ],
)
def test_each_explicit_status(sample_appointments, status, expected_id):
    source, _ = sample_appointments

    result = select_appointments(source, "D1", status)

    assert [a.appointment_id for a in result] == [expected_id]


def test_no_matching_status_returns_empty(sample_appointments):
    source, _ = sample_appointments

    result = select_appointments(source, "D2", AppointmentStatus.CANCELLED)

    assert result == []
    assert result is not source


def test_source_and_objects_unchanged(sample_appointments):
    source, (a1, a2, a3, _) = sample_appointments
    original_order = list(source)
    original_fields = [
        (a.appointment_id, a.date_time, a.status, a.practitioner)
        for a in source
    ]

    result = select_appointments(source, "D1")

    assert source == original_order
    assert [
        (a.appointment_id, a.date_time, a.status, a.practitioner)
        for a in source
    ] == original_fields
    assert result[0] is a1
    assert result[1] is a2
    assert result[2] is a3


def test_fresh_list_and_repeatability(sample_appointments):
    source, _ = sample_appointments

    first = select_appointments(source, "D1")
    second = select_appointments(source, "D1")

    assert first == second
    assert first is not second
    assert first is not source

    already_sorted = list(first)
    sorted_again = select_appointments(already_sorted, "D1")
    assert sorted_again == already_sorted
    assert sorted_again is not already_sorted

    empty_source = []
    empty_result = select_appointments(empty_source, "D1")
    assert empty_result == []
    assert empty_result is not empty_source


def test_query_uses_named_sort_key(sample_appointments, monkeypatch):
    source, _ = sample_appointments
    calls = []
    original_key = queries.appointment_sort_key

    def tracking_key(appointment):
        calls.append(appointment.appointment_id)
        return original_key(appointment)

    monkeypatch.setattr(queries, "appointment_sort_key", tracking_key)

    result = queries.select_appointments(source, "D1")

    assert [a.appointment_id for a in result] == ["A1", "A2", "A3"]
    assert sorted(calls) == ["A1", "A2", "A3"]
