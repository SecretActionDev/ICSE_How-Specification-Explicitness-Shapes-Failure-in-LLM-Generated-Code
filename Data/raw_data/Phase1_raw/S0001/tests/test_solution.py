## Student Name:Khawaja Faiza Qaisar
## Student ID: 217948233

## USed this command to ran my tests: export PYTHONPATH=$PYTHONPATH:$(pwd)/src && pytest -v

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

def test_tight_fit_between_events():
    """
    Checks if a slot is suggested when it fits perfectly between two events.
    """
    events = [
        {"start": "09:00", "end": "10:00"},
        {"start": "11:00", "end": "12:00"}
    ]
    # A 60-min meeting should fit exactly at 10:00
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")
    assert "10:00" in slots
    assert "10:15" not in slots # Because 10:15 + 60 mins would hit the 11:00 event

def test_meeting_cannot_exceed_work_end():
    """
    A meeting must end by 17:00. 
    A 45-min meeting starting at 16:30 should be invalid.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=45, day="2026-02-01")
    
    assert "16:15" in slots # Ends at 17:00
    assert "16:30" not in slots # Ends at 17:15 (Overtime)

def test_overlapping_busy_events():
    """
    If two events overlap (14:00-15:00 and 14:30-15:30), 
    the logic should treat the whole block as busy.
    """
    events = [
        {"start": "14:00", "end": "15:00"},
        {"start": "14:30", "end": "15:30"}
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")
    
    assert "14:00" not in slots
    assert "15:00" not in slots
    assert "15:30" in slots

def test_no_available_slots_full_day():
    """
    If the schedule is completely packed, return an empty list.
    """
    events = [{"start": "09:00", "end": "17:00"}]
    slots = suggest_slots(events, meeting_duration=15, day="2026-02-01")
    
    assert slots == []

def test_earliest_possible_slot():
    """
    Ensures the very first slot of the day is suggested if free.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=15, day="2026-02-01")
    
    assert slots[0] == "09:00"