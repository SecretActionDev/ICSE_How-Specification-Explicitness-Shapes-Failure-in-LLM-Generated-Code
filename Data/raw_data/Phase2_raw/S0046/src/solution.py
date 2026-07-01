from typing import List, Dict
from datetime import datetime

def time_to_minutes(time_str: str) -> int:
    try:
        h, m = map(int, time_str.split(":"))
        if not (0 <= h < 24 and 0 <= m < 60):
            raise ValueError
        return h * 60 + m
    except Exception:
        raise ValueError(f"Invalid time format: {time_str}")

def minutes_to_time(minutes: int) -> str:
    h = minutes // 60
    m = minutes % 60
    return f"{h:02d}:{m:02d}"

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    # Validate meeting duration
    if meeting_duration < 15:
        raise ValueError("Meeting duration must be at least 15 minutes.")

    # Validate date
    try:
        date_obj = datetime.strptime(day, "%Y-%m-%d")
    except Exception:
        raise ValueError(f"Invalid date: {day}")
    
    # Determine weekday and working hours
    weekday = date_obj.weekday()  # Monday=0 ... Sunday=6
    WORK_START = 9 * 60
    WORK_END = 17 * 60
    FRIDAY_LAST_START = 15 * 60  # 15:00 cutoff for Friday
    GRANULARITY = 15

    if weekday == 4:  # Friday
        max_start = FRIDAY_LAST_START
    else:
        max_start = WORK_END

    # Convert events to minutes
    busy_times = []
    for event in events:
        start = time_to_minutes(event["start"])
        end = time_to_minutes(event["end"])
        if start >= end:
            raise ValueError(f"Event start time must be before end time: {event}")
        # Clip events to working hours
        start = max(start, WORK_START)
        end = min(end, WORK_END)
        if start < end:
            busy_times.append((start, end))
    busy_times.sort()

    # Merge overlapping events
    merged = []
    for start, end in busy_times:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    # Generate available slots
    available_slots = []
    current_time = WORK_START

    for start, end in merged:
        while current_time + meeting_duration <= start:
            if current_time <= max_start:
                available_slots.append(minutes_to_time(current_time))
            current_time += GRANULARITY
        current_time = max(current_time, end)

    # After last event
    while current_time + meeting_duration <= WORK_END:
        if current_time <= max_start:
            available_slots.append(minutes_to_time(current_time))
        current_time += GRANULARITY

    return available_slots