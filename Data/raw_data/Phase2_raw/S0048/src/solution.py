from typing import List, Dict
from datetime import datetime

def time_to_minutes(t: str) -> int:
    try:
        h, m = map(int, t.split(":"))
        if not (0 <= h < 24 and 0 <= m < 60):
            raise ValueError
    except Exception:
        raise ValueError(f"Invalid time format: {t}")
    return h * 60 + m

def minutes_to_time(m: int) -> str:
    h = m // 60
    m = m % 60
    return f"{h:02d}:{m:02d}"

def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    if not intervals:
        return []
    intervals.sort()
    merged = [intervals[0]]
    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            last[1] = max(last[1], current[1])
        else:
            merged.append(current)
    return merged

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    # Validate duration
    if meeting_duration <= 0:
        raise ValueError("Meeting duration must be greater than 0")
    if meeting_duration % 15 != 0:
        raise ValueError("Meeting duration must align with 15-minute increments")

    # Validate date
    try:
        day_date = datetime.strptime(day, "%Y-%m-%d")
    except Exception:
        raise ValueError(f"Invalid date format: {day}")

    is_friday = day_date.weekday() == 4
    WORK_START = 9 * 60
    WORK_END = 17 * 60
    LUNCH_START = 12 * 60
    LUNCH_END = 13 * 60
    BUFFER = 15
    FRIDAY_LAST_START = 15 * 60

    busy_intervals = []

    for e in events:
        try:
            start = time_to_minutes(e['start'])
            end = time_to_minutes(e['end'])
        except KeyError:
            raise ValueError("Event must have 'start' and 'end'")
        if start >= end:
            raise ValueError(f"Event start {e['start']} >= end {e['end']}")
        # Apply buffer and clamp to working hours
        start = max(WORK_START, start - BUFFER)
        end = min(WORK_END, end + BUFFER)
        busy_intervals.append([start, end])

    # Add lunch break
    busy_intervals.append([LUNCH_START, LUNCH_END])

    # Merge overlapping intervals
    busy_intervals = merge_intervals(busy_intervals)

    # Compute free intervals
    free_intervals = []
    prev_end = WORK_START
    for start, end in busy_intervals:
        if start > prev_end:
            free_intervals.append([prev_end, start])
        prev_end = max(prev_end, end)
    if prev_end < WORK_END:
        free_intervals.append([prev_end, WORK_END])

    # Generate available start times
    available_slots = []
    for start, end in free_intervals:
        slot_start = ((start + 14) // 15) * 15  # next 15-min increment
        while slot_start + meeting_duration <= end:
            if not (is_friday and slot_start >= FRIDAY_LAST_START):
                available_slots.append(minutes_to_time(slot_start))
            slot_start += 15

    return available_slots