## Student Name: Evan Gocool
## Student ID: 220178398

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

    assert "09:30" not in slots
    assert "11:00" not in slots
    assert "10:00" in slots
    assert "10:15" in slots

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

def test_meeting_exactly_fits_before_event():
    """
    A meeting that ends exactly when an event starts should be allowed.
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "09:00" in slots
    assert "10:00" not in slots


def test_meeting_exactly_fits_after_event():
    """
    A meeting that starts exactly when an event ends should be allowed.
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "11:00" in slots


def test_no_slots_available_when_day_is_fully_booked():
    """
    If the entire working day is blocked, no slots should be returned.
    """
    events = [{"start": "09:00", "end": "17:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert slots == []

def test_meeting_does_not_extend_past_working_hours():
    """
    A meeting that would extend past 17:00 should not be suggested.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=120, day="2026-02-01")

    assert "15:00" in slots     # 15:00–17:00 ✔
    assert "15:15" not in slots
    assert "16:00" not in slots

def test_multiple_events_block_combined_time_range():
    """
    Multiple events should collectively block overlapping slots.
    """
    events = [
        {"start": "10:00", "end": "10:30"},
        {"start": "10:30", "end": "11:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:15" not in slots
    assert "10:30" not in slots
    assert "11:00" in slots

def test_friday_meetings_do_not_start_after_1500():
    """
    Constraint:
    On Fridays, meetings may not start after 15:00.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="Fri")

    assert "14:45" in slots      # Still allowed
    assert "15:00" in slots      # Last allowed start time
    assert "15:15" not in slots  # Not allowed
