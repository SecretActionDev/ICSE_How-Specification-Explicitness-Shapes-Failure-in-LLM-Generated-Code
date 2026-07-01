from typing import List, Dict
from datetime import datetime

WORK_START = 9 * 60
WORK_END = 17 * 60
LUNCH_START = 12 * 60
LUNCH_END = 13 * 60
INTERVAL = 15  # 15-minute increments
MIN_DURATION = 30  # minimum meeting duration
VALID_DURATION_MULTIPLE = 30  # durations must be multiples of 30
FRIDAY_CUTOFF = 15 * 60  # 15:00 in minutes


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


def is_friday(day: str) -> bool:
    dt = datetime.strptime(day, "%Y-%m-%d")
    return dt.weekday() == 4  # Monday=0, Friday=4


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
    # Convert events to busy intervals
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
    # Add lunch break
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
    # Generate slots aligned to 15-min intervals
    # -------------------------
    slots = []
    friday = is_friday(day)

    for start, end in free:
        t = start
        # Align start to next 15-min increment
        if t % INTERVAL != 0:
            t += INTERVAL - (t % INTERVAL)
        while t + meeting_duration <= end and t + meeting_duration <= WORK_END:
            # Apply Friday 15:00 cutoff
            if friday and t > FRIDAY_CUTOFF - meeting_duration:
                break
            slots.append(to_time_str(t))
            t += INTERVAL

    return sorted(slots)