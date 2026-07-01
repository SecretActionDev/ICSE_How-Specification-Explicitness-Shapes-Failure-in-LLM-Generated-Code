from typing import List, Dict

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    
    def to_minutes(t: str) -> int:
        h, m = map(int, t.split(":"))
        return h * 60 + m

    def to_time_str(m: int) -> str:
        return f"{m // 60:02d}:{m % 60:02d}"

    WORK_START = to_minutes("09:00")
    WORK_END = to_minutes("17:00")
    LUNCH_START = to_minutes("12:00")
    LUNCH_END = to_minutes("13:00")

    # Step 1: Normalize and filter events within working hours
    blocked = []

    for e in events:
        start = to_minutes(e["start"])
        end = to_minutes(e["end"])

        # Ignore events completely outside working hours
        if end <= WORK_START or start >= WORK_END:
            continue

        # Clamp to working hours
        start = max(start, WORK_START)
        end = min(end, WORK_END)

        blocked.append((start, end))

    # Add lunch break
    blocked.append((LUNCH_START, LUNCH_END))

    # Step 2: Generate candidate slots
    slots = []
    step = 15

    current = WORK_START
    latest_start = WORK_END - meeting_duration

    while current <= latest_start:
        slot_start = current
        slot_end = current + meeting_duration

        # Step 3: Check overlap
        conflict = False
        for b_start, b_end in blocked:
            if not (slot_end <= b_start or slot_start >= b_end):
                conflict = True
                break

        if not conflict:
            slots.append(to_time_str(slot_start))

        current += step

    return slots