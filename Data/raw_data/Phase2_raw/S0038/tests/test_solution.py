## Student Name: Ashik Acharya
## Student ID: 219611565

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
def test_fully_booked_day_returns_no_slots():
    """
    Edge case:
    If the entire working day is booked (except lunch), no slots should exist.
    """
    events = [
        {"start": "09:00", "end": "12:00"},
        {"start": "13:00", "end": "17:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert slots == []


def test_meeting_duration_too_long_for_day():
    """
    Edge case:
    Meeting duration longer than total available working hours.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=600, day="2026-02-01")

    assert slots == []


def test_event_covers_entire_working_day():
    """
    Edge case:
    A single event covering the whole workday should leave no slots.
    """
    events = [{"start": "09:00", "end": "17:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert slots == []


def test_event_ending_at_lunch_blocks_before_lunch_slots():
    """
    Edge case:
    Event ending exactly at 12:00 should block meetings that overlap into lunch.
    """
    events = [{"start": "11:00", "end": "12:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "11:30" not in slots
    assert "10:15" in slots


def test_event_ending_at_work_start_allows_first_slot():
    """
    Edge case:
    Event ending exactly at 09:00 should not block the first slot.
    """
    events = [{"start": "08:00", "end": "09:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "09:00" in slots

def test_friday_no_slots_after_1500_with_short_day_string():
    """
    Friday rule:
    Meetings must not start after 15:00 on Fridays ("Fri").
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="Fri")

    assert "15:00" in slots
    assert "15:15" not in slots
    assert "15:30" not in slots
    assert "16:00" not in slots


def test_friday_no_slots_after_1500_with_full_day_string():
    """
    Friday rule:
    Meetings must not start after 15:00 when day="Friday".
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="Friday")

    assert "15:00" in slots
    assert "15:15" not in slots
    assert "16:00" not in slots


def test_friday_1500_slot_is_valid():
    """
    Friday rule:
    A meeting starting exactly at 15:00 on Friday is allowed.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="Fri")

    assert "15:00" in slots


def test_non_friday_allows_slots_after_1500():
    """
    Control test:
    Non-Friday days should still allow slots after 15:00.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="Mon")

    assert "15:15" in slots
    assert "16:00" in slots