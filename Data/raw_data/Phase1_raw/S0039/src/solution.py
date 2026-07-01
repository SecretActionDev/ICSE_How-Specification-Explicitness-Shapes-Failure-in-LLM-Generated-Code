from typing import List, Dict

# Define working hours and lunch
WORK_START = "09:00"
WORK_END = "17:00"
LUNCH_START = "12:00"
LUNCH_END = "13:00"
SLOT_INTERVAL = 15  # minutes, 15-min granularity

# Helper: convert "HH:MM" to minutes
def time_to_minutes(t: str) -> int:
    hours, minutes = map(int, t.split(":"))
    return hours * 60 + minutes

# Helper: convert minutes to "HH:MM"
def minutes_to_time(m: int) -> str:
    hours = m // 60
    minutes = m % 60
    return f"{hours:02d}:{minutes:02d}"

# Prepare and sort events
def prepare_events(events: List[Dict[str, str]]) -> List[tuple]:
    event_list = []
    for e in events:
        start = time_to_minutes(e['start'])
        end = time_to_minutes(e['end'])
        event_list.append((start, end))
    return sorted(event_list)

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    if meeting_duration <= 0:
        return []

    # Convert working hours and lunch to minutes
    WORK_START_MIN = time_to_minutes(WORK_START)
    WORK_END_MIN = time_to_minutes(WORK_END)
    LUNCH_START_MIN = time_to_minutes(LUNCH_START)
    LUNCH_END_MIN = time_to_minutes(LUNCH_END)

    # Add lunch as a blocked event
    events = events + [{"start": LUNCH_START, "end": LUNCH_END}]

    # Prepare and sort events
    event_times = prepare_events(events)

    # Merge overlapping events for safety
    merged_events = []
    for start, end in event_times:
        if not merged_events:
            merged_events.append([start, end])
        else:
            last_start, last_end = merged_events[-1]
            if start <= last_end:
                merged_events[-1][1] = max(last_end, end)
            else:
                merged_events.append([start, end])

    # Initialize free slots
    free_slots = []
    current = WORK_START_MIN
    for start, end in merged_events:
        if start - current >= meeting_duration:
            free_slots.append((current, start))
        current = max(current, end)
    if WORK_END_MIN - current >= meeting_duration:
        free_slots.append((current, WORK_END_MIN))

    # Generate valid start times in 15-min increments
    valid_slots = []
    for start, end in free_slots:
        slot_start = ((start + SLOT_INTERVAL - 1) // SLOT_INTERVAL) * SLOT_INTERVAL  # round up to next 15-min
        while slot_start + meeting_duration <= end:
            valid_slots.append(minutes_to_time(slot_start))
            slot_start += SLOT_INTERVAL

    return valid_slots