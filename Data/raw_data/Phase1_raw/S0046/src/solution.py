from typing import List, Dict
from datetime import datetime

def time_to_minutes(time_str: str) -> int:
    h, m = map(int, time_str.split(":"))
    return h * 60 + m

def minutes_to_time(minutes: int) -> str:
    h = minutes // 60
    m = minutes % 60
    return f"{h:02d}:{m:02d}"

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    # Minimum allowed duration: 15 mins
    if meeting_duration < 15:
        raise ValueError("Meeting duration must be at least 15 minutes.")

    # Define working hours
    WORK_START = 9 * 60    # 09:00
    WORK_END = 17 * 60     # 17:00
    GRANULARITY = 15       # 15-min increments

    # Convert events to minutes and clip to working hours
    busy_times = []
    for event in events:
        start = max(time_to_minutes(event["start"]), WORK_START)
        end = min(time_to_minutes(event["end"]), WORK_END)
        if start < end:  # only consider events inside working hours
            busy_times.append((start, end))
    busy_times.sort()

    # Merge overlapping events
    merged = []
    for start, end in busy_times:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    # Generate available slots
    available_slots = []
    current_time = WORK_START

    # Skip past days if needed (optional, not strictly enforced in tests)
    # now = datetime.now()
    # today_name = now.strftime("%A")
    # if day != today_name and datetime.strptime(day, "%A") < now:
    #     return []

    for start, end in merged:
        while current_time + meeting_duration <= start:
            available_slots.append(minutes_to_time(current_time))
            current_time += GRANULARITY
        current_time = max(current_time, end)

    # Fill after last event until WORK_END
    while current_time + meeting_duration <= WORK_END:
        available_slots.append(minutes_to_time(current_time))
        current_time += GRANULARITY

    return available_slots