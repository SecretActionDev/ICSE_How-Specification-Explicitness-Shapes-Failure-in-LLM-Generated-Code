from typing import List, Dict
from datetime import datetime

# -------------------------
# Helper functions
# -------------------------
def time_to_minutes(t: str) -> int:
    try:
        h, m = map(int, t.split(":"))
    except Exception:
        raise ValueError(f"Invalid time format: {t}")
    if not (0 <= h < 24 and 0 <= m < 60):
        raise ValueError(f"Invalid time value: {t}")
    return h * 60 + m

def minutes_to_time(m: int) -> str:
    h = m // 60
    m = m % 60
    return f"{h:02d}:{m:02d}"

def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    if not intervals:
        return []
    intervals.sort()
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(end, merged[-1][1])
        else:
            merged.append([start, end])
    return merged

def validate_date(day: str):
    try:
        datetime.strptime(day, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date: {day}")

# -------------------------
# Main function
# -------------------------
def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    # -------------------------
    # Input validation
    # -------------------------
    validate_date(day)
    if meeting_duration <= 0:
        raise ValueError("Meeting duration must be positive")
    if meeting_duration < 30:
        raise ValueError("Meeting duration must be at least 30 minutes")
    if meeting_duration % 30 != 0:
        raise ValueError("Meeting duration must be a multiple of 30 minutes")

    WORK_START, WORK_END = 9*60, 17*60
    LUNCH_START, LUNCH_END = 12*60, 13*60
    SLOT_INTERVAL = 15
    BUFFER_AFTER_EVENT = 15  # minutes

    # Determine weekday (Monday=0, Friday=4)
    weekday = datetime.strptime(day, "%Y-%m-%d").weekday()
    FRIDAY_CUTOFF = 15*60  # 15:00 in minutes

    # -------------------------
    # Parse events
    # -------------------------
    busy_intervals = []

    for e in events:
        if 'start' not in e or 'end' not in e:
            continue
        start = time_to_minutes(e['start'])
        end = time_to_minutes(e['end'])
        if start >= end:
            raise ValueError(f"Event start must be before end: {e}")
        # Clamp to working hours
        start = max(start, WORK_START)
        end = min(end, WORK_END)
        if start < end:
            busy_intervals.append([start, end + BUFFER_AFTER_EVENT])

    # Add lunch interval (no buffer)
    busy_intervals.append([LUNCH_START, LUNCH_END])

    # Merge overlapping intervals
    busy_intervals = merge_intervals(busy_intervals)

    # -------------------------
    # Generate valid slots
    # -------------------------
    valid_slots = []
    candidate_start = WORK_START

    while candidate_start + meeting_duration <= WORK_END:
        # Align to 15-min interval
        if candidate_start % SLOT_INTERVAL != 0:
            candidate_start += SLOT_INTERVAL - (candidate_start % SLOT_INTERVAL)
            continue

        candidate_end = candidate_start + meeting_duration

        # Friday rule: no meeting starts after cutoff
        if weekday == 4 and candidate_start > FRIDAY_CUTOFF:
            break
        if weekday == 4 and candidate_end > WORK_END:
            # Prevent meeting from exceeding working hours on Friday
            break

        # Check overlap with busy intervals
        overlap = False
        for b_start, b_end in busy_intervals:
            if candidate_start < b_end and candidate_end > b_start:
                overlap = True
                candidate_start = b_end
                break

        if not overlap:
            valid_slots.append(minutes_to_time(candidate_start))
            candidate_start += SLOT_INTERVAL

    return sorted(valid_slots)