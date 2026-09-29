"""Tests written against the ledger's stated behaviour. Synthetic data only."""

from ledger import add_entry, total


def test_total_sums_amounts() -> None:
    book = [
        {"reference": "SYN-001", "amount": 10.10},
        {"reference": "SYN-002", "amount": 20.20},
        {"reference": "SYN-003", "amount": 5.05},
    ]
    assert total(book) == 35.35


def test_add_entry_starts_from_an_empty_ledger() -> None:
    first = add_entry("SYN-001", 10.10)
    second = add_entry("SYN-002", 20.20)
    assert len(first) == 1
    assert len(second) == 1

def test_total_is_exact(sample_ledger):
    """Written for you. Run it and read the number in the failure carefully."""
    assert total(sample_ledger) == 35.35


def test_total_of_an_empty_ledger_is_zero():
    """TODO (CA-3): assert the total of an empty ledger."""
    raise NotImplementedError


def test_add_entry_does_not_leak_between_calls():
    """TODO (CA-3): call add_entry twice with no ledger argument, and assert
    that each call returns a ledger of length 1."""
    raise NotImplementedError


def test_add_entry_returns_a_new_list(sample_ledger):
    """TODO (CA-3): add an entry to sample_ledger and assert the original is
    still length 3 while the returned ledger is length 4."""
    raise NotImplementedError

def test_add_entry_returns_a_new_list(sample_ledger):
    extended = add_entry("SYN-001", Decimal("1.00"), sample_ledger)

def test_find_reference_hit(sample_ledger):
    """TODO (CA-3): assert a present reference is found."""
    raise NotImplementedError


def test_find_reference_miss_returns_none(sample_ledger):
    """TODO (CA-3): assert an absent reference returns None."""
    raise NotImplementedError