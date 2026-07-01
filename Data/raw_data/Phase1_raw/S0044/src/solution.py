from typing import List, Dict

def time_to_minutes(t: str) -> int:
    """Convert 'HH:MM' string to minutes since midnight."""
    h, m = map(int, t.split(":"))
    return h * 60 + m

def minutes_to_time(m: int) -> str:
    """Convert minutes since midnight to 'HH:MM' string."""
    h = m // 60
    m = m % 60
    return f"{h:02d}:{m:02d}"

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    # Define working periods in minutes
    working_periods = [(time_to_minutes("09:00"), time_to_minutes("12:00")),
                       (time_to_minutes("13:00"), time_to_minutes("17:00"))]

    # Convert events to minutes and filter only those overlapping working hours
    busy_intervals = []
    for event in events:
        start = time_to_minutes(event["start"])
        end = time_to_minutes(event["end"])
        # Ignore events completely outside working hours
        if end <= working_periods[0][0] or start >= working_periods[-1][1]:
            continue
        busy_intervals.append((start, end))
    
    # Sort intervals for easier checking
    busy_intervals.sort()

    # Generate candidate slots on 15-min grid within working periods
    slots = []
    for period_start, period_end in working_periods:
        t = period_start
        while t + meeting_duration <= period_end:
            slots.append(t)
            t += 15

    # Filter out slots that conflict with existing events
    valid_slots = []
    for slot_start in slots:
        slot_end = slot_start + meeting_duration
        conflict = False
        for ev_start, ev_end in busy_intervals:
            # Overlap check
            if slot_start < ev_end and slot_end > ev_start:
                conflict = True
                break
            # For meetings >= 30 mins, cannot start exactly at an event end
            if meeting_duration >= 30 and slot_start == ev_end:
                conflict = True
                break
        if not conflict:
            valid_slots.append(minutes_to_time(slot_start))

    return valid_slots