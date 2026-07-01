from typing import List, Dict
from datetime import datetime, timedelta

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    # Validate meeting duration
    if meeting_duration <= 0:
        raise ValueError("Meeting duration must be positive")
    if meeting_duration % 30 != 0:
        raise ValueError("Meeting duration must be a multiple of 30 minutes")

    # Business hours
    BUSINESS_START = "09:00"
    BUSINESS_END = "17:00"
    LUNCH_START = "12:00"
    LUNCH_END = "13:00"
    FRIDAY_LAST_START = "15:00"
    BUFFER_MINUTES = 15
    SLOT_INCREMENT = 15

    # Helper to convert time string to minutes
    def time_to_minutes(t: str) -> int:
        try:
            h, m = map(int, t.split(":"))
        except Exception:
            raise ValueError(f"Invalid time format: {t}")
        if not (0 <= h < 24 and 0 <= m < 60):
            raise ValueError(f"Invalid time value: {t}")
        return h * 60 + m

    # Helper to convert minutes to time string
    def minutes_to_time(m: int) -> str:
        return f"{m // 60:02d}:{m % 60:02d}"

    # Convert business hours
    day_start = time_to_minutes(BUSINESS_START)
    day_end = time_to_minutes(BUSINESS_END)
    lunch_start = time_to_minutes(LUNCH_START)
    lunch_end = time_to_minutes(LUNCH_END)
    friday_last_start = time_to_minutes(FRIDAY_LAST_START)

    # Validate and normalize events
    normalized_events = []
    for e in events:
        try:
            start = time_to_minutes(e['start'])
            end = time_to_minutes(e['end'])
        except KeyError:
            raise ValueError("Event must have 'start' and 'end'")
        if start >= end:
            raise ValueError(f"Event start >= end: {e}")
        normalized_events.append({'start': start, 'end': end})

    # Sort events by start time
    sorted_events = sorted(normalized_events, key=lambda x: x['start'])

    # Initialize free slots list
    free_slots = []

    previous_end = day_start
    for event in sorted_events:
        # Clip events to business hours
        event_start = max(event['start'], day_start)
        event_end = min(event['end'], day_end)

        # Skip events outside business hours
        if event_end <= previous_end:
            continue

        # Free time before this event
        gap_start = previous_end
        gap_end = event_start - BUFFER_MINUTES
        if gap_end - gap_start >= meeting_duration:
            free_slots.append((gap_start, gap_end))

        # Update previous_end to end of event + buffer
        previous_end = max(previous_end, event_end + BUFFER_MINUTES)

    # After last event
    if day_end - previous_end >= meeting_duration:
        free_slots.append((previous_end, day_end))

    # Generate possible start times in 15-min increments
    available_starts = []
    for start, end in free_slots:
        # Round up to next 15-minute increment
        if start % SLOT_INCREMENT != 0:
            start += SLOT_INCREMENT - (start % SLOT_INCREMENT)
        slot_start = start
        while slot_start + meeting_duration <= end:
            # Skip lunch
            if slot_start < lunch_start or slot_start >= lunch_end:
                # Skip Friday cutoff
                if not (day.lower()[:3] == "fri" and slot_start > friday_last_start):
                    available_starts.append(minutes_to_time(slot_start))
            slot_start += SLOT_INCREMENT

    return available_starts