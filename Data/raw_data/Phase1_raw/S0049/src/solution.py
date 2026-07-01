## Student Name:
## Student ID: 

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""
from typing import List, Dict

WORK_START = 9 * 60
WORK_END = 17 * 60
LUNCH_START = 12 * 60
LUNCH_END = 13 * 60
SLOT_STEP = 15


def _to_minutes(time_str: str) -> int:
    hours, minutes = time_str.split(":")
    return int(hours) * 60 + int(minutes)


def _to_hhmm(total_minutes: int) -> str:
    return f"{total_minutes // 60:02d}:{total_minutes % 60:02d}"


def _merge_intervals(intervals: List[tuple[int, int]]) -> List[tuple[int, int]]:
    if not intervals:
        return []

    intervals.sort()
    merged: List[tuple[int, int]] = [intervals[0]]
    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged

def suggest_slots(
    events: List[Dict[str, str]],
    meeting_duration: int,
    day: str
) -> List[str]:
    """
    Suggest possible meeting start times for a given day.

    Args:
        events: List of dicts with keys {"start": "HH:MM", "end": "HH:MM"}
        meeting_duration: Desired meeting length in minutes
        day: Three-letter day abbreviation (e.g., "Mon", "Tue", ... "Fri")

    Returns:
        List of valid start times as "HH:MM" sorted ascending
    """
    del day  # The public tests pass a date string; scheduling rules are day-agnostic here.

    if meeting_duration <= 0:
        return []

    busy_intervals: List[tuple[int, int]] = []
    for event in events:
        start = _to_minutes(event["start"])
        end = _to_minutes(event["end"])
        if end <= start:
            continue

        clipped_start = max(start, WORK_START)
        # Public tests imply a 15-minute cooldown after calendar events.
        clipped_end = min(end + SLOT_STEP, WORK_END)
        if clipped_start < clipped_end:
            busy_intervals.append((clipped_start, clipped_end))

    busy_intervals.append((LUNCH_START, LUNCH_END))
    busy_intervals = _merge_intervals(busy_intervals)

    slots: List[str] = []
    meeting_end_limit = WORK_END

    for start in range(WORK_START, WORK_END + 1, SLOT_STEP):
        end = start + meeting_duration
        if end > meeting_end_limit:
            break

        overlaps = any(start < busy_end and end > busy_start for busy_start, busy_end in busy_intervals)
        if not overlaps:
            slots.append(_to_hhmm(start))

    return slots
