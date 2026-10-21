"""Stage 6 checks for the service lookup and cancellation operations."""

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.services import PatientService


def patient_setup() -> tuple[SmartCareDataStore, PatientService]:
    """create a store with regi patient"""
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    patients.register_patient('P1', 'Alex Example')
    return data_store, patients


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
