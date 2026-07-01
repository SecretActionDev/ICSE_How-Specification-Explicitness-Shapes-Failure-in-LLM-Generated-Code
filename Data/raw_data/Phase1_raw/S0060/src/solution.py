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
        raise ValueError("Invalid duration")

    if meeting_duration % 30 != 0:
        raise ValueError("Meeting duration must be a multiple of 30 minutes")

    if meeting_duration < 30:
        raise ValueError("Too short")

    date_obj = validate_date(day)
    is_friday = date_obj.weekday() == 4

    # -------- CONSTANTS --------
    WORK_START = 9 * 60
    WORK_END = 17 * 60
    LUNCH_START = 12 * 60
    LUNCH_END = 13 * 60
    BUFFER = 15
    STEP = 15
    FRIDAY_LAST_START = 14 * 60

    # -------- PROCESS EVENTS --------
    busy = []
    for e in events:
        s = time_to_minutes(e["start"])
        e_ = time_to_minutes(e["end"])

        if s >= e_:
            raise ValueError("Invalid event interval")

        busy.append((s, e_))

    # merge overlaps
    busy.sort()
    merged = []
    for s, e_ in busy:
        if not merged or s > merged[-1][1]:
            merged.append([s, e_])
        else:
            merged[-1][1] = max(merged[-1][1], e_)

    # -------- SLOT CHECK --------
    slots = []

    for current in range(WORK_START, WORK_END, STEP):

        meeting_end = current + meeting_duration

        # Must fit in work hours
        if meeting_end > WORK_END:
            continue

        # ❗ KEY FIX: must end before lunch OR start after 13:15
        if not (meeting_end <= LUNCH_START or current >= LUNCH_END + BUFFER):
            continue

        # Block exactly 13:00
        if current == LUNCH_END:
            continue

        # Friday cutoff
        if is_friday and current > FRIDAY_LAST_START:
            continue

        conflict = False

        for s, e_ in merged:
            buffered_end = e_ + BUFFER

            if current < buffered_end and meeting_end > s:
                conflict = True
                break

        if not conflict:
            slots.append(minutes_to_time(current))

    return slots