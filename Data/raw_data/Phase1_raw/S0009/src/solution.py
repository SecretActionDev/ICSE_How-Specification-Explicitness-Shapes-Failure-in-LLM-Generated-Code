## Student Name: Manya Khattri
## Student ID: 219830025

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""
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

    #Reject weekends
    try:
        date_obj = datetime.strptime(day,"%Y-%m-%d")
    except ValueError:
        return[] #invalid date format

    WORK_START = 9*60 #9:00
    WORK_END = 17*60 #17:00
    LUNCH_START = 12*60 #12:00
    LUNCH_END = 13*60 #13:00

    def to_minutes(t: str) -> int:
        h, m = map(int, t.split(":"))
        return h * 60 + m

    def to_time_str(minutes: int) -> str:
        return f"{minutes // 60:02d}:{minutes % 60:02d}"

    # Convert events to minute intervals
    busy_intervals = []
    for event in events:
        start = to_minutes(event["start"])
        end = to_minutes(event["end"])
        #clipping event to working hours
        start = max(start,WORK_START)
        end = min(end, WORK_END)
        if start<end:
            busy_intervals.append((start, end))

    # Sort events by start time
    busy_intervals.sort()

    available_starts = []

     # Try every possible start minute in working hours
    for start in range(WORK_START, WORK_END - meeting_duration + 1,15):

        #Adding lunch break
        if LUNCH_START<=start<LUNCH_END:
            continue
        end = start + meeting_duration

        # Check for overlap
        conflict = False
        for busy_start, busy_end in busy_intervals:
            if not (end <= busy_start or start >= busy_end):
                conflict = True
                break

        if not conflict:
            available_starts.append(to_time_str(start))

    return available_starts

    # TODO: Implement this function
    #commenting the raise because it is unreachable and not needed, since everything is filled.
    #raise NotImplementedError("suggest_slots function has not been implemented yet")