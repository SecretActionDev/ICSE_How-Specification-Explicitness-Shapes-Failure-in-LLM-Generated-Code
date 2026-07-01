## Student Name: Clarence Corpuz    
## Student ID: 218848291

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
def test_combined_constraints_regular_day():
    events = [
        {"start": "09:30", "end": "10:15"},
        {"start": "13:30", "end": "14:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="Mon")

    assert "09:00" in slots
    assert "09:30" not in slots
    assert "10:15" in slots
    assert "12:00" not in slots
    assert "12:45" not in slots
    assert "13:30" not in slots


def test_events_outside_working_hours_and_unsorted():
    events = [
        {"start": "18:00", "end": "19:00"},
        {"start": "08:00", "end": "08:30"},
        {"start": "10:00", "end": "10:30"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="Tue")

    assert "09:00" in slots
    assert "10:00" not in slots
    assert "10:30" in slots


def test_lunch_break_and_long_meeting():
    events = []
    slots = suggest_slots(events, meeting_duration=90, day="Wed")

    assert "10:30" in slots
    assert "11:00" not in slots   # overlaps lunch
    assert "12:00" not in slots
    assert "13:00" in slots


def test_friday_cutoff_with_other_constraints():
    events = [
        {"start": "14:00", "end": "14:30"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="Fri")

    assert "14:30" in slots
    assert "15:00" not in slots
    assert "15:15" not in slots
    assert "12:30" not in slots


def test_no_available_slots_returns_empty():
    events = [
        {"start": "09:00", "end": "12:00"},
        {"start": "13:00", "end": "15:00"},
    ]
    slots = suggest_slots(events, meeting_duration=60, day="Fri")

    assert slots == []


def test_friday_no_slots_after_1500():
    """
    Constraint:
    On Fridays, meetings must not start after 15:00.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="Fri")

    assert "15:00" in slots
    assert "15:15" not in slots
    assert "16:00" not in slots


def test_friday_event_does_not_enable_late_start():
    """
    Constraint:
    Even if an event ends late, Friday meetings cannot start after 15:00.
    """
    events = [{"start": "14:00", "end": "14:30"}]
    slots = suggest_slots(events, meeting_duration=30, day="Fri")

    assert "14:30" in slots
    assert "15:15" not in slots


def test_friday_long_meeting_must_start_before_1500():
    """
    Constraint:
    Long meetings on Friday must still start no later than 15:00.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=90, day="Fri")

    assert "14:30" in slots
    assert "15:00" not in slots


def test_non_friday_allows_late_start():
    """
    Control test:
    Non-Friday days should still allow starts after 15:00.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="Thu")

    assert "15:15" in slots
    assert "16:00" in slots


def test_friday_with_busy_morning_still_blocks_late_start():
    """
    Constraint:
    Even if morning is fully booked, Friday late starts are still forbidden.
    """
    events = [
        {"start": "09:00", "end": "12:00"},
        {"start": "13:00", "end": "14:30"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="Fri")

    assert "14:30" in slots
    assert "15:00" not in slots
    assert "15:15" not in slots
