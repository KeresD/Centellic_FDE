"""Tests for the ledger. LEARNER STARTER. Synthetic data only.

CA-3: three of these are written for you as a shape to copy. The rest raise
NotImplementedError. Replace each one with a real assertion.
"""

import pytest

from ledger import add_entry, find_reference, total


@pytest.fixture
def sample_ledger():
    """Three synthetic entries whose amounts are chosen to break float maths.

    A fixture exists so the same data is not copy-pasted into six tests. When
    the shape of an entry changes, it changes here once.
    """
    return [
        {"reference": "SYN-001", "amount": 10.10},
        {"reference": "SYN-002", "amount": 20.20},
        {"reference": "SYN-003", "amount": 5.05},
    ]


def test_total_is_exact(sample_ledger):
    """Written for you. Run it and read the number in the failure carefully."""
    assert total(sample_ledger) == 35.35

'''
def test_total_of_an_empty_ledger_is_zero():
    """TODO (CA-3): assert the total of an empty ledger."""
    raise NotImplementedError '''

def test_total_of_an_empty_ledger_is_zero():
    assert total([]) == 0

def test_add_entry_does_not_leak_between_calls():
    """TODO (CA-3): call add_entry twice with no ledger argument, and assert
    that each call returns a ledger of length 1."""
    first = add_entry("SYN-001", 10.10)
    second = add_entry("SYN-002", 20.20)
    assert len(first) == 1
    assert len(second) == 1

'''
def test_add_entry_returns_a_new_list(sample_ledger):
    """TODO (CA-3): add an entry to sample_ledger and assert the original is
    still length 3 while the returned ledger is length 4."""
    raise NotImplementedError '''

def test_add_entry_returns_a_new_list(sample_ledger):
    new_ledger = add_entry("SYN-004", 1.00, sample_ledger)
    assert len(sample_ledger) == 3
    assert len(new_ledger) == 4

'''
def test_find_reference_hit(sample_ledger):
    """TODO (CA-3): assert a present reference is found."""
    raise NotImplementedError '''

def test_find_reference_hit(sample_ledger):
    assert find_reference(sample_ledger, "SYN-001") == "SYN-001"

'''
def test_find_reference_miss_returns_none(sample_ledger):
    """TODO (CA-3): assert an absent reference returns None."""
    raise NotImplementedError '''

def test_find_reference_miss_returns_none(sample_ledger):
    assert find_reference(sample_ledger, "SYN-999") is None