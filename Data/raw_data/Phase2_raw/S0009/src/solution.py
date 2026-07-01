from typing import List, Dict
from datetime import datetime

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
        day: Date string in format "YYYY-MM-DD"

    Returns:
        List of valid start times as "HH:MM" sorted ascending
    """

    # Convert date string to datetime object
    try:
        date_obj = datetime.strptime(day, "%Y-%m-%d")
    except ValueError:
        return []  # invalid date format

    WORK_START = 9 * 60  # 9:00
    WORK_END = 17 * 60   # 17:00
    LUNCH_START = 12 * 60  # 12:00
    LUNCH_END = 13 * 60    # 13:00
    FRIDAY_LAST_START = 15 * 60  # 15:00, no meeting should start after this on Friday

    def to_minutes(t: str) -> int:
        h, m = map(int, t.split(":"))
        return h * 60 + m

    def to_time_str(minutes: int) -> str:
        return f"{minutes // 60:02d}:{minutes % 60:02d}"

    # Convert events to minute intervals (clipped to working hours)
    busy_intervals = []
    for event in events:
        start = max(to_minutes(event["start"]), WORK_START)
        end = min(to_minutes(event["end"]), WORK_END)
        if start < end:
            busy_intervals.append((start, end))

    # Sort busy intervals by start time
    busy_intervals.sort()

    # Determine the latest possible meeting start time
    latest_start = WORK_END - meeting_duration
    # Apply Friday-specific constraint
    if date_obj.weekday() == 4:  # 0=Monday, 4=Friday
        latest_start = min(latest_start, FRIDAY_LAST_START)

    available_starts = []

    # Try every 15-minute increment within allowed range
    for start in range(WORK_START, latest_start + 1, 15):
        # Skip lunch
        if LUNCH_START <= start < LUNCH_END:
            continue

        end = start + meeting_duration

        # Check for conflicts with busy intervals
        conflict = False
        for busy_start, busy_end in busy_intervals:
            if not (end <= busy_start or start >= busy_end):
                conflict = True
                break

        if not conflict:
            available_starts.append(to_time_str(start))

    return available_starts