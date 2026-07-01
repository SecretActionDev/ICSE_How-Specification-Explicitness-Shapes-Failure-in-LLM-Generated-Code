from typing import List, Dict
from datetime import datetime, timedelta

def time_to_minutes(t: str) -> int:
    try:
        h, m = map(int, t.split(":"))
        if not (0 <= h < 24 and 0 <= m < 60):
            raise ValueError
        return h * 60 + m
    except Exception:
        raise ValueError(f"Invalid time format: {t}")

def minutes_to_time(m: int) -> str:
    h = m // 60
    m = m % 60
    return f"{h:02d}:{m:02d}"

def validate_date(day: str):
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
    
    WORK_START = 9*60
    WORK_END = 17*60
    LUNCH_START = 12*60
    LUNCH_END = 13*60
    BUFFER = 15
    
    # ----------------------------
    # Convert events
    # ----------------------------
    busy = []
    for e in events:
        if "start" not in e or "end" not in e:
            raise ValueError("Event must have 'start' and 'end'")
        s = time_to_minutes(e["start"])
        t = time_to_minutes(e["end"])
        if s >= t:
            raise ValueError(f"Invalid event interval: {e}")
        # Clip to work hours
        start = max(s, WORK_START)
        end = min(t, WORK_END)
        if start < end:
            busy.append((start, end))
    
    # Add lunch break
    busy.append((LUNCH_START, LUNCH_END))
    
    # Sort and merge
    busy.sort()
    merged = []
    for s, e in busy:
        if not merged or merged[-1][1] < s:
            merged.append([s, e])
        else:
            merged[-1][1] = max(merged[-1][1], e)
    
    # ----------------------------
    # Generate possible slots
    # ----------------------------
    slots = []
    t = WORK_START
    # Check Friday cutoff for last possible start
    day_of_week = datetime.strptime(day, "%Y-%m-%d").weekday()  # Monday=0
    max_start_time = WORK_END - meeting_duration
    if day_of_week == 4:  # Friday
        max_start_time = min(max_start_time, 15*60)  # latest start 15:00
    
    while t <= max_start_time:
        # Round to nearest 15-min increment
        if t % 15 != 0:
            t += 15 - (t % 15)
            continue
        # Check if slot overlaps any busy interval (with 15-min buffer before/after)
        slot_end = t + meeting_duration
        conflict = False
        for s, e in merged:
            if slot_end > s - BUFFER and t < e + BUFFER:
                conflict = True
                break
        if not conflict:
            slots.append(minutes_to_time(t))
        t += 15
    
    return slots