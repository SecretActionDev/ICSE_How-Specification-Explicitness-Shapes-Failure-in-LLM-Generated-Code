from typing import List, Dict

def convert_time_to_mins(time_str: str) -> int:
    """Convert 'HH:MM' string to minutes since 00:00."""
    try:
        hour, minute = map(int, time_str.split(':'))
        if not (0 <= hour < 24 and 0 <= minute < 60):
            return False
        return hour * 60 + minute
    except:
        return False

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    """
    Suggest possible meeting start times for a given day.
    - Working hours: 09:00Р17:00 (540Р1020 minutes)
    - Meetings on Friday must start І 15:00
    - Slots every 15 minutes
    """
    WORK_START = 9 * 60  # 540 minutes
    WORK_END = 17 * 60   # 1020 minutes
    FRIDAY_CUTOFF = 15 * 60  # 900 minutes

    # Convert events to minutes for easier checking
    busy_times = []
    for event in events:
        start = convert_time_to_mins(event['start'])
        end = convert_time_to_mins(event['end'])
        if start is not False and end is not False:
            busy_times.append((start, end))

    busy_times.sort()  # sort by start time

    # Generate potential start times every 15 minutes
    slots = []
    current_time = WORK_START
    while current_time + meeting_duration <= WORK_END:
        # Friday constraint: do not start after 15:00
        if day == "Fri" and current_time > FRIDAY_CUTOFF:
            break

        # Check for conflicts
        conflict = False
        for start, end in busy_times:
            if not (current_time + meeting_duration <= start or current_time >= end):
                conflict = True
                break

        if not conflict:
            slots.append(f"{current_time // 60:02d}:{current_time % 60:02d}")

        current_time += 15  # move to next 15-minute slot

    return slots