from typing import List, Dict

WORK_START = 9 * 60
WORK_END = 17 * 60
LUNCH_START = 12 * 60
LUNCH_END = 13 * 60
BUFFER = 15


def to_minutes(t: str) -> int:
    h, m = map(int, t.split(":"))
    return h * 60 + m


def to_time_str(m: int) -> str:
    return f"{m // 60:02d}:{m % 60:02d}"


def merge_intervals(intervals):
    intervals.sort()
    merged = []

    for start, end in intervals:
        if not merged or merged[-1][1] < start:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    return merged


def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    # Step 1: convert events + apply buffer
    blocked = []

    for e in events:
        start = to_minutes(e["start"])
        end = to_minutes(e["end"]) + BUFFER
        blocked.append((start, end))

    # Step 2: add lunch
    blocked.append((LUNCH_START, LUNCH_END))

    # Step 3: merge overlaps
    blocked = merge_intervals(blocked)

    # Step 4: find available gaps
    slots = []
    current = WORK_START

    for start, end in blocked:
        if current < start:
            gap_start = current
            gap_end = start

            # generate slots every 15 min
            t = gap_start
            while t + meeting_duration <= gap_end:
                if t >= WORK_START and t + meeting_duration <= WORK_END:
                    slots.append(to_time_str(t))
                t += 15

        current = max(current, end)

    # last gap (after final event)
    if current < WORK_END:
        t = current
        while t + meeting_duration <= WORK_END:
            slots.append(to_time_str(t))
            t += 15

    return sorted(slots)
