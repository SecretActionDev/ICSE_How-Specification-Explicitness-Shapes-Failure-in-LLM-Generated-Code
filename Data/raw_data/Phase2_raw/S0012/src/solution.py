from typing import List, Dict
from datetime import datetime, timedelta

def suggest_slots(
    events: List[Dict[str, str]],
    meeting_duration: int,
    day: str
) -> List[str]:

    WORK_START = datetime.strptime("09:00", "%H:%M")
    WORK_END = datetime.strptime("17:00", "%H:%M")
    LUNCH_START = datetime.strptime("12:00", "%H:%M")
    LUNCH_END = datetime.strptime("13:00", "%H:%M")
    FRIDAY_CUTOFF = datetime.strptime("15:00", "%H:%M")

    # Determine if the given date is Friday
    date_obj = datetime.strptime(day, "%Y-%m-%d")
    is_friday = date_obj.weekday() == 4  # Monday=0 ... Friday=4

    # Convert events to datetime ranges
    parsed_events = []
    for e in events:
        start = datetime.strptime(e["start"], "%H:%M")
        end = datetime.strptime(e["end"], "%H:%M")

        if end <= WORK_START or start >= WORK_END:
            continue

        parsed_events.append((start, end))

    parsed_events.sort(key=lambda x: x[0])

    slots = []
    current = WORK_START
    delta = timedelta(minutes=15)
    meeting_delta = timedelta(minutes=meeting_duration)

    while current + meeting_delta <= WORK_END:
        meeting_end = current + meeting_delta

        # Lunch restriction
        if LUNCH_START <= current < LUNCH_END:
            current += delta
            continue

        # Friday restriction
        if is_friday and current > FRIDAY_CUTOFF:
            current += delta
            continue

        overlap = False
        for event_start, event_end in parsed_events:
            if current <= event_end and meeting_end > event_start:
                overlap = True
                break

        if not overlap:
            slots.append(current.strftime("%H:%M"))

        current += delta

    return slots