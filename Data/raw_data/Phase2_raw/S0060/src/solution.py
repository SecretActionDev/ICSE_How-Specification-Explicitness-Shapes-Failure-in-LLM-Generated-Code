from typing import List, Dict
import datetime
import re

def time_to_minutes(t: str) -> int:
    if not re.match(r"^\d{2}:\d{2}$", t):
        raise ValueError("Invalid time format")
    h, m = map(int, t.split(":"))
    if not (0 <= h <= 23 and 0 <= m <= 59):
        raise ValueError("Invalid time value")
    return h * 60 + m

def minutes_to_time(m: int) -> str:
    return f"{m//60:02d}:{m%60:02d}"

def validate_date(day: str):
    try:
        return datetime.datetime.strptime(day, "%Y-%m-%d")
    except:
        raise ValueError("Invalid date")

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    # -------- VALIDATION --------
    if not isinstance(events, list):
        raise ValueError("Events must be a list")
    if not isinstance(meeting_duration, int):
        raise ValueError("Meeting duration must be int")
    if meeting_duration <= 0:
        raise ValueError("Meeting duration must be positive")
    if meeting_duration % 30 != 0:
        raise ValueError("Meeting duration must be a multiple of 30 minutes")

    date_obj = validate_date(day)
    is_friday = date_obj.weekday() == 4  # Monday=0 ... Friday=4

    # -------- CONSTANTS --------
    WORK_START = 9 * 60        # 09:00
    WORK_END = 17 * 60         # 17:00
    LUNCH_START = 12 * 60      # 12:00
    LUNCH_END = 13 * 60        # 13:00
    STEP = 15                  # 15-minute increments
    BUFFER = 15                # 15-minute buffer after events
    FRIDAY_LAST_START = 15 * 60  # meetings cannot start after 15:00 on Fridays

    # -------- PROCESS EVENTS --------
    busy = []
    for e in events:
        s = time_to_minutes(e["start"])
        e_ = time_to_minutes(e["end"])
        if s >= e_:
            raise ValueError("Invalid event interval")
        # Clip events to working hours
        s = max(s, WORK_START)
        e_ = min(e_, WORK_END)
        busy.append((s, e_))

    # Merge overlapping events
    busy.sort()
    merged = []
    for s, e_ in busy:
        if not merged or s > merged[-1][1]:
            merged.append([s, e_])
        else:
            merged[-1][1] = max(merged[-1][1], e_)

    # -------- FIND SLOTS --------
    slots = []
    current = WORK_START
    while current + meeting_duration <= WORK_END:
        meeting_end = current + meeting_duration

        # Cannot overlap lunch
        if not (meeting_end <= LUNCH_START or current >= LUNCH_END):
            current += STEP
            continue

        # Friday cannot start after cutoff
        if is_friday and current >= FRIDAY_LAST_START:
            current += STEP
            continue

        # Check conflicts
        conflict = False
        for s, e_ in merged:
            if current < e_ + BUFFER and meeting_end > s:
                conflict = True
                break

        if not conflict:
            slots.append(minutes_to_time(current))

        current += STEP

    return slots