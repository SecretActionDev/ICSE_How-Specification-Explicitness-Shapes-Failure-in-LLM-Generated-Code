from typing import List, Dict

def to_minutes(t: str) -> int:
    h, m = map(int, t.split(":"))
    return h * 60 + m

def to_time_str(m: int) -> str:
    return f"{m // 60:02d}:{m % 60:02d}"

def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    if not intervals:
        return []
    
    intervals.sort()
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        last_end = merged[-1][1]
        if start <= last_end:  # overlap
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])
    
    return merged

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    WORK_START = to_minutes("09:00")
    WORK_END = to_minutes("17:00")
    
    # Convert events to minutes
    intervals = []
    for e in events:
        start = to_minutes(e["start"])
        end = to_minutes(e["end"])
        intervals.append([start, end])
    
    # Add lunch break
    intervals.append([to_minutes("12:00"), to_minutes("13:00")])
    
    # Merge overlapping intervals
    blocked = merge_intervals(intervals)
    
    valid_slots = []
    
    # Generate slots every 30 minutes
    current = WORK_START
    while current + meeting_duration <= WORK_END:
        meeting_end = current + meeting_duration
        
        # Check conflict
        conflict = False
        for start, end in blocked:
            if not (meeting_end <= start or current >= end):
                conflict = True
                break
        
        if not conflict:
            valid_slots.append(to_time_str(current))
        
        current += 30  # 30-minute increments
    
    return valid_slots