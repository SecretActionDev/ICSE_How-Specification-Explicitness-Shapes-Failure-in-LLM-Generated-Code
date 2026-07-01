## Student Name:MHD-Oubai Al-khimi
## Student ID: 219533637

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
def test_meeting_fits_exactly_at_end_of_day():
    """Should allow a meeting that ends exactly at 17:00."""
    events = []
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")
    assert "16:00" in slots
    assert "16:15" not in slots  # Would end at 17:15

def test_meeting_too_long_for_any_slot():
    """Should return an empty list if duration is longer than any available gap."""
    # Longest gap is 09:00-12:00 (180 mins) or 13:00-17:00 (240 mins)
    events = []
    slots = suggest_slots(events, meeting_duration=300, day="2026-02-01")
    assert slots == []

def test_event_overlaps_lunch_break():
    """Events overlapping lunch should still block the time outside of lunch."""
    # Event from 11:30 to 13:30. Lunch is already blocked.
    events = [{"start": "11:30", "end": "13:30"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")
    assert "11:15" not in slots # Ends at 11:45 (overlap)
    assert "11:00" in slots     # Ends at 11:30 (no overlap)
    assert "13:30" in slots

def test_back_to_back_meetings_possible():
    """A new meeting should be able to start exactly when another ends."""
    events = [{"start": "09:00", "end": "10:00"}]
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")
    assert "10:00" in slots

def test_no_events_all_day():
    """If no events, all 15-min increments outside lunch should be present."""
    slots = suggest_slots([], 30, "2026-02-01")
    # 09:00 to 11:30 (last start for 30min meeting before lunch)
    assert "09:00" in slots
    assert "11:30" in slots
    # 13:00 to 16:30 (last start for 30min meeting before EOD)
    assert "13:00" in slots
    assert "16:30" in slots
