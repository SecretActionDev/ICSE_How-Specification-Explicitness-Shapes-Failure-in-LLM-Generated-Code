## Student Name:Khawaja Faiza Qaisar
## Student ID: 217948233

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
import sys
import pytest
from pathlib import Path

# Figure out where the 'src' folder is relative to this test file
src_path = str(Path(__file__).resolve().parent.parent / "src")

# Add that folder to the list of places Python looks for code
if src_path not in sys.path:
    sys.path.insert(0, src_path)

#Now you can safely import your code and run pytest
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
    A meeting may NOT start exactly at the end of an event.
    It must start at the next 15‑minute boundary.
    """
    events = [
        {"start": "09:00", "end": "10:00"},
        {"start": "11:00", "end": "12:00"}
    ]
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:15" not in slots
    assert "13:00" not in slots
    assert "13:15" in slots

def test_meeting_cannot_exceed_work_end():
    """
    A meeting must end by 17:00.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=45, day="2026-02-01")

    assert "16:15" in slots
    assert "16:30" not in slots


def test_overlapping_busy_events():
    """
    Overlapping events must merge into one busy block.
    A meeting cannot start exactly at the end of that block.
    """
    events = [
        {"start": "14:00", "end": "15:00"},
        {"start": "14:30", "end": "15:30"}
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "14:00" not in slots
    assert "15:00" not in slots
    assert "15:30" not in slots
    assert "15:45" in slots

def test_no_available_slots_full_day():
    """
    If the entire day is busy, no slots should be returned.
    """
    events = [{"start": "09:00", "end": "17:00"}]
    slots = suggest_slots(events, meeting_duration=15, day="2026-02-01")

    assert slots == []

def test_events_only_for_specific_day():
    """
    Only events matching the requested day should block slots.
    """
    events = [
        {"day": "2026-02-01", "start": "09:30", "end": "10:00"},
        {"day": "2026-02-01", "start": "11:00", "end": "12:00"},
        {"day": "2026-02-02", "start": "09:00", "end": "09:30"},  # Different day
        {"day": "2026-02-02", "start": "14:00", "end": "15:00"}   # Different day
    ]

    # Day 1
    slots_day1 = suggest_slots(events, meeting_duration=30, day="2026-02-01")
    assert "09:00" in slots_day1
    assert "09:30" not in slots_day1
    assert "10:15" in slots_day1
    assert "11:00" not in slots_day1

    # Day 2
    slots_day2 = suggest_slots(events, meeting_duration=30, day="2026-02-02")

    assert "09:00" not in slots_day2
    assert "09:30" not in slots_day2
    assert "09:45" in slots_day2
    assert "14:00" not in slots_day2
    assert "15:00" not in slots_day2
    assert "15:15" in slots_day2


def test_event_starts_before_work_hours():
    """
    Events starting before work hours but ending inside them
    should block early-morning slots.
    """
    events = [{"start": "08:00", "end": "09:30"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "09:00" not in slots
    assert "09:30" not in slots
    assert "09:45" in slots


def test_meeting_duration_longer_than_free_time():
    """
    If the meeting duration is longer than any free block,
    no slots should be returned.
    """
    events = [
        {"start": "09:00", "end": "12:00"},
        {"start": "13:00", "end": "17:00"}
    ]
    slots = suggest_slots(events, meeting_duration=180, day="2026-02-01") 
    assert slots == []


def test_back_to_back_events():
    """
    Events that touch (10:00–11:00 and 11:00–12:00)
    leave no gap for a meeting.
    """
    events = [
        {"start": "10:00", "end": "11:00"},
        {"start": "11:00", "end": "12:00"}
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "11:00" not in slots
    assert "11:15" not in slots
    assert "13:15" in slots



def test_multiple_small_gaps():
    """
    Small gaps that cannot fit the meeting duration should be ignored.
    """
    events = [
        {"start": "09:00", "end": "09:20"},
        {"start": "09:35", "end": "09:50"},
        {"start": "10:05", "end": "10:20"}
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "09:00" not in slots
    assert "09:15" not in slots
    assert "09:30" not in slots
    assert "10:00" not in slots
    assert "10:30" in slots


def test_exact_fit_but_cannot_start_at_event_end():
    """
    Even if a meeting fits exactly between events,
    it cannot start at the event end time.
    """
    events = [
        {"start": "09:00", "end": "10:00"},
        {"start": "10:45", "end": "12:00"}
    ]
    slots = suggest_slots(events, meeting_duration=45, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:15" not in slots
    assert "13:15" in slots


def test_invalid_event_ignored():
    """
    Events with end <= start should be ignored.
    """
    events = [
        {"start": "10:00", "end": "09:00"},  # invalid
        {"start": "13:00", "end": "14:00"}
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "09:00" in slots
    assert "10:00" in slots
    assert "10:30" in slots
    assert "13:00" not in slots


def test_duplicate_events():
    """
    Duplicate events should not affect correctness.
    """
    events = [
        {"start": "10:00", "end": "11:00"},
        {"start": "10:00", "end": "11:00"} 
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:30" not in slots
    assert "11:15" in slots


##The new Testcases
def test_friday_no_events_duration_60():
    events = []
    result = suggest_slots(events, meeting_duration=60, day="Friday")
    assert "15:00" in result
    assert "15:15" not in result
    assert result[0] == "09:00"


def test_friday_short_meeting():
    events = []
    result = suggest_slots(events, meeting_duration=30, day="Friday")
    assert "15:00" in result
    assert "15:15" not in result


def test_friday_event_until_1445():
    events = [
        {"day": "Friday", "start": "14:00", "end": "14:45"}
    ]
    result = suggest_slots(events, meeting_duration=30, day="Friday")
    assert "15:00" in result
    assert "15:15" not in result

def test_friday_event_ends_at_1500():
    events = [
        {"day": "Friday", "start": "14:00", "end": "15:00"}
    ]
    result = suggest_slots(events, meeting_duration=30, day="Friday")
    assert "15:00" not in result #because event ends at 15
    assert "15:15" not in result

def test_friday_long_meeting_cannot_start_at_1500():
    events = []
    result = suggest_slots(events, meeting_duration=120, day="Friday")
    assert "15:00" in result
    assert "15:15" not in result


def test_monday_no_restriction():
    events = []
    result = suggest_slots(events, meeting_duration=60, day="Monday")
    assert "15:00" in result
    assert "15:15" in result
    assert "16:00" in result


def test_monday_event_ends_at_1500():
    events = [
        {"day": "Monday", "start": "14:00", "end": "15:00"}
    ]
    result = suggest_slots(events, meeting_duration=30, day="Monday")
    assert "15:15" in result


