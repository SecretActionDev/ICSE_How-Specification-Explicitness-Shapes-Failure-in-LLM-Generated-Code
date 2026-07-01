from typing import List, Dict
from datetime import datetime, timedelta

# Define working hours and lunch
WORK_START = "09:00"
WORK_END = "17:00"
LUNCH_START = "12:00"
LUNCH_END = "13:00"
SLOT_INTERVAL = 15  # minutes
FRIDAY_LAST_START = "15:00"

def time_to_minutes(t: str) -> int:
    try:
        hours, minutes = map(int, t.split(":"))
        if not (0 <= hours < 24) or not (0 <= minutes < 60):
            raise ValueError
        return hours * 60 + minutes
    except Exception:
        raise ValueError(f"Invalid time format: {t}")

def minutes_to_time(m: int) -> str:
    hours = m // 60
    minutes = m % 60
    return f"{hours:02d}:{minutes:02d}"

def prepare_events(events: List[Dict[str, str]]) -> List[tuple]:
    event_list = []
    for e in events:
        start = time_to_minutes(e['start'])
        end = time_to_minutes(e['end'])
        if start >= end:
            raise ValueError(f"Event start {e['start']} must be before end {e['end']}")
        event_list.append((start, end))
    return sorted(event_list)

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    if meeting_duration < SLOT_INTERVAL:
        raise ValueError("Meeting duration too short or negative")
    
    try:
        dt_day = datetime.strptime(day, "%Y-%m-%d")
    except Exception:
        raise ValueError(f"Invalid date: {day}")

    # Convert working hours
    WORK_START_MIN = time_to_minutes(WORK_START)
    WORK_END_MIN = time_to_minutes(WORK_END)
    LUNCH_START_MIN = time_to_minutes(LUNCH_START)
    LUNCH_END_MIN = time_to_minutes(LUNCH_END)
    FRIDAY_LAST_START_MIN = time_to_minutes(FRIDAY_LAST_START)

    # Add lunch as blocked event
    events = events + [{"start": LUNCH_START, "end": LUNCH_END}]

    event_times = prepare_events(events)

    # Merge overlapping events
    merged_events = []
    for start, end in event_times:
        if not merged_events:
            merged_events.append([start, end])
        else:
            last_start, last_end = merged_events[-1]
            if start <= last_end:
                merged_events[-1][1] = max(last_end, end)
            else:
                merged_events.append([start, end])

    # Compute free slots
    free_slots = []
    current = WORK_START_MIN
    for start, end in merged_events:
        start = max(start, WORK_START_MIN)
        end = min(end, WORK_END_MIN)
        if start - current >= meeting_duration:
            free_slots.append((current, start))
        current = max(current, end)
    if WORK_END_MIN - current >= meeting_duration:
        free_slots.append((current, WORK_END_MIN))

    # Generate valid start times
    valid_slots = []
    for start, end in free_slots:
        slot_start = ((start + SLOT_INTERVAL - 1) // SLOT_INTERVAL) * SLOT_INTERVAL
        while slot_start + meeting_duration <= end:
            # Friday cutoff rule
            if dt_day.weekday() == 4 and slot_start > FRIDAY_LAST_START_MIN:
                break
            valid_slots.append(minutes_to_time(slot_start))
            slot_start += SLOT_INTERVAL

    return valid_slots