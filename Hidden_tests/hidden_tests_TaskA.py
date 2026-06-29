import pytest
from typing import List, Dict
from solution import suggest_slots  # Replace with your actual module name

# -----------------------------
# Helper function
# -----------------------------
def slots_equal(actual: List[str], expected: List[str]):
    """Helper to compare lists of time slots."""
    assert sorted(actual) == sorted(expected)

# -----------------------------
# 1. Basic functionality / empty calendar
# -----------------------------
## test CO
def test_TC1_empty_day():
    events = []
    meeting_duration = 30
    day = "2026-03-11"  # Wednesday
    result = suggest_slots(events, meeting_duration, day)

    # Hardcoded expected slots for a full empty day
    expected = [
        "09:00","09:15","09:30","09:45",
        "10:00","10:15","10:30","10:45",
        "11:00","11:15",
        "13:15","13:30","13:45","14:00","14:15","14:30","14:45",
        "15:00","15:15","15:30","15:45",
        "16:00","16:15","16:30"
    ]

    slots_equal(result, expected)

# # -----------------------------
# 2. Single event blocking mid-day
# -----------------------------
## test CO
def test_TC2_single_event_midday():
    events = [{"start":"12:00","end":"13:00"}]
    meeting_duration = 60
    day = "2026-03-11"
    result = suggest_slots(events, meeting_duration, day)

    # Hardcoded expected slots considering lunch + buffer
    expected = [
        "09:00","09:15","09:30","09:45",
        "10:00","10:15","10:30","10:45",
        "13:15","13:30","13:45","14:00","14:15","14:30","14:45",
        "15:00","15:15", "15:30","15:45",
        "16:00"
    ]
    slots_equal(result, expected)



# -----------------------------
# 3. Multiple non-overlapping events
# -----------------------------
## test CO
def test_TC3_multiple_nonoverlapping_events():
    events = [{"start":"10:00","end":"11:00"},{"start":"14:00","end":"15:00"}]
    meeting_duration = 30
    day = "2026-03-11"
    result = suggest_slots(events, meeting_duration, day)
    expected = [
        "09:00","09:15",
        "11:15", 
        "13:15",
        "15:15", "15:30","15:45",
        "16:00", "16:15","16:30"
    ]
    slots_equal(result, expected)

# -----------------------------
# 4. Overlapping events
# -----------------------------
## test CO
def test_TC4_overlapping_events():
    events = [{"start":"10:00","end":"11:00"},{"start":"10:30","end":"11:30"}]
    meeting_duration = 30
    day = "2026-03-11"
    result = suggest_slots(events, meeting_duration, day)
    expected = [
        "09:00","09:15",
        "13:15","13:30","13:45","14:00","14:15","14:30","14:45",
        "15:00","15:15", "15:30","15:45",
        "16:00", "16:15","16:30"
    ]
    slots_equal(result, expected)

# -----------------------------
# 5. Adjacent events: test CO
# -----------------------------
def test_TC5_adjacent_events():
    events = [{"start":"10:00","end":"11:00"},{"start":"11:00","end":"12:00"}]
    meeting_duration = 30
    day = "2026-03-11"
    result = suggest_slots(events, meeting_duration, day)
    expected = [
        "09:00","09:15",
        "13:15","13:30","13:45","14:00","14:15","14:30","14:45",
        "15:00","15:15", "15:30","15:45",
        "16:00", "16:15","16:30"
    ]
    slots_equal(result, expected)

# -----------------------------
# 6. Meeting fits exactly at working hours start: test EG
# -----------------------------

def test_TC6_meeting_fits_morning():
    events = []
    meeting_duration = 150 # 2 hours 30 minutes, fits exactly from 09:00 to 11:45
    day = "2026-03-11"
    result = suggest_slots(events, meeting_duration, day)
    expected = [
        "09:00", "09:15",
        "13:15","13:30","13:45","14:00","14:15","14:30"
    ]
    slots_equal(result, expected)

# -----------------------------
# 7. Meeting longer than working hours: test EC
# -----------------------------
def test_TC7_meeting_exceeds_working_hours():
    events = []
    meeting_duration = 600
    day = "2026-03-11"
    result = suggest_slots(events, meeting_duration, day)
    assert result == []

# -----------------------------
# 8. Event partially outside working hours: test EC
# -----------------------------
def test_TC8_event_partial_outside_hours():
    events = [{"start":"08:00","end":"10:00"}]
    meeting_duration = 60
    day = "2026-03-11"
    result = suggest_slots(events, meeting_duration, day)
    expected = [
        "10:15","10:30","10:45",
        "13:15","13:30","13:45","14:00","14:15","14:30","14:45",
        "15:00","15:15", "15:30","15:45",
        "16:00"
    ]
    slots_equal(result, expected)

# -----------------------------
# 9. Friday with free slots after 15:00: test CO
# -----------------------------
def test_TC9_friday_cutoff():
    events = []
    meeting_duration = 30
    day = "2026-03-13"
    result = suggest_slots(events, meeting_duration, day)
    expected = [
        "09:00","09:15","09:30","09:45",
        "10:00","10:15","10:30","10:45","11:00","11:15",
        "13:15","13:30","13:45","14:00","14:15","14:30"
    ]
    slots_equal(result, expected)

# -----------------------------
# 10. Friday with event ending at 15:00
# -----------------------------
def test_TC10_friday_event_ends_at_cutoff():
    events = [{"start":"14:00","end":"15:00"}]
    meeting_duration = 30
    day = "2026-03-13"
    result = suggest_slots(events, meeting_duration, day)
    for slot in result:
        h,m = map(int, slot.split(":"))
        assert h*60+m <= 14*60  # cannot start after 14:30

# -----------------------------
# 11. Friday, meeting duration exceeds cutoff
# -----------------------------
def test_TC11_friday_long_meeting():
    events = []
    meeting_duration = 120
    day = "2026-03-13"
    result = suggest_slots(events, meeting_duration, day)
    for slot in result:
        h,m = map(int, slot.split(":"))
        assert h*60+m + 120 <= 17*60
        assert h*60+m <= 15*60

# -----------------------------
# 12. Granularity 15-min increments: AI
# -----------------------------
def test_TC12_granularity_15min():
    events = []
    meeting_duration = 30
    day = "2026-03-11"
    result = suggest_slots(events, meeting_duration, day)
    expected = [
        "09:00","09:15","09:30","09:45",
        "10:00","10:15","10:30","10:45", "11:00","11:15",
        "13:15","13:30","13:45","14:00","14:15","14:30","14:45",
        "15:00","15:15", "15:30","15:45",
        "16:00", "16:15","16:30"
    ]
    slots_equal(result, expected)

# -----------------------------
# 13. Very short duration (1-min increments): AI
# -----------------------------
def test_TC13_short_duration():
    events = []
    meeting_duration = 1
    day = "2026-03-11"

    with pytest.raises(ValueError):
        suggest_slots(events, meeting_duration, day)

# -----------------------------
# 14. Event occupies entire working hours
# -----------------------------
def test_TC14_event_full_day():
    events = [{"start":"09:00","end":"17:00"}]
    meeting_duration = 30
    day = "2026-03-11"
    result = suggest_slots(events, meeting_duration, day)
    assert result == []

# -----------------------------
# 15. Negative duration: IV
# -----------------------------
def test_TC15_negative_duration():
    with pytest.raises(ValueError):
        suggest_slots([], -30, "2026-03-11")

# -----------------------------
# 16. Invalid time format:CO
# -----------------------------
def test_TC16_invalid_time_format():
    with pytest.raises(ValueError):
        suggest_slots([{"start":"9AM","end":"10:00"}], 30, "2026-03-11")

# -----------------------------
# 17. Start >= end: IV
# -----------------------------
def test_TC17_invalid_event_interval():
    with pytest.raises(ValueError):
        suggest_slots([{"start":"10:00","end":"09:00"}], 30, "2026-03-11")

# -----------------------------
# 18. Invalid date: CO
# -----------------------------
def test_TC18_invalid_date():
    with pytest.raises(ValueError):
        suggest_slots([], 30, "2026-02-30")

# -----------------------------
# 19. Multiple free windows, deterministic ordering: TB
# -----------------------------
def test_TC19_multiple_windows_order():
    events = [{"start":"10:00","end":"11:00"},{"start":"14:00","end":"15:00"}]
    meeting_duration = 30
    day = "2026-03-11"
    result = suggest_slots(events, meeting_duration, day)
    assert result == sorted(result)

# -----------------------------
# 20. Stress test: many events: iv
# -----------------------------
def test_TC20_many_events():
    events = [{"start":f"{h:02d}:00","end":f"{h:02d}:30"} for h in range(9,17)]
    meeting_duration = 30
    day = "2026-03-11"
    result = suggest_slots(events, meeting_duration, day)
    # All slots should be blocked, except any remaining free minutes
    assert result == [] or all(int(slot.split(":")[0]) < 9 or int(slot.split(":")[0]) >= 17 for slot in result)

# -----------------------------
# 21.  small gaps between events: IV
# -----------------------------
def test_TC21_small_gaps_between_events():
    events = [{"start":"09:00","end":"09:15"},{"start":"09:30","end":"09:45"}]
    meeting_duration = 30
    day = "2026-03-11"
    result = suggest_slots(events, meeting_duration, day)
    # Ensure free slots are correct
    expected = ["10:00","10:15","10:30","10:45","11:00","11:15",
                "13:15","13:30","13:45","14:00","14:15",
                "14:30","14:45","15:00","15:15","15:30","15:45","16:00","16:15","16:30"]
    slots_equal(result, expected)

# -----------------------------
# 22. Friday + overlapping event + duration: IV
# -----------------------------
def test_TC22_friday_overlap_long_meeting():
    events = [{"start":"14:00","end":"15:30"}]
    meeting_duration = 60
    day = "2026-03-13"  # Friday
    result = suggest_slots(events, meeting_duration, day)
    # Latest start must be before 14:00
    for slot in result:
        h,m = map(int, slot.split(":"))
        assert h*60+m <= 14*60

# -----------------------------
# 23. Edge case: empty events, duration fills last slot: EC
# -----------------------------
def test_TC23_empty_day_duration_fills_last_slot():
    events = []
    meeting_duration = 30
    day = "2026-03-11"
    result = suggest_slots(events, meeting_duration, day)
    # Last slot should be 16:30
    assert "16:30" in result

# -----------------------------
# 24. Event partially overlaps Friday cutoff: EC
# -----------------------------
def test_TC24_friday_event_partial_cutoff():
    events = [{"start":"14:30","end":"16:00"}]
    meeting_duration = 30
    day = "2026-03-13"  # Friday
    result = suggest_slots(events, meeting_duration, day)
    for slot in result:
        h,m = map(int, slot.split(":"))
        # Cannot start after 14:30
        assert h*60+m <= 14*60

# -----------------------------
# 25. Multiple consecutive overlapping events: CO
# -----------------------------
def test_TC25_multiple_consecutive_overlaps():
    events = [{"start":"10:00","end":"11:00"},
              {"start":"13:30","end":"14:30"},
              {"start":"16:00","end":"16:30"}]
    meeting_duration = 30
    day = "2026-03-11"
    result = suggest_slots(events, meeting_duration, day)
    expected = [
        "09:00","09:15",
        "11:15",
        "14:45",
        "15:00","15:15"
    ]
    assert result == expected

# -----------------------------
# 26. Lunch break blocks meetings: AI
# -----------------------------
def test_TC26_lunch_break_blocked():
    """
    Functional requirement:
    No meeting may start during lunch (12:00–13:00).
    """
    events = []
    meeting_duration = 30
    day = "2026-03-11"
    result = suggest_slots(events, meeting_duration, day)
    lunch_slots = ["12:00","12:15","12:30","12:45"]
    for slot in lunch_slots:
        assert slot not in result

# -----------------------------
# 27. Meeting may start exactly after lunch: AI
# -----------------------------
def test_TC27_start_after_lunch_allowed():
    """
    Functional requirement:
    Meetings may start at 13:00 (end of lunch).
    """
    events = []
    meeting_duration = 30
    day = "2026-03-11"
    result = suggest_slots(events, meeting_duration, day)
    assert "13:15" in result
    assert "12:45" not in result

# -----------------------------
# 28. 15-minute buffer after events: AI could be IV?
# -----------------------------
def test_TC28_buffer_after_event():
    events = [{"start":"09:00","end":"09:30"}]
    meeting_duration = 30
    day = "2026-03-11"
    result = suggest_slots(events, meeting_duration, day)
    # Earliest valid start is after 15-min buffer
    assert "09:45" in result
    assert "09:30" not in result
    assert "09:30" not in result

# -----------------------------
# 29. Zero-duration meeting: EC
# -----------------------------
def test_TC29_zero_duration_meeting():
    """
    Edge case:
    Zero-duration meetings are invalid; should raise error or return empty list.
    """
    events = []
    meeting_duration = 0
    day = "2026-03-11"
    try:
        result = suggest_slots(events, meeting_duration, day)
        assert result == []
    except ValueError:
        assert True

# -----------------------------
# 30. Meeting duration must be multiple of 30: there are multiple
# AI
# -----------------------------
@pytest.mark.parametrize("duration, valid", [
    (30, True),
    (60, True),
    (45, False),
    (20, False),
])
def test_TC30_meeting_duration_multiple_of_30(duration, valid):
    events = []
    day = "2026-03-11"
    if valid:
        result = suggest_slots(events, meeting_duration=duration, day=day)
        assert isinstance(result, list)
        assert all((int(slot.split(":")[1]) % 15 == 0) for slot in result)
    else:
        with pytest.raises(ValueError, match="Meeting duration must be a multiple of 30 minutes"):
            suggest_slots(events, meeting_duration=duration, day=day)
