from typing import List, Dict
from datetime import datetime, timedelta

WORK_START = 9 * 60
WORK_END = 17 * 60
LUNCH_START = 12 * 60
LUNCH_END = 13 * 60
BUFFER = 15
GRANULARITY = 15
MIN_DURATION = 15
FRIDAY_CUTOFF = 15 * 60  # 15:00 in minutes

def to_minutes(t: str) -> int:
    try:
        h, m = map(int, t.split(":"))
        if not (0 <= h < 24 and 0 <= m < 60):
            raise ValueError
        return h * 60 + m
    except:
        raise ValueError(f"Invalid time format: {t}")

def to_time_str(m: int) -> str:
    return f"{m // 60:02d}:{m % 60:02d}"

def merge_intervals(intervals):
    intervals.sort()
    merged = []

    for start, end in intervals:
        if not merged or merged[-1][1] < start:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    return merged

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    # Validate meeting duration
    if meeting_duration <= 0:
        raise ValueError("Meeting duration must be positive")
    if meeting_duration < MIN_DURATION:
        raise ValueError(f"Meeting duration must be at least {MIN_DURATION} minutes")

    # Validate date
    try:
        dt = datetime.strptime(day, "%Y-%m-%d")
        weekday = dt.weekday()  # Monday=0, Friday=4
    except:
        raise ValueError(f"Invalid date: {day}")

    # Step 1: convert events + apply buffer
    blocked = []

    for e in events:
        start = to_minutes(e["start"])
        end = to_minutes(e["end"])
        if start >= end:
            raise ValueError(f"Event start must be before end: {e}")
        blocked.append((start, end + BUFFER))

    # Step 2: add lunch break
    blocked.append((LUNCH_START, LUNCH_END))

    # Step 3: merge overlaps
    blocked = merge_intervals(blocked)

    # Step 4: find available gaps
    slots = []
    current = WORK_START

    # Determine max allowed end time
    max_end = WORK_END
    if weekday == 4:  # Friday
        max_end = min(WORK_END, FRIDAY_CUTOFF + meeting_duration)

    for start, end in blocked:
        if current < start:
            gap_start = current
            gap_end = min(start, max_end)

            # generate slots every 15 min
            t = gap_start
            while t + meeting_duration <= gap_end:
                if t >= WORK_START:
                    slots.append(to_time_str(t))
                t += GRANULARITY

        current = max(current, end)

    # last gap after final event
    if current < max_end:
        t = current
        while t + meeting_duration <= max_end:
            slots.append(to_time_str(t))
            t += GRANULARITY

    return sorted(slots)