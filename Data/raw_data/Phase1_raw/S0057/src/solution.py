from typing import List, Dict
from datetime import datetime


def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    # -----------------------------
    # Validation
    # -----------------------------
    try:
        date_obj = datetime.strptime(day, "%Y-%m-%d")
    except:
        raise ValueError("Invalid date format")

    if meeting_duration <= 0:
        raise ValueError("Meeting duration must be greater than 0")

    if meeting_duration % 30 != 0:
        raise ValueError("Meeting duration must be a multiple of 30 minutes")

    if meeting_duration == 1:
        raise ValueError("Meeting duration too small")

    # -----------------------------
    # Helpers
    # -----------------------------
    def to_minutes(t: str) -> int:
        try:
            h, m = map(int, t.split(":"))
            return h * 60 + m
        except:
            raise ValueError("Invalid time format")

    def to_str(m: int) -> str:
        return f"{m // 60:02d}:{m % 60:02d}"

    # -----------------------------
    # Constants
    # -----------------------------
    WORK_START = 9 * 60
    WORK_END = 17 * 60
    LUNCH_START = 12 * 60
    LUNCH_END = 13 * 60
    BUFFER = 15

    is_friday = date_obj.weekday() == 4

    # -----------------------------
    # Normalize events
    # -----------------------------
    intervals = []
    for e in events:
        start = to_minutes(e["start"])
        end = to_minutes(e["end"])

        if start >= end:
            raise ValueError("Invalid event interval")

        # Clip to working hours
        start = max(start, WORK_START)
        end = min(end, WORK_END)

        if start < end:
            intervals.append((start, end))

    # Add lunch as a blocked interval
    intervals.append((LUNCH_START, LUNCH_END))

    # -----------------------------
    # Merge intervals
    # -----------------------------
    intervals.sort()
    merged = []

    for s, e in intervals:
        if not merged or merged[-1][1] < s:
            merged.append([s, e])
        else:
            merged[-1][1] = max(merged[-1][1], e)

    # -----------------------------
    # Add buffer after events
    # -----------------------------
    buffered = []
    for s, e in merged:
        buffered.append((s, min(e + BUFFER, WORK_END)))

    # Merge again after buffering
    buffered.sort()
    merged = []
    for s, e in buffered:
        if not merged or merged[-1][1] < s:
            merged.append([s, e])
        else:
            merged[-1][1] = max(merged[-1][1], e)

    # -----------------------------
    # Find free gaps
    # -----------------------------
    free = []
    prev = WORK_START

    for s, e in merged:
        if prev < s:
            free.append((prev, s))
        prev = max(prev, e)

    if prev < WORK_END:
        free.append((prev, WORK_END))

    # -----------------------------
    # Generate slots (15-min steps)
    # -----------------------------
    result = []

    for start, end in free:
        current = start

        while current + meeting_duration <= end:
            # Friday rule
            if is_friday and current > 15 * 60:
                break

            # Must also finish within work hours
            if current + meeting_duration > WORK_END:
                break

            result.append(to_str(current))
            current += 15

    # -----------------------------
    # Final cleanup
    # -----------------------------
    result = sorted(set(result), key=lambda x: to_minutes(x))
    return result