from typing import List, Dict

def time_to_minutes(t: str) -> int:
    h, m = map(int, t.split(":"))
    return h * 60 + m

def minutes_to_time(m: int) -> str:
    h = m // 60
    m = m % 60
    return f"{h:02d}:{m:02d}"

def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    if not intervals:
        return []
    intervals.sort()
    merged = [intervals[0]]
    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:  # overlap
            last[1] = max(last[1], current[1])
        else:
            merged.append(current)
    return merged

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    if meeting_duration <= 0:
        return []
    
    WORK_START = 9 * 60  # 540
    WORK_END = 17 * 60   # 1020
    LUNCH_START = 12 * 60
    LUNCH_END = 13 * 60
    BUFFER = 15
    
    # Convert events to intervals with 15-min buffer
    busy_intervals = []
    for e in events:
        start = max(WORK_START, time_to_minutes(e['start']) - BUFFER)
        end = min(WORK_END, time_to_minutes(e['end']) + BUFFER)
        busy_intervals.append([start, end])
    
    # Add lunch as a busy interval
    busy_intervals.append([LUNCH_START, LUNCH_END])
    
    # Merge overlapping intervals
    busy_intervals = merge_intervals(busy_intervals)
    
    # Compute free intervals
    free_intervals = []
    prev_end = WORK_START
    for start, end in busy_intervals:
        if start > prev_end:
            free_intervals.append([prev_end, start])
        prev_end = max(prev_end, end)
    if prev_end < WORK_END:
        free_intervals.append([prev_end, WORK_END])
    
    # Generate available start times
    available_slots = []
    for start, end in free_intervals:
        slot_start = ((start + 14) // 15) * 15  # next 15-min multiple
        while slot_start + meeting_duration <= end:
            available_slots.append(minutes_to_time(slot_start))
            slot_start += 15
    
    return available_slots