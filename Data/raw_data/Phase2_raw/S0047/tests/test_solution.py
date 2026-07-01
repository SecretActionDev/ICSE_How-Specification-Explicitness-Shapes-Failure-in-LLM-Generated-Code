## Student Name: Peter Saleeb
## Student ID: 215605322

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
import pytest
from src.solution import suggest_slots

TEST_DAY = "2026-02-01"


def test_single_event_blocks_overlapping_slots():
    """
    Functional requirement:
    Slots overlapping an event must not be suggested.
    """
    events = [{
        "start": "10:00",
        "end": "11:00",
        "day": TEST_DAY
    }]

    slots = suggest_slots(events, meeting_duration=30, day=TEST_DAY)

    assert "10:00" not in slots
    assert "10:30" not in slots
    assert "11:15" in slots


def test_event_outside_working_hours_is_ignored():
    """
    Constraint:
    Events completely outside working hours should not affect availability.
    """
    events = [{
        "start": "07:00",
        "end": "08:00",
        "day": TEST_DAY
    }]

    slots = suggest_slots(events, meeting_duration=60, day=TEST_DAY)

    assert "09:00" in slots
    assert "16:00" in slots


def test_unsorted_events_are_handled():
    """
    Constraint:
    Event order should not affect correctness.
    """
    events = [
        {"start": "13:00", "end": "14:00", "day": TEST_DAY},
        {"start": "09:30", "end": "10:00", "day": TEST_DAY},
        {"start": "11:00", "end": "12:00", "day": TEST_DAY},
    ]

    slots = suggest_slots(events, meeting_duration=30, day=TEST_DAY)

    assert slots[1] == "10:00"
    assert "09:30" not in slots


def test_lunch_break_blocks_all_slots_during_lunch():
    """
    Constraint:
    No meeting may start during the lunch break (12:00–13:00).
    """
    slots = suggest_slots([], meeting_duration=30, day=TEST_DAY)

    assert "12:00" not in slots
    assert "12:15" not in slots
    assert "12:30" not in slots
    assert "12:45" not in slots


def test_invalid_meeting_duration_returns_empty():
    """
    Edge case:
    Invalid meeting duration should return empty list.
    """
    events = [{
        "start": "09:00",
        "end": "10:00",
        "day": TEST_DAY
    }]

    assert suggest_slots(events, meeting_duration="30", day=TEST_DAY) == []
    assert suggest_slots(events, meeting_duration=25 * 60, day=TEST_DAY) == []


def test_invalid_events_are_ignored():
    """
    Edge case:
    If events are malformed, assume no valid events.
    """
    events = [
        {"start": "10:00", "day": TEST_DAY},                  # missing end
        {"start": "11:00", "end": "10:00", "day": TEST_DAY},  # end before start
        {"start": "xx:yy", "end": "12:00", "day": TEST_DAY},  # invalid time
    ]

    slots = suggest_slots(events, meeting_duration=30, day=TEST_DAY)

    assert "09:00" in slots
    assert "10:00" in slots


def test_mix_of_invalid_and_valid_events():
    """
    Edge case:
    If some events are malformed, only those malformed events are ignored.
    """
    events = [
        {"start": "10:00", "day": TEST_DAY},                  # missing end
        {"start": "11:00", "end": "10:00", "day": TEST_DAY},  # invalid range
        {"start": "xx:yy", "end": "12:00", "day": TEST_DAY},  # invalid time
        {"start": "09:20", "end": "10:00", "day": TEST_DAY},  # valid
    ]

    slots = suggest_slots(events, meeting_duration=30, day=TEST_DAY)

    assert "09:00" not in slots
    assert "10:00" in slots


def test_invalid_day_assumes_today():
    """
    Rule:
    Invalid day should default to today.
    """
    events = [{
        "start": "09:00",
        "end": "10:00",
        "day": "2099-01-01"  # should be ignored
    }]

    slots = suggest_slots(events, meeting_duration=30, day="NotADay")

    assert "09:00" in slots
    assert "10:00" in slots


def test_meeting_cannot_extend_past_working_hours():
    """
    Constraint:
    Meeting must fully fit within working hours.
    """
    slots = suggest_slots([], meeting_duration=90, day=TEST_DAY)

    assert "15:30" in slots      # ends exactly at 17:00
    assert "16:00" not in slots  # would end at 17:30

def test_events_on_other_days_are_ignored():
    events = [
        {"start": "09:00", "end": "10:00", "day": "2026-02-02"},
        {"start": "11:00", "end": "12:00", "day": TEST_DAY},
    ]

    slots = suggest_slots(events, meeting_duration=30, day=TEST_DAY)

    assert "09:00" in slots
    assert "11:00" not in slots

def test_weekday_abbreviation_uses_next_occurrence():
    events = []

    slots = suggest_slots(events, meeting_duration=60, day="mon")

    assert slots  # should not crash or be empty

def test_zero_length_event_is_ignored():
    events = [{
        "start": "10:00",
        "end": "10:00",
        "day": TEST_DAY
    }]

    slots = suggest_slots(events, meeting_duration=30, day=TEST_DAY)

    assert "10:00" in slots

def test_overlapping_events_block_union():
    events = [
        {"start": "09:30", "end": "10:30", "day": TEST_DAY},
        {"start": "10:00", "end": "11:00", "day": TEST_DAY},
    ]

    slots = suggest_slots(events, meeting_duration=30, day=TEST_DAY)

    assert "09:30" not in slots
    assert "10:30" not in slots
    assert "11:00" in slots

def test_no_meetings_after_3pm_friday():
    events = [
        {"start": "09:30", "end": "10:30", "day": TEST_DAY}, 
        {"start": "13:00", "end": "14:00", "day": TEST_DAY},
    ]

    slots = suggest_slots(events, meeting_duration=30, day="fri")

    assert "15:00" not in slots
    assert "16:00" not in slots