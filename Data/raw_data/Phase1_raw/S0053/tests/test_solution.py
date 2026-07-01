## Student Name:
## Student ID: 

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""

from pathlib import Path
import sys

sys.path.append(str((Path(__file__).parent.parent / 'src').resolve()))
print(sys.path)


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

def test_no_events_returns_full_workday_except_lunch():
    """
    Baseline:
    With no events, all 15-min grid slots in 09:00–17:00 should be available,
    except starts during lunch (12:00–13:00).
    """
    slots = suggest_slots([], meeting_duration=30, day="2026-02-01")

    assert "09:00" in slots
    assert "11:30" in slots
    assert "12:00" not in slots
    assert "12:45" not in slots
    assert "13:00" in slots
    assert "16:30" in slots  # 16:30–17:00 fits


def test_meeting_duration_longer_than_any_free_block_returns_empty():
    """
    Constraint:
    If the requested duration cannot fit anywhere, return [].
    Lunch splits the day into 09:00–12:00 (180m) and 13:00–17:00 (240m).
    241m cannot fit.
    """
    slots = suggest_slots([], meeting_duration=241, day="2026-02-01")
    assert slots == []


def test_meeting_duration_240_does_not_fit_if_afternoon_is_shortened():
    """
    Constraint:
    240m would fit 13:00–17:00, so add an event that reduces afternoon availability.
    """
    events = [{"start": "16:00", "end": "16:30"}]  # cooldown makes busy until 16:45
    slots = suggest_slots(events, meeting_duration=240, day="2026-02-01")
    assert slots == []


def test_event_touching_work_start_blocks_start_and_adds_cooldown():
    """
    Edge:
    Event begins at work start; cooldown blocks 09:30 start too.
    """
    events = [{"start": "09:00", "end": "09:15"}]  # cooldown makes it busy until 09:30
    slots = suggest_slots(events, meeting_duration=15, day="2026-02-01")

    assert "09:00" not in slots
    assert "09:15" not in slots
    assert "09:30" in slots


def test_event_end_near_work_end_limits_latest_start_with_duration():
    """
    Edge:
    Even if time is free, start must allow meeting to finish by 17:00.
    """
    events = [{"start": "15:00", "end": "16:45"}]  # cooldown pushes to 17:00
    slots = suggest_slots(events, meeting_duration=15, day="2026-02-01")

    # cooldown blocks starts >= 15:00; the last possible starts should be before 15:00
    assert "14:45" in slots
    assert "15:00" not in slots
    assert "16:45" not in slots
    assert "16:45" not in slots
    assert "16:45" not in slots
    assert "16:45" not in slots
    assert "16:45" not in slots


def test_overlapping_events_merge_and_cooldown_applied_to_latest_end():
    """
    Correctness:
    Overlapping events should merge; cooldown effectively applies to the merged block end.
    """
    events = [
        {"start": "10:00", "end": "10:30"},
        {"start": "10:20", "end": "11:00"},  # overlaps; latest end is 11:00 -> busy until 11:15
    ]
    slots = suggest_slots(events, meeting_duration=15, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:30" not in slots
    assert "11:00" not in slots
    assert "11:15" in slots


def test_back_to_back_events_create_continuous_block_with_cooldown():
    """
    Correctness:
    Back-to-back events should produce a continuous busy interval; cooldown extends after the last.
    """
    events = [
        {"start": "09:30", "end": "10:00"},
        {"start": "10:00", "end": "10:30"},
    ]  # cooldown extends to 10:45
    slots = suggest_slots(events, meeting_duration=15, day="2026-02-01")

    assert "09:30" not in slots
    assert "10:30" not in slots
    assert "10:45" in slots


def test_event_partially_overlapping_working_hours_is_clamped_and_still_blocks():
    """
    Constraint:
    Event partly outside working hours should be clamped but still block overlapping time,
    and cooldown still matters within the window.
    """
    events = [{"start": "08:30", "end": "09:10"}]  # within workday: 09:00–09:10, cooldown to 09:25 -> grid => 09:30
    slots = suggest_slots(events, meeting_duration=15, day="2026-02-01")

    assert "09:00" not in slots
    assert "09:15" not in slots
    assert "09:30" in slots


def test_lunch_has_no_cooldown_allows_13_00_start():
    """
    Constraint:
    Lunch blocks 12:00–13:00, but does NOT add cooldown, so 13:00 is allowed.
    """
    slots = suggest_slots([], meeting_duration=30, day="2026-02-01")

    assert "13:00" in slots
    assert "12:45" not in slots


def test_weekend_string_blocks_all_slots():
    """
    Constraint:
    If day is explicitly Saturday/Sunday (string), return [].
    """
    assert suggest_slots([], meeting_duration=30, day="Saturday") == []
    assert suggest_slots([], meeting_duration=30, day="sun") == []


def test_duration_not_multiple_of_step_still_works():
    """
    Robustness:
    Duration doesn't have to be a multiple of 15; start times are still on a 15-min grid.
    """
    slots = suggest_slots([], meeting_duration=20, day="2026-02-01")

    assert "09:00" in slots
    assert "16:45" not in slots  # 16:45–17:05 would exceed work end
    assert "16:30" in slots      # 16:30–16:50 fits
