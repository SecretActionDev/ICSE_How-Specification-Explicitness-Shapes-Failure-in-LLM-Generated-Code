## Student Name: Daniel Ferlisi
## Student ID: 218714923

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
def test_meeting_can_end_exactly_at_work_end():
    """
    Edge case:
    A meeting is allowed to end exactly at 17:00.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "16:00" in slots
    assert "16:15" not in slots


def test_event_with_buffer_blocks_next_slot():
    """
    Constraint:
    A meeting cannot start until 15 minutes after an event ends.
    """
    events = [{"start": "10:00", "end": "10:30"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:30" not in slots
    assert "10:45" in slots


def test_event_partially_overlapping_working_hours():
    """
    Edge case:
    Events partially outside working hours should be clamped.
    """
    events = [{"start": "08:30", "end": "09:30"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "09:00" not in slots
    assert "09:45" in slots


def test_multiple_overlapping_events():
    """
    Constraint:
    Multiple overlapping events should block the full combined interval.
    """
    events = [
        {"start": "10:00", "end": "11:00"},
        {"start": "10:30", "end": "12:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "11:30" not in slots
    assert "12:15" not in slots  # blocked by lunch
    assert "13:00" in slots


def test_empty_event_list_respects_lunch_break():
    """
    Constraint:
    Lunch break blocks slots even when no events exist.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=15, day="2026-02-01")

    assert "11:45" in slots
    assert "12:00" not in slots
    assert "12:30" not in slots
    assert "13:00" in slots
