from typing import List, Dict
from datetime import datetime, timedelta

def time_to_minutes(t: str) -> int:
    """Convert 'HH:MM' string to minutes since midnight."""
    try:
        h, m = map(int, t.split(":"))
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError
    except Exception:
        raise ValueError(f"Invalid time format: {t}")
    return h * 60 + m

def minutes_to_time(m: int) -> str:
    """Convert minutes since midnight to 'HH:MM' string."""
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}"

def validate_date(day: str):
    """Validate date string 'YYYY-MM-DD'."""
    try:
        dt = datetime.strptime(day, "%Y-%m-%d")
        return dt
    except ValueError:
        raise ValueError(f"Invalid date: {day}")

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    # -----------------------------
    # 1. Input validation
    # -----------------------------
    dt = validate_date(day)

    if meeting_duration <= 0:
        raise ValueError("Meeting duration must be positive")
    if meeting_duration % 30 != 0:
        raise ValueError("Meeting duration must be a multiple of 30 minutes")
    if meeting_duration < 30:
        raise ValueError("Meeting duration must be at least 30 minutes")

    WORK_START = 9*60
    WORK_END = 17*60
    LUNCH_START = 12*60
    LUNCH_END = 13*60
    SLOT_GRANULARITY = 15
    BUFFER_AFTER_EVENT = 15

    # Friday-specific cutoff
    FRIDAY_CUTOFF = 15*60  # 15:00 in minutes

    # No meetings on weekends
    if dt.weekday() >= 5:  # Saturday=5, Sunday=6
        return []

    # -----------------------------
    # 2. Normalize events
    # -----------------------------
    normalized_events = []
    for ev in events:
        if "start" not in ev or "end" not in ev:
            raise ValueError("Event must have start and end")
        start = max(time_to_minutes(ev["start"]), WORK_START)
        end = min(time_to_minutes(ev["end"]), WORK_END)
        if start >= end:
            raise ValueError(f"Invalid event interval: {ev}")
        normalized_events.append({"start": start, "end": end})

    # Sort by start time
    normalized_events.sort(key=lambda x: x["start"])

    # -----------------------------
    # 3. Generate potential slots
    # -----------------------------
    slots = []
    current = WORK_START
    while current + meeting_duration <= WORK_END:
        # Skip lunch
        if LUNCH_START <= current < LUNCH_END:
            current = LUNCH_END
            continue

        # Ensure 15-min increments
        if current % SLOT_GRANULARITY != 0:
            current += SLOT_GRANULARITY - (current % SLOT_GRANULARITY)
            continue

        # Friday cutoff enforcement
        if dt.weekday() == 4:  # Friday
            if current > FRIDAY_CUTOFF:
                break
            # Ensure meeting fits before cutoff
            if current + meeting_duration > FRIDAY_CUTOFF:
                current += SLOT_GRANULARITY
                continue

        # Check conflicts with events + buffer
        conflict = False
        for ev in normalized_events:
            ev_start = ev["start"]
            ev_end = ev["end"] + BUFFER_AFTER_EVENT
            if current < ev_end and current + meeting_duration > ev_start:
                conflict = True
                break

        if not conflict:
            slots.append(minutes_to_time(current))

        current += SLOT_GRANULARITY

    # -----------------------------
    # 4. Return sorted, unique slots
    # -----------------------------
    slots = sorted(list(set(slots)))
    return slots