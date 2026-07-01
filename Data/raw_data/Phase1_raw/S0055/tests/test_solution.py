## Student Name: Daksh Dave 
## Student ID: 219241983

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

def test_buffer_after_event():
    """
    No meeting may start exactly after the event ends and should start only after 15min has passed minimum.
    """
    events = [{"start": "9:00", "end": "10:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:15" in slots

def test_lunch_time_not_allowed():
    """
    Meeting cannot be held under lunch time periods 12:00 to 13:00
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=50, day="2026-02-01")

    assert "11:15" not in slots
    assert "12:00" not in slots

def test_event_working_hours():
    events = [{"start": "08:00", "end": "09:10"}]  # overlaps start of workday
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "09:00" not in slots   
    assert "09:30" in slots 

def test_overlapping_events_merged_buffer():
    events = [
        {"start": "10:00", "end": "10:30"},             #overlaping events will be merged
        {"start": "10:20", "end": "11:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "11:00" not in slots
    assert "11:15" in slots

def test_latest_start_time_insideworkhours():   #if meeting time slot starts or ends after work hours, it should not be allowed
    events = []

    slots1 = suggest_slots(events, meeting_duration=60, day="2026-02-01")
    assert "16:00" in slots1
    assert "16:15" not in slots1

    slots2 = suggest_slots(events, meeting_duration=30, day="2026-02-01")
    assert "16:30" in slots2
    assert "16:45" not in slots2