## Student Name: Brandon Ngo
## Student ID: 218777714

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
def test_meeting_duration_boundary_end_of_day():
    """
    Duration and end-of-day boundary:
    For 90-min meetings, last valid start is 15:30 (ends 17:00).
    """
    events = []
    slots = suggest_slots(events, meeting_duration=90, day="2026-02-01")

    assert "15:30" in slots
    assert "15:45" not in slots


def test_event_crossing_work_start_clips_morning_slot():
    """
    Constraint:
    Events that start before working hours and end after 09:00 block early slots.
    """
    events = [{"start": "08:50", "end": "09:10"}]
    slots = suggest_slots(events, meeting_duration=15, day="2026-02-01")

    assert "09:00" not in slots
    assert "09:15" in slots


def test_back_to_back_events_leave_no_gap():
    """
    Constraint:
    Back-to-back events cover the entire interval without gaps.
    """
    events = [
        {"start": "09:00", "end": "09:45"},
        {"start": "09:45", "end": "10:00"},
    ]
    slots = suggest_slots(events, meeting_duration=15, day="2026-02-01")

    assert "09:45" not in slots
    assert "10:00" in slots


def test_lunch_boundary_for_one_hour_meeting():
    """
    Constraint:
    60-min meetings must not cross lunch; 11:00 is valid, 11:15 is not.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "11:00" in slots
    assert "11:15" not in slots


def test_empty_day_slot_count_for_30_min():
    """
    Sanity:
    On an empty day, 30-min meetings have 26 starts (11 morning + 15 afternoon).
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert len(slots) == 26
    assert slots[0] == "09:00"
    assert slots[-1] == "16:30"


def test_friday_no_meetings_after_15_00():
    """
    Constraint:
    On Fridays, no meetings may start after 15:00.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-06")  # Friday

    assert "15:00" in slots
    assert "15:15" not in slots
    assert "15:30" not in slots
    assert "16:00" not in slots


def test_friday_empty_day_reduced_slot_count():
    """
    Constraint:
    On an empty Friday, 30-min meetings have only 18 starts (not 26).
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-13")  # Friday

    # Morning: 09:00 to 11:30 = 11 slots
    # Afternoon: 13:00 to 15:00 = 9 slots (stop at 15:00, not 16:30)
    # Total = 20 slots
    assert len(slots) == 20
    assert slots[-1] == "15:00"


def test_non_friday_unaffected_by_friday_rule():
    """
    Constraint:
    Non-Friday days should allow meetings after 15:00.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-05")  # Thursday

    assert "15:15" in slots
    assert "16:00" in slots
    assert "16:30" in slots
