from typing import List, Dict
from datetime import datetime

def time_to_minutes(t: str) -> int:
    try:
        hours, minutes = map(int, t.split(":"))
        if not (0 <= hours < 24 and 0 <= minutes < 60):
            raise ValueError
        return hours * 60 + minutes
    except:
        raise ValueError(f"Invalid time format: {t}")

def minutes_to_time(m: int) -> str:
    return f"{m // 60:02d}:{m % 60:02d}"

def validate_events(events: List[Dict[str, str]]):
    for e in events:
        start = time_to_minutes(e["start"])
        end = time_to_minutes(e["end"])
        if start >= end:
            raise ValueError(f"Event start must be before end: {e}")

def validate_date(day: str):
    try:
        datetime.strptime(day, "%Y-%m-%d")
    except:
        raise ValueError(f"Invalid date: {day}")

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    if meeting_duration < 15:
        raise ValueError("Meeting duration too short")
    validate_date(day)
    validate_events(events)
    
    WORK_START = time_to_minutes("09:00")
    WORK_END = time_to_minutes("17:00")
    LUNCH_START = time_to_minutes("12:00")
    LUNCH_END = time_to_minutes("13:00")
    SLOT_GRANULARITY = 15
    
    # Convert events to intervals in minutes
    blocked_intervals = [(time_to_minutes(e["start"]), time_to_minutes(e["end"])) for e in events]
    blocked_intervals.append((LUNCH_START, LUNCH_END))
    
    # Merge overlapping intervals for robustness
    blocked_intervals.sort()
    merged = []
    for start, end in blocked_intervals:
        if not merged:
            merged.append([start, end])
        else:
            last_start, last_end = merged[-1]
            if start <= last_end:
                merged[-1][1] = max(last_end, end)
            else:
                merged.append([start, end])
    
    blocked_intervals = merged
    
    # Generate candidate start times
    valid_slots = []
    current_time = WORK_START
    while current_time + meeting_duration <= WORK_END:
        # Skip if overlaps with any blocked interval
        overlap = False
        for start, end in blocked_intervals:
            if not (current_time + meeting_duration <= start or current_time >= end):
                overlap = True
                break
        if not overlap:
            valid_slots.append(minutes_to_time(current_time))
        current_time += SLOT_GRANULARITY
    
    return sorted(valid_slots)