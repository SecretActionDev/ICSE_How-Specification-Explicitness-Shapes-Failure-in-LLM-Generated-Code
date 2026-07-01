from typing import List, Dict

def suggest_slots(
    events: List[Dict[str, str]],
    meeting_duration: int,
    day: str
) -> List[str]:
    """
    Suggest valid meeting start times for a given day.
    
    Parameters:
    - events: list of dicts with 'start' and 'end' times in "HH:MM" format
    - meeting_duration: desired meeting duration in minutes
    - day: string representing the day of the week, e.g., 'Monday', 'Friday'
    
    Returns:
    - List of strings representing available meeting start times
    """
    
    # 1. Setup Working Hours and Lunch
    WORK_START = 9 * 60   # 09:00
    WORK_END = 17 * 60    # 17:00
    LUNCH_START = 12 * 60 # 12:00
    LUNCH_END = 13 * 60   # 13:00

    # Friday restriction: meetings cannot start after 15:00
    FRIDAY_END_LIMIT = 15 * 60  # 15:00

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
    # Sort for correct gap finding
    busy_times.sort()

    available_starts = []
    current_time = WORK_START

    while current_time + meeting_duration <= WORK_END:
        # Apply Friday restriction
        if day.lower() == "friday" and current_time > FRIDAY_END_LIMIT:
            break

        meeting_end = current_time + meeting_duration
        conflict_end = -1

        for b_start, b_end in busy_times:
            # Check for overlap
            if not (meeting_end <= b_start or current_time >= b_end):
                conflict_end = b_end
                break

        if conflict_end == -1:
            # No conflict, slot is valid
            # Also ensure Friday restriction is respected
            if day.lower() != "friday" or current_time <= FRIDAY_END_LIMIT:
                available_starts.append(to_str(current_time))
            current_time += 15  # Move to next 15-min step
        else:
            # Conflict found, jump to end of busy period and align to next 15-min
            current_time = conflict_end
            if current_time % 15 != 0:
                current_time += 15 - (current_time % 15)

    return available_starts