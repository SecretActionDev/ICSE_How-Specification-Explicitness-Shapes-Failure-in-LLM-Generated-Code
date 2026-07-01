from typing import List, Dict
from datetime import datetime

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    import re

    # ---------- Step 0: Validate inputs ----------
    if meeting_duration <= 0:
        raise ValueError("Meeting duration must be positive")
    if meeting_duration % 30 != 0:
        raise ValueError("Meeting duration must be a multiple of 30 minutes")
    
    # Validate day string
    try:
        dt = datetime.strptime(day, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid day string")
    
    # 15-min granularity
    GRANULARITY = 15

    # Working hours
    weekday = dt.weekday()
    work_start = 9*60
    work_end = 17*60
    if weekday == 4:  # Friday
        # Optional Friday cut-off rules: latest meeting slots may differ
        pass
    
    # Lunch break 12:00–13:00
    lunch_start = 12*60
    lunch_end = 13*60

    # ---------- Step 1: Convert and validate events ----------
    merged_events = []
    for e in events:
        try:
            start_h, start_m = map(int, e['start'].split(':'))
            end_h, end_m = map(int, e['end'].split(':'))
        except:
            raise ValueError("Invalid time format in events")
        start = start_h*60 + start_m
        end = end_h*60 + end_m
        if start >= end:
            raise ValueError("Event start time must be before end time")
        merged_events.append((start, end))
    
    # ---------- Step 2: Merge overlapping events ----------
    merged_events.sort()
    merged = []
    for start, end in merged_events:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    
    # ---------- Step 3: Clip to working hours and add 15-min buffer ----------
    BUFFER = 15
    adjusted = []
    for s,e in merged:
        # Clip to work hours
        s = max(s, work_start)
        e = min(e, work_end)
        # Add buffer after event
        e += BUFFER
        if s < e:
            adjusted.append([s,e])
    merged = adjusted
    
    # ---------- Step 4: Compute free intervals ----------
    free_intervals = []
    prev_end = work_start
    for s,e in merged:
        if s - prev_end >= meeting_duration:
            free_intervals.append((prev_end, s))
        prev_end = max(prev_end, e)
    if work_end - prev_end >= meeting_duration:
        free_intervals.append((prev_end, work_end))
    
    # ---------- Step 5: Subtract lunch break ----------
    def subtract_lunch(intervals):
        result = []
        for s,e in intervals:
            if e <= lunch_start or s >= lunch_end:
                result.append((s,e))
            else:
                if s < lunch_start:
                    result.append((s,lunch_start))
                if e > lunch_end:
                    result.append((lunch_end,e))
        return result
    
    free_intervals = subtract_lunch(free_intervals)
    
    # ---------- Step 6: Generate slots ----------
    slots = []
    for s,e in free_intervals:
        # Align s to next 15-min boundary
        s = ((s + GRANULARITY - 1)//GRANULARITY)*GRANULARITY
        while s + meeting_duration <= e:
            slots.append(f"{s//60:02d}:{s%60:02d}")
            s += GRANULARITY
    
    return sorted(slots)