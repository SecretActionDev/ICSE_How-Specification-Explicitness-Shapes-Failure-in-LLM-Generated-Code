## Student Name: Manya Khattri
## Student ID: 219830025

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

    assert "10:15" in slots
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

def test_meeting_fits_exactly_before_event():
    """
    Edge case:
    Meeting that ends exactly when an event starts should be allowed.
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-02")

    assert "09:30" in slots
    assert "10:00" not in slots


def test_meeting_fits_exactly_after_event():
    """
    Edge case:
    Meeting that starts exactly when an event ends should be allowed.
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-02")

    assert "11:00" in slots


def test_meeting_too_long_for_remaining_day():
    """
    Edge case:
    Meeting duration exceeds remaining working hours.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=120, day="2026-02-02")

    assert "16:00" not in slots
    assert "15:00" in slots


def test_event_partially_overlapping_work_start():
    """
    Edge case:
    Event that starts before working hours but overlaps the start of the day.
    """
    events = [{"start": "08:30", "end": "09:30"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-02")

    assert "09:00" not in slots
    assert "09:30" in slots


def test_multiple_events_create_gap():
    """
    Edge case:
    A gap between events should produce valid meeting slots.
    """
    events = [
        {"start": "09:00", "end": "10:00"},
        {"start": "10:30", "end": "11:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-02")

    assert "10:00" in slots
    assert "10:15" not in slots

def test_friday_no_meetings_start_at_or_after_1500():
    """
    New requirement:
    On Fridays, meetings must not start at or after 15:00.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-06")  # Friday

    assert "15:00" not in slots
    assert "15:15" not in slots
    assert "16:00" not in slots


def test_friday_meetings_before_1500_are_allowed():
    """
    New requirement:
    Meetings starting before 15:00 on Fridays should be allowed.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-06")  # Friday

    assert "14:30" in slots
    assert "14:45" in slots


def test_friday_long_meeting_starting_before_1500_is_allowed():
    """
    Clarification:
    On Fridays, meetings are allowed as long as they START before 15:00,
    even if they end after 15:00.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-06")  # Friday

    assert "14:30" in slots
    assert "15:00" not in slots


def test_non_friday_allows_1500_start():
    """
    Control test:
    On non-Fridays, meetings may start at 15:00.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-05")  # Thursday

    assert "15:00" in slots
    assert "15:15" in slots


def test_friday_with_events_still_respects_cutoff():
    """
    Combined constraint:
    Friday cutoff applies even when events exist.
    """
    events = [{"start": "13:00", "end": "14:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-06")  # Friday

    assert "14:00" in slots
    assert "14:30" in slots
    assert "15:00" not in slots
