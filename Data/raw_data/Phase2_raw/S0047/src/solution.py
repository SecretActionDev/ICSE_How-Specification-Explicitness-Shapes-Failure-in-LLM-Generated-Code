from typing import List, Dict
import datetime

WORK_START = 9 * 60     # 09:00
WORK_END = 17 * 60      # 17:00
SLOT_INTERVAL = 15      # 15-minute increments
LUNCH_START = 12 * 60   # 12:00
LUNCH_END = 13 * 60     # 13:00
FRIDAY_LAST_SLOT = 15 * 60  # 15:00

def time_to_minutes(t: str) -> int:
    try:
        h, m = map(int, t.split(":"))
        return h * 60 + m
    except:
        raise ValueError(f"Invalid time format: {t}")

def minutes_to_time(m: int) -> str:
    h = m // 60
    m = m % 60
    return f"{h:02d}:{m:02d}"

def get_weekday_from_date(date_str: str) -> str:
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%a")  # 'Mon', 'Tue', etc.
    except:
        raise ValueError(f"Invalid date: {date_str}")

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    # Validate meeting_duration
    if not isinstance(meeting_duration, int) or meeting_duration <= 0 or meeting_duration >= 24*60:
        raise ValueError("Invalid meeting duration")
    if meeting_duration < SLOT_INTERVAL:
        raise ValueError("Meeting duration too short; minimum is 15 minutes")

    # Determine weekday
    if len(day) == 3:  # Already a 3-letter weekday
        weekday = day
    else:  # Assume YYYY-MM-DD
        weekday = get_weekday_from_date(day)

    if weekday in ["Sat", "Sun"]:
        return []

    # Convert events to minutes and clip to work hours
    busy = []
    for e in events:
        if not isinstance(e, dict):
            raise ValueError("Event must be a dict with start and end")
        start = time_to_minutes(e.get("start", ""))
        end = time_to_minutes(e.get("end", ""))
        if start >= end:
            raise ValueError(f"Invalid event interval: {e}")
        # Clip to work hours
        start = max(start, WORK_START)
        end = min(end, WORK_END)
        if start < end:
            busy.append((start, end))

    # Add lunch break as busy slot
    busy.append((LUNCH_START, LUNCH_END))

    # Sort and merge overlapping intervals
    busy.sort()
    merged = []
    for start, end in busy:
        if not merged:
            merged.append([start, end])
        else:
            last_start, last_end = merged[-1]
            if start <= last_end:
                merged[-1][1] = max(last_end, end)
            else:
                merged.append([start, end])

    # Find free intervals
    free = []
    prev_end = WORK_START
    for start, end in merged:
        if start - prev_end >= meeting_duration:
            free.append((prev_end, start))
        prev_end = end
    if WORK_END - prev_end >= meeting_duration:
        free.append((prev_end, WORK_END))

    # Generate slots at 15-minute increments
    slots = []
    for start, end in free:
        t = ((start + SLOT_INTERVAL - 1) // SLOT_INTERVAL) * SLOT_INTERVAL  # round up to next slot
        while t + meeting_duration <= end:
            # Friday rule: exclude slots starting after FRIDAY_LAST_SLOT
            if weekday == "Fri" and t > FRIDAY_LAST_SLOT:
                break
            slots.append(minutes_to_time(t))
            t += SLOT_INTERVAL

    return sorted(slots)