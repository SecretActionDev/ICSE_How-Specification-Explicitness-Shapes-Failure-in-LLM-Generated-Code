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
