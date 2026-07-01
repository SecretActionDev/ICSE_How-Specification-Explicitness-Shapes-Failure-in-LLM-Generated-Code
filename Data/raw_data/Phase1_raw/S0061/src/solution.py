from typing import List, Dict
from datetime import datetime

WORK_START = 9 * 60
WORK_END = 17 * 60
LUNCH_START = 12 * 60
LUNCH_END = 13 * 60
INTERVAL = 15  # 15-minute increments
MIN_DURATION = 30  # minimum meeting duration
VALID_DURATION_MULTIPLE = 30  # durations must be multiples of 30


def to_minutes(t: str) -> int:
    try:
        h, m = map(int, t.split(":"))
    except Exception:
        raise ValueError(f"Invalid time format: {t}")
    if not (0 <= h < 24 and 0 <= m < 60):
        raise ValueError(f"Invalid time value: {t}")
    return h * 60 + m


def to_time_str(m: int) -> str:
    h, mi = divmod(m, 60)
    return f"{h:02d}:{mi:02d}"


def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort()
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def validate_date(day: str):
    try:
        datetime.strptime(day, "%Y-%m-%d")
    except Exception:
        raise ValueError(f"Invalid date: {day}")


def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    # -------------------------
    # Validation
    # -------------------------
    validate_date(day)

    if meeting_duration <= 0:
        raise ValueError("Meeting duration must be positive")
    if meeting_duration % VALID_DURATION_MULTIPLE != 0:
        raise ValueError(f"Meeting duration must be a multiple of {VALID_DURATION_MULTIPLE} minutes")
    if meeting_duration < MIN_DURATION:
        raise ValueError(f"Meeting duration must be at least {MIN_DURATION} minutes")

    # -------------------------
    # Convert events
    # -------------------------
    busy = []

    for e in events:
        start = to_minutes(e["start"])
        end = to_minutes(e["end"])
        if start >= end:
            raise ValueError(f"Event start >= end: {e}")
        # Clip to working hours
        start = max(start, WORK_START)
        end = min(end, WORK_END)
        if start < end:
            # enforce 15-min buffer after each event
            busy.append((start, end + INTERVAL))
    # Add lunch
    busy.append((LUNCH_START, LUNCH_END))

    busy = merge_intervals(busy)

    # -------------------------
    # Find free intervals
    # -------------------------
    free = []
    prev_end = WORK_START

    for start, end in busy:
        if prev_end + INTERVAL <= start:
            free.append((prev_end, start))
        prev_end = end

    if prev_end + INTERVAL <= WORK_END:
        free.append((prev_end, WORK_END))

    # -------------------------
    # Generate slots aligned to 15-min
    # -------------------------
    slots = []
    for start, end in free:
        t = start
        if t % INTERVAL != 0:
            t += INTERVAL - (t % INTERVAL)
        while t + meeting_duration <= end and t + meeting_duration <= WORK_END:
            slots.append(to_time_str(t))
            t += INTERVAL

    return slots