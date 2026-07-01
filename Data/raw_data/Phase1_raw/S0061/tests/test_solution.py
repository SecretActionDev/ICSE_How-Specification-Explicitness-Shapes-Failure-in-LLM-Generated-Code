## Student Name:
## Student ID: 

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
import pytest
from src.solution import suggest_slots


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
def test_empty_events_returns_all_valid_slots_except_lunch():
    """
    Functional requirement:
    When there are no events, the system shall suggest all valid start times
    within working hours, excluding restricted periods (e.g., lunch).
    """
    slots = suggest_slots([], meeting_duration=30, day="2026-02-01")

    assert slots[0] == "09:00"
    assert "11:30" in slots
    # Lunch is blocked
    assert "12:00" not in slots
    assert "12:30" not in slots
    # Still returns slots after lunch
    assert "13:00" in slots
    assert "16:30" in slots  # latest 30-min start before 17:00


def test_meeting_must_end_by_work_end_time():
    """
    Constraint:
    Suggested start times must allow the meeting to finish within working hours.
    """
    slots = suggest_slots([], meeting_duration=60, day="2026-02-01")

    assert "16:00" in slots     # 16:00 -> 17:00 OK
    assert "16:15" not in slots # 16:15 -> 17:15 not allowed
    assert "16:30" not in slots # 16:30 -> 17:30 not allowed


def test_back_to_back_events_create_no_gap_slot_between_them():
    """
    Edge case:
    If events are back-to-back, the system shall not suggest a start time
    that overlaps either event (including any required buffer).
    """
    events = [
        {"start": "09:00", "end": "10:00"},
        {"start": "10:00", "end": "11:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "09:00" not in slots
    assert "09:30" not in slots
    assert "10:00" not in slots
    # With the post-event buffer in the provided solution, earliest is 11:15
    assert "11:15" in slots


def test_overlapping_events_are_treated_as_one_blocked_period():
    """
    Constraint:
    Overlapping events shall be handled correctly (effectively blocking their union),
    regardless of how the input events overlap.
    """
    events = [
        {"start": "10:00", "end": "11:00"},
        {"start": "10:30", "end": "12:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:45" not in slots
    assert "11:30" not in slots
    # After the combined block ends (plus buffer in provided solution),
    # 12:00 and 12:15/12:30/12:45 are still blocked by lunch, so first post-lunch slot is fine.
    assert "13:00" in slots


def test_invalid_meeting_duration_returns_empty_list():
    """
    Input validation:
    A non-positive meeting duration shall result in no suggested slots.
    """
    assert suggest_slots([], meeting_duration=0, day="2026-02-01") == []
    assert suggest_slots([], meeting_duration=-15, day="2026-02-01") == []