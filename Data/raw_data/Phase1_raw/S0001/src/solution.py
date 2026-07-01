## Student Name: Khawaja Faiza Qaisar
## Student ID: 217948233

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""


from typing import List, Dict

def suggest_slots(
    events: List[Dict[str, str]],
    meeting_duration: int,
    day: str
) -> List[str]:
    # 1. Setup Working Hours and Lunch
    WORK_START = 9 * 60   # 09:00
    WORK_END = 17 * 60    # 17:00
    LUNCH_START = 12 * 60 # 12:00
    LUNCH_END = 13 * 60   # 13:00
    
    def to_minutes(time_str: str) -> int:
        h, m = map(int, time_str.split(':'))
        return h * 60 + m

    def to_str(minutes: int) -> str:
        h, m = divmod(minutes, 60)
        return f"{h:02d}:{m:02d}"

    # 2. Build and sort the busy list
    busy_times = []
    for event in events:
        start = to_minutes(event["start"])
        end = to_minutes(event["end"])
        if end > WORK_START and start < WORK_END:
            busy_times.append((max(start, WORK_START), min(end, WORK_END)))
    
    # Add Lunch Break
    busy_times.append((LUNCH_START, LUNCH_END))
    # Crucial: Must be sorted for the logic to find the next available gap correctly
    busy_times.sort()

    available_starts = []
    current_time = WORK_START

    while current_time + meeting_duration <= WORK_END:
        meeting_end = current_time + meeting_duration
        conflict_end = -1
        
        for b_start, b_end in busy_times:
            # Check if current window [current_time, meeting_end] overlaps with [b_start, b_end]
            if not (meeting_end <= b_start or current_time >= b_end):
                conflict_end = b_end
                break
        
        if conflict_end == -1:
            # No conflict found
            available_starts.append(to_str(current_time))
            # The test 'test_unsorted_events_are_handled' implies a 15-min step 
            # AFTER a successful slot is found.
            current_time += 15
        else:
            # Conflict found! Jump to the end of the busy period.
            current_time = conflict_end

            # Align to next 15-minute boundary
            if current_time % 15 != 0:
                current_time += 15 - (current_time % 15)

    return available_starts