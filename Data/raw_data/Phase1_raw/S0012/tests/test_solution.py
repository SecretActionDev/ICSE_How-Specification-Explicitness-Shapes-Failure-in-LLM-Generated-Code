## Student Name: Lamisa Quaiyum Shamma
## Student ID: 221448105

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
import pytest
from solution import suggest_slots

def test_single_event_blocks_overlapping_slots():
    """
    Functional requirement:
    Slots overlapping an event must not be suggested.
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:30" not in slots
    assert "11:15" in slots

def test_event_outside_working_hours_is_ignored():
    """
    Constraint:
    Events completely outside working hours should not affect availability.
    """
    events = [{"start": "07:00", "end": "08:00"}]
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "09:00" in slots
    assert "16:00" in slots

def test_unsorted_events_are_handled():
    """
    Constraint:
    Event order should not affect correctness.
    """
    events = [
        {"start": "13:00", "end": "14:00"},
        {"start": "09:30", "end": "10:00"},
        {"start": "11:00", "end": "12:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert  slots[1] == "10:15"
    assert "09:30" not in slots

def test_lunch_break_blocks_all_slots_during_lunch():
    """
    Constraint:
    No meeting may start during the lunch break (12:00–13:00).
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "12:00" not in slots
    assert "12:15" not in slots
    assert "12:30" not in slots
    assert "12:45" not in slots

"""TODO: Add at least 5 additional test cases to test your implementation."""

def test_exact_gap_allows_single_slot():
    """
    Functional requirement:
    If a gap exactly matches the meeting duration (respecting buffer rule),
    that slot should be suggested.
    """
    events = [
        {"start": "09:30", "end": "10:00"},
        {"start": "10:45", "end": "11:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:15" in slots


def test_meeting_longer_than_workday_returns_empty():
    """
    Constraint:
    If meeting duration exceeds working hours, return empty list.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=600, day="2026-02-01")

    assert slots == []


def test_full_day_blocked_returns_empty():
    """
    Functional requirement:
    If events block the entire workday (excluding lunch),
    no slots should be returned.
    """
    events = [
        {"start": "09:00", "end": "12:00"},
        {"start": "13:00", "end": "17:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert slots == []


def test_meeting_can_end_exactly_at_17():
    """
    Boundary condition:
    A meeting ending exactly at 17:00 should be allowed.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "16:00" in slots


def test_event_ending_at_lunch_blocks_properly():
    """
    Constraint:
    Event ending at 12:00 should still enforce lunch restriction.
    """
    events = [
        {"start": "11:00", "end": "12:00"}
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "12:00" not in slots


def test_event_starting_at_9_blocks_early_slots():
    """
    Boundary condition:
    If event starts at 09:00, first available slot must respect buffer rule.
    """
    events = [
        {"start": "09:00", "end": "10:00"}
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "09:00" not in slots
    assert "10:00" not in slots
    assert "10:15" in slots
