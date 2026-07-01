from typing import List, Dict

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
        day: Three-letter day abbreviation (e.g., "Mon", "Tue", ... "Fri")

    Returns:
        List of valid start times as "HH:MM" sorted ascending.

    Notes:
        - Working hours are 09:00 to 17:00.
        - Lunch break is 12:00Р13:00.
        - Meetings on Fridays must not start after 15:00.
        - Existing events are respected (no overlap allowed).
    """
    if meeting_duration <= 0:
        return []

    work_start = 9 * 60
    work_end = 17 * 60
    if meeting_duration > (work_end - work_start):
        return []

    def to_minutes(t: str) -> int:
        h, m = t.split(":")
        return int(h) * 60 + int(m)

    blocked = []
    for ev in events:
        s = to_minutes(ev["start"])
        e = to_minutes(ev["end"])
        if e <= work_start or s >= work_end:
            continue
        if s < work_start:
            s = work_start
        if e > work_end:
            e = work_end
        if s < e:
            e_block = e + 1 if e < work_end else e
            blocked.append((s, e_block))

    # Lunch break blocks all overlapping slots (12:00Р13:00)
    blocked.append((12 * 60, 13 * 60))

    if blocked:
        blocked.sort()
        merged = []
        for s, e in blocked:
            if not merged or s > merged[-1][1]:
                merged.append([s, e])
            else:
                if e > merged[-1][1]:
                    merged[-1][1] = e
    else:
        merged = []

    # Friday latest start restriction
    friday_latest_start = 15 * 60 if day == "Fri" else work_end - meeting_duration
    latest_start = min(work_end - meeting_duration, friday_latest_start)

    slots = []
    idx = 0
    for start in range(work_start, latest_start + 1, 15):
        end = start + meeting_duration
        while idx < len(merged) and merged[idx][1] <= start:
            idx += 1
        if idx < len(merged) and end > merged[idx][0]:
            continue
        slots.append(f"{start // 60:02d}:{start % 60:02d}")

    return slots