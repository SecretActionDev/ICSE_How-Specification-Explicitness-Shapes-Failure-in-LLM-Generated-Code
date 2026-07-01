from typing import List, Dict
from datetime import datetime

def time_to_minutes(t: str) -> int:
    """Convert HH:MM string to minutes since midnight."""
    try:
        h, m = map(int, t.split(":"))
        if not (0 <= h < 24 and 0 <= m < 60):
            raise ValueError
        return h * 60 + m
    except Exception:
        raise ValueError(f"Invalid time format: {t}")

def minutes_to_time(m: int) -> str:
    """Convert minutes since midnight to HH:MM string."""
    h = m // 60
    m = m % 60
    return f"{h:02d}:{m:02d}"

def validate_date(day: str):
    """Ensure the day string is a valid date."""
    try:
        datetime.strptime(day, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date: {day}")

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    # ----------------------------
    # Validation
    # ----------------------------
    validate_date(day)
    if meeting_duration <= 0:
        raise ValueError("Meeting duration must be positive")
    if meeting_duration % 30 != 0 or meeting_duration < 30:
        raise ValueError("Meeting duration must be a multiple of 30 minutes")
    
    # ----------------------------
    # Constants
    # ----------------------------
    WORK_START = 9 * 60
    WORK_END = 17 * 60
    LUNCH_START = 12 * 60
    LUNCH_END = 13 * 60
    BUFFER = 15
    FRIDAY_LAST_START = 15 * 60  # Latest start on Friday
    
    day_of_week = datetime.strptime(day, "%Y-%m-%d").weekday()  # Monday=0
    
    # ----------------------------
    # Convert events to busy intervals
    # ----------------------------
    busy = []
    for e in events:
        if "start" not in e or "end" not in e:
            raise ValueError("Event must have 'start' and 'end'")
        s = time_to_minutes(e["start"])
        t = time_to_minutes(e["end"])
        if s >= t:
            raise ValueError(f"Invalid event interval: {e}")
        # Clip to working hours
        start = max(s, WORK_START)
        end = min(t, WORK_END)
        if start < end:
            busy.append((start, end))
    
    # Add lunch break
    busy.append((LUNCH_START, LUNCH_END))
    
    # Sort and merge overlapping intervals
    busy.sort()
    merged = []
    for s, e in busy:
        if not merged or merged[-1][1] < s:
            merged.append([s, e])
        else:
            merged[-1][1] = max(merged[-1][1], e)
    
    # ----------------------------
    # Generate candidate slots
    # ----------------------------
    slots = []
    t = WORK_START
    max_start_time = WORK_END - meeting_duration
    if day_of_week == 4:  # Friday
        max_start_time = min(max_start_time, FRIDAY_LAST_START)
    
    while t <= max_start_time:
        # Align to 15-minute increments
        if t % 15 != 0:
            t += 15 - (t % 15)
            continue
        
        slot_end = t + meeting_duration
        conflict = False
        
        for s, e in merged:
            # Check buffer before and after events
            if not (slot_end <= s - BUFFER or t >= e + BUFFER):
                conflict = True
                break
        
        if not conflict:
            slots.append(minutes_to_time(t))
        
        t += 15
    
    return slots