## Student Name: Daniel Di Giovanni
## Student ID: 218204818

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""

from __future__ import annotations
from typing import List, Tuple, TypedDict


class Event(TypedDict):
    start: str
    end: str



def _to_minutes(hhmm: str) -> int:
    h_str, m_str = hhmm.split(":")
    h = int(h_str)
    m = int(m_str)
    if not (0 <= h <= 23 and 0 <= m <= 59):
        raise ValueError(f"Invalid time: {hhmm}")
    return h * 60 + m


WORK_START = _to_minutes("09:00")
LUNCH_START = _to_minutes("12:00")
LUNCH_END = _to_minutes("13:00")
WORK_END = _to_minutes("17:00")


def _to_hhmm(minutes: int) -> str:
    h = minutes // 60
    m = minutes % 60
    return f"{h:02d}:{m:02d}"


def _add_busy_interval(busy: List[Tuple[int, int]], start_min: int, end_min: int) -> None:
    # Clamp to working hours and keep only overlaps.
    s = max(start_min, WORK_START)
    e = min(end_min, WORK_END)
    if e > s:
        busy.append((s, e))


def _ceil_to_grid(x: int, grid: int) -> int:
    return ((x + grid - 1) // grid) * grid


def suggest_slots(
    events: List[Event],
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

    if meeting_duration <= 0:
        raise ValueError("meeting_duration must be > 0")

    d = day.strip().lower()
    if d in {"sat", "saturday", "sun", "sunday"}:
        return []

    WORK_START = _to_minutes("09:00")
    WORK_END = _to_minutes("17:00")
    STEP = 15

    # Friday cutoff: no meeting may start at or after 15:00
    FRIDAY_CUTOFF = _to_minutes("15:00")
    is_friday = d in {"fri", "friday"}
    latest_start_cap = FRIDAY_CUTOFF if is_friday else WORK_END

    # Policy implied by your tests:
    # - 15-minute cooldown AFTER each event ends (but NOT after lunch).
    COOLDOWN_AFTER_EVENT = 15

    # Always block lunch (no cooldown added).
    lunch = {"start": "12:00", "end": "13:00"}

    busy: List[Tuple[int, int]] = []

    # Add user events with cooldown after end
    for e in events:
        s = _to_minutes(e["start"])
        t = _to_minutes(e["end"])
        if t <= s:
            raise ValueError(f"Event end must be after start: {e}")
        _add_busy_interval(busy, s, t + COOLDOWN_AFTER_EVENT)

    # Add lunch (no cooldown)
    _add_busy_interval(busy, _to_minutes(lunch["start"]), _to_minutes(lunch["end"]))

    # Merge busy intervals (events may be unsorted)
    busy.sort()
    merged: List[tuple[int, int]] = []
    for s, e in busy:
        if not merged or s > merged[-1][1]:
            merged.append((s, e))
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))

    # Compute free intervals within workday
    free: List[tuple[int, int]] = []
    cursor = WORK_START
    for s, e in merged:
        if s > cursor:
            free.append((cursor, s))
        cursor = max(cursor, e)
    if cursor < WORK_END:
        free.append((cursor, WORK_END))

    # Enumerate valid starts
    results: List[str] = []
    for fs, fe in free:
        start = _ceil_to_grid(fs, STEP)
        last_start = min(fe - meeting_duration, latest_start_cap - STEP)  # < 15:00 on Fridays
        while start <= last_start:
            # Extra guard (covers edge cases where start lands at cutoff)
            if is_friday and start >= FRIDAY_CUTOFF:
                break
            results.append(_to_hhmm(start))
            start += STEP

    return results
