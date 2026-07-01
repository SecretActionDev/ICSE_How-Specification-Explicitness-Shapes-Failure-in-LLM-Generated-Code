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


def test_adjacent_event_boundaries_are_allowed_without_overlap():
    """
    Edge case:
    A meeting ending exactly when an event starts (or starting exactly when it ends)
    should be allowed before the event starts, but the public tests imply a 15-minute
    cooldown after the event ends.
    """
    events = [{"start": "10:00", "end": "10:30"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "09:30" in slots
    assert "10:00" not in slots
    assert "10:30" not in slots
    assert "10:45" in slots


def test_meeting_cannot_cross_lunch_break_even_if_start_before_noon():
    """
    Constraint:
    A meeting must not overlap the lunch break interval (12:00–13:00), even if it
    starts before lunch.
    """
    slots = suggest_slots([], meeting_duration=30, day="2026-02-01")

    assert "11:30" in slots
    assert "11:45" not in slots


def test_event_partially_outside_working_hours_is_clipped():
    """
    Constraint:
    An event overlapping the start of the workday should block only the overlapping
    portion inside working hours.
    """
    events = [{"start": "08:30", "end": "09:30"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "09:00" not in slots
    assert "09:30" not in slots
    assert "09:45" in slots


def test_overlapping_events_are_merged_effectively():
    """
    Edge case:
    Overlapping events should behave like one combined busy interval.
    """
    events = [
        {"start": "10:00", "end": "11:00"},
        {"start": "10:30", "end": "11:30"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "11:00" not in slots
    assert "11:30" not in slots
    assert "13:00" in slots


def test_no_slots_when_morning_and_afternoon_are_fully_blocked():
    """
    Functional requirement:
    Return an empty list when no valid meeting slots exist.
    """
    events = [
        {"start": "09:00", "end": "12:00"},
        {"start": "13:00", "end": "17:00"},
    ]
    slots = suggest_slots(events, meeting_duration=15, day="2026-02-01")

    assert slots == []


def test_slots_are_sorted_and_follow_15_minute_grid():
    """
    Constraint:
    Suggested slots should be sorted ascending and generated on a 15-minute grid.
    """
    slots = suggest_slots([], meeting_duration=15, day="2026-02-01")

    assert slots[0] == "09:00"
    assert slots[-1] == "16:45"
    assert "09:10" not in slots
    assert slots == sorted(slots)


def test_friday_slots_after_1500_are_excluded():
    """
    New requirement:
    On Fridays, meetings must not start after 15:00.
    """
    slots = suggest_slots([], meeting_duration=15, day="2026-02-06")  # Friday

    assert "15:00" in slots
    assert "15:15" not in slots
    assert "16:45" not in slots


def test_non_friday_still_allows_late_afternoon_slots():
    """
    Regression check:
    The Friday cutoff should not affect other days.
    """
    slots = suggest_slots([], meeting_duration=15, day="2026-02-05")  # Thursday

    assert "15:15" in slots
    assert "16:45" in slots
