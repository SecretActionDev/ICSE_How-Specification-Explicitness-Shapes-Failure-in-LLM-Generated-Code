## Student Name: Wenhao Zhu
## Student ID: 219171156

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

    assert slots[1] == "10:15"
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


# -------------------------------------------------------------------
# Additional tests (at least 5)
# -------------------------------------------------------------------

def test_event_ending_at_slot_start_does_not_block():
    """
    Edge case:
    If an event ends exactly when the meeting would start, it should NOT overlap.
    """
    events = [{"start": "09:00", "end": "10:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" in slots
    assert "09:45" not in slots  # would overlap the event


def test_event_starting_at_meeting_end_does_not_block():
    """
    Edge case:
    If an event starts exactly when the meeting would end, it should NOT overlap.
    """
    events = [{"start": "10:30", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" in slots  # meeting [10:00,10:30) ends exactly at event start
    assert "10:15" not in slots  # meeting [10:15,10:45) overlaps


def test_back_to_back_events_merge_and_block_gapless_window():
    """
    Constraint:
    Back-to-back events should block the entire combined window.
    """
    events = [
        {"start": "10:00", "end": "10:30"},
        {"start": "10:30", "end": "11:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:15" not in slots
    assert "10:30" not in slots
    assert "11:00" in slots


def test_overlapping_events_are_merged():
    """
    Constraint:
    Overlapping events should be treated as one busy interval.
    """
    events = [
        {"start": "09:30", "end": "10:30"},
        {"start": "10:00", "end": "11:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "09:30" not in slots
    assert "10:15" not in slots
    assert "11:00" in slots


def test_meeting_too_long_returns_empty():
    """
    Edge case:
    If the meeting duration cannot fit in the working day (after constraints),
    there should be no suggested slots.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=8 * 60 + 1, day="2026-02-01")
    assert slots == []


def test_event_partially_outside_work_hours_is_clipped():
    """
    Constraint:
    An event overlapping working hours should block only the overlapping portion.
    """
    events = [{"start": "16:30", "end": "18:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "16:00" in slots        # [16:00,16:30) OK
    assert "16:15" not in slots    # overlaps [16:30,17:00)
    assert "16:30" not in slots    # starts inside busy portion


def test_invalid_event_is_ignored():
    """
    Edge case:
    An invalid event (end <= start) should not break the function and should be ignored.
    """
    events = [{"start": "11:00", "end": "11:00"}, {"start": "14:00", "end": "13:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "11:15" in slots
    assert "14:15" in slots


def test_no_slots_start_during_lunch_for_longer_meeting():
    """
    Constraint:
    Lunch break start restriction should still apply even for longer meetings.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "12:00" not in slots
    assert "12:15" not in slots
    assert "12:30" not in slots
    assert "12:45" not in slots

def test_friday_cutoff_excludes_after_1500():
    # No events: normally we'd get slots up to 16:00 for a 60-min meeting,
    # but on Friday we must exclude anything starting after 15:00.
    events = []
    res = suggest_slots(events, meeting_duration=60, day="Fri")

    assert "15:00" in res
    assert "15:15" not in res
    assert "15:30" not in res
    assert "16:00" not in res


def test_friday_cutoff_even_if_long_meeting_still_caps_by_start_time():
    # 120-min meeting: on a normal day latest start is 15:00 (ends at 17:00)
    # Friday cutoff is also 15:00, so "15:00" should be allowed, "15:15" not.
    events = []
    res = suggest_slots(events, meeting_duration=120, day="Fri")

    assert "15:00" in res
    assert "15:15" not in res


def test_non_friday_not_capped_at_1500():
    # Same as first test, but not Friday: 60-min meeting can start at 16:00.
    events = []
    res = suggest_slots(events, meeting_duration=60, day="Thu")

    assert "16:00" in res
    assert "16:15" not in res  # would end after 17:00


def test_friday_cutoff_with_busy_time_before_cutoff():
    # Busy from 14:00-15:00 means 15:00 is still a valid start (meeting starts at 15:00).
    # But anything after 15:00 is still excluded by Friday rule.
    events = [{"start": "14:00", "end": "15:00"}]
    res = suggest_slots(events, meeting_duration=30, day="Fri")

    assert "15:00" in res
    assert "15:15" not in res