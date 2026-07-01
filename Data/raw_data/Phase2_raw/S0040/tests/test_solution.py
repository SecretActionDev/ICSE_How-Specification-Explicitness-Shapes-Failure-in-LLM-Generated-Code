## Student Name: Kyle Williamson
## Student ID: 218953901

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

def test_ac1_find_available_slots_between_meetings():
    """AC1: Find Available Slots Between Meetings"""
    events = [
        {"start": "09:00", "end": "10:00"},
        {"start": "11:00", "end": "12:00"},
        {"start": "14:00", "end": "15:00"}
    ]
    result = suggest_slots(events, 30, "Mon")
    print("AC1 - Available Slots Between Meetings:")
    print(f"Result: {result}")
    print(f"Expected: ['10:00', '10:30', '12:00', '12:30', '13:00', '13:30', '15:00', '15:30', '16:00', '16:30']\n")


def test_ac2_empty_calendar_full_day():
    """AC2: Empty Calendar Returns Full Day Availability"""
    events = []
    result = suggest_slots(events, 60, "Tue")
    print("AC2 - Empty Calendar:")
    print(f"Result: {result}")
    print(f"Expected: ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00']\n")


def test_ac3_no_slots_when_fully_booked():
    """AC3: No Available Slots When Fully Booked"""
    events = [
        {"start": "09:00", "end": "13:00"},
        {"start": "13:00", "end": "17:00"}
    ]
    result = suggest_slots(events, 30, "Wed")
    print("AC3 - Fully Booked Calendar:")
    print(f"Result: {result}")
    print(f"Expected: []\n")


def test_ac4_meeting_duration_exceeds_gaps():
    """AC4: Meeting Duration Exceeds Available Gaps"""
    events = [
        {"start": "09:00", "end": "11:00"},
        {"start": "12:00", "end": "14:00"}
    ]
    result = suggest_slots(events, 120, "Thu")
    print("AC4 - Long Meeting Duration:")
    print(f"Result: {result}")
    print(f"Expected: ['14:00', '14:30', '15:00'] (slots where 120 min fits before 17:00)\n")


def test_ac5_handles_back_to_back_meetings():
    """AC5: Handles Back-to-Back Meetings"""
    events = [
        {"start": "09:00", "end": "10:00"},
        {"start": "10:00", "end": "11:00"}
    ]
    result = suggest_slots(events, 30, "Fri")
    print("AC5 - Back-to-Back Meetings (Friday):")
    print(f"Result: {result}")
    print(f"Expected: ['11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30'] (stops at 15:00 for Friday)\n")


def test_ac6_respects_end_of_business_day():
    """AC6: Respects End of Business Day Boundary"""
    events = [
        {"start": "09:00", "end": "16:00"}
    ]
    result = suggest_slots(events, 90, "Mon")
    print("AC6 - End of Business Day Boundary:")
    print(f"Result: {result}")
    print(f"Expected: [] (only 60 minutes left, need 90)\n")


def test_friday_restriction():
    """Test Friday 15:00 End Time Restriction"""
    events = [
        {"start": "09:00", "end": "10:00"}
    ]
    result = suggest_slots(events, 60, "Fri")
    print("Friday Restriction Test:")
    print(f"Result: {result}")
    print(f"Expected: ['10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00']")
    print(f"Note: 14:30 is NOT included because 14:30 + 60 min = 15:30 (past 15:00)\n")


def test_friday_vs_other_days():
    """Compare Friday restriction vs other days"""
    events = [{"start": "09:00", "end": "10:00"}]
    
    result_thursday = suggest_slots(events, 60, "Thu")
    result_friday = suggest_slots(events, 60, "Fri")
    
    print("Friday vs Thursday Comparison:")
    print(f"Thursday (ends 17:00): {result_thursday}")
    print(f"Friday (ends 15:00): {result_friday}")
    print(f"Difference: {set(result_thursday) - set(result_friday)}\n")


def run_all_tests():
    """Run all test cases"""
    print("=" * 60)
    print("MEETING SCHEDULER TEST SUITE")
    print("=" * 60 + "\n")
    
    test_ac1_find_available_slots_between_meetings()
    test_ac2_empty_calendar_full_day()
    test_ac3_no_slots_when_fully_booked()
    test_ac4_meeting_duration_exceeds_gaps()
    test_ac5_handles_back_to_back_meetings()
    test_ac6_respects_end_of_business_day()
    test_friday_restriction()
    test_friday_vs_other_days()
    
    print("=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()