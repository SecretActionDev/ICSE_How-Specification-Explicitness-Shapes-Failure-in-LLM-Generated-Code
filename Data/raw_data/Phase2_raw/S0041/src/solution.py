from typing import List, Dict
from datetime import datetime

# ----------------------------
# Helpers
# ----------------------------

def to_minutes(t: str) -> int:
    try:
        h, m = map(int, t.split(":"))
        if not (0 <= h < 24) or not (0 <= m < 60):
            raise ValueError
        return h * 60 + m
    except Exception:
        raise ValueError(f"Invalid time format: {t}")

def to_time_str(m: int) -> str:
    return f"{m // 60:02d}:{m % 60:02d}"

def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    if not intervals:
        return []
    intervals.sort()
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        last_end = merged[-1][1]
        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])
    return merged

def validate_day(day: str):
    try:
        datetime.strptime(day, "%Y-%m-%d")
    except Exception:
        raise ValueError(f"Invalid date: {day}")

# ----------------------------
# Main function
# ----------------------------

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    # Input validation
    if meeting_duration <= 0:
        raise ValueError("Meeting duration must be positive.")
    if meeting_duration < 15:
        raise ValueError("Meeting duration must be at least 15 minutes.")
    validate_day(day)
    
    WORK_START = to_minutes("09:00")
    WORK_END = to_minutes("17:00")
    
    # Convert events to minutes and validate
    intervals = []
    for e in events:
        start = to_minutes(e["start"])
        end = to_minutes(e["end"])
        if start >= end:
            raise ValueError(f"Event start time {e['start']} >= end time {e['end']}")
        # Clip events partially outside working hours
        start = max(start, WORK_START)
        end = min(end, WORK_END)
        if start < end:
            intervals.append([start, end])
    
    # Add lunch break
    intervals.append([to_minutes("12:00"), to_minutes("13:00")])
    
    # Merge overlapping intervals
    blocked = merge_intervals(intervals)
    
    # Generate slots in 15-min increments
    valid_slots = []
    current = WORK_START
    while current + meeting_duration <= WORK_END:
        meeting_end = current + meeting_duration
        conflict = any(not (meeting_end <= start or current >= end) for start, end in blocked)
        if not conflict:
            valid_slots.append(to_time_str(current))
        current += 15
    
    return valid_slots