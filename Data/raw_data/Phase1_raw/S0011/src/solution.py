## Student Name:
## Student ID: 

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""

# def suggest_slots(
#     events: List[Dict[str, str]],
#     meeting_duration: int,
#     day: str
# ) -> List[str]:
#     """
#     Suggest possible meeting start times for a given day.

#     Args:
#         events: List of dicts with keys {"start": "HH:MM", "end": "HH:MM"}
#         meeting_duration: Desired meeting length in minutes
#         day: Three-letter day abbreviation (e.g., "Mon", "Tue", ... "Fri")

#     Returns:
#         List of valid start times as "HH:MM" sorted ascending
#     """
#     # TODO: Implement this function
#     raise NotImplementedError("suggest_slots function has not been implemented yet")

from typing import List, Dict

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    if meeting_duration <= 0:
        return []

    def to_minutes(hhmm: str) -> int:
        h, m = hhmm.split(":")
        return int(h) * 60 + int(m)

    def to_hhmm(x: int) -> str:
        return f"{x//60:02d}:{x%60:02d}"

    WORK_START = to_minutes("09:00")
    WORK_END   = to_minutes("17:00")

    LUNCH_START = to_minutes("12:00")
    LUNCH_END   = to_minutes("13:00")

    STEP = 15

    # Parse + CLIP events to working hours; ignore events fully outside.
    busy = []
    for e in events:
        if "start" not in e or "end" not in e:
            continue
        s = to_minutes(e["start"])
        t = to_minutes(e["end"])
        if t <= s:
            continue

        # If completely outside, ignore
        if t <= WORK_START or s >= WORK_END:
            continue

        # Clip to working window
        s = max(s, WORK_START)
        t = min(t, WORK_END)
        if t > s:
            busy.append((s, t))

    # Merge overlapping/touching busy intervals
    busy.sort()
    merged = []
    for s, t in busy:
        if not merged or s > merged[-1][1]:
            merged.append([s, t])
        else:
            merged[-1][1] = max(merged[-1][1], t)

    latest_start = WORK_END - meeting_duration
    if latest_start < WORK_START:
        return []

    res: List[str] = []
    start = WORK_START
    if start % STEP != 0:
        start += (STEP - start % STEP)

    i = 0
    while start <= latest_start:
        end = start + meeting_duration

        # lunch: cannot START during 12:00–13:00
        if LUNCH_START <= start < LUNCH_END:
            start += STEP
            continue

        while i < len(merged) and merged[i][1] <= start:
            i += 1

        overlaps = False
        if i < len(merged):
            bs, bt = merged[i]
            if start < bt and bs < end:
                overlaps = True

        if not overlaps:
            res.append(to_hhmm(start))

        start += STEP

    return res