from typing import List, Dict
from datetime import datetime

WORK_START = "09:00"
WORK_END = "17:00"
LUNCH_START = "12:00"
LUNCH_END = "13:00"
SLOT_GRANULARITY = 15  # minutes
BUFFER_AFTER_EVENT = 15  # minutes
FRIDAY_END = "15:00"  # latest meeting start on Friday

def time_to_minutes(t: str) -> int:
    try:
        h, m = map(int, t.split(":"))
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError
        return h * 60 + m
    except Exception:
        raise ValueError(f"Invalid time format: {t}")

def minutes_to_time(m: int) -> str:
    return f"{m // 60:02d}:{m % 60:02d}"

def validate_event(event: Dict[str, str]):
    if "start" not in event or "end" not in event:
        raise ValueError("Event must have start and end times")
    start = time_to_minutes(event["start"])
    end = time_to_minutes(event["end"])
    if start >= end:
        raise ValueError(f"Event start {event['start']} must be before end {event['end']}")

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    # Validate meeting duration
    if meeting_duration <= 0:
        raise ValueError("Meeting duration must be positive")
    if meeting_duration % 30 != 0:
        raise ValueError("Meeting duration must be a multiple of 30 minutes")
    
    # Validate date
    try:
        dt = datetime.strptime(day, "%Y-%m-%d")
    except Exception:
        raise ValueError(f"Invalid date: {day}")
    
    work_start = time_to_minutes(WORK_START)
    work_end = time_to_minutes(WORK_END)
    lunch_start = time_to_minutes(LUNCH_START)
    lunch_end = time_to_minutes(LUNCH_END)
    
    # Friday cutoff
    max_end = work_end
    if dt.weekday() == 4:  # Friday
        max_end = min(max_end, time_to_minutes(FRIDAY_END))
    
    if meeting_duration > (max_end - work_start):
        return []
    
    # Normalize and merge events
    busy_times = []
    for e in events:
        validate_event(e)
        start = max(work_start, time_to_minutes(e["start"]))
        end = min(max_end, time_to_minutes(e["end"]))
        if start < end:
            busy_times.append((start, end))
    
    busy_times.sort()
    merged = []
    for s, e in busy_times:
        if not merged or s > merged[-1][1]:
            merged.append([s, e])
        else:
            merged[-1][1] = max(merged[-1][1], e)
    busy_times = merged
    
    # Add lunch
    busy_times.append([lunch_start, lunch_end])
    busy_times.sort()
    
    # Generate free slots
    slots = []
    prev_end = work_start
    for start, end in busy_times:
        slot_start = prev_end
        if prev_end != work_start:
            slot_start += BUFFER_AFTER_EVENT
        # Align to next 15-minute increment
        if slot_start % SLOT_GRANULARITY != 0:
            slot_start += SLOT_GRANULARITY - (slot_start % SLOT_GRANULARITY)
        while slot_start + meeting_duration <= start:
            if slot_start + meeting_duration <= max_end:
                slots.append(minutes_to_time(slot_start))
            slot_start += SLOT_GRANULARITY
        prev_end = max(prev_end, end + BUFFER_AFTER_EVENT)
    
    # Slots after last event
    slot_start = prev_end
    if slot_start % SLOT_GRANULARITY != 0:
        slot_start += SLOT_GRANULARITY - (slot_start % SLOT_GRANULARITY)
    while slot_start + meeting_duration <= max_end:
        slots.append(minutes_to_time(slot_start))
        slot_start += SLOT_GRANULARITY
    
    return sorted(slots)