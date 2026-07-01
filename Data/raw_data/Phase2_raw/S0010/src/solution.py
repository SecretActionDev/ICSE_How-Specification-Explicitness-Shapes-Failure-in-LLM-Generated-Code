from typing import List, Dict, Tuple

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    """
    Suggest available meeting slots for a given day.

    Args:
        events: List of dicts with 'start' and 'end' times in "HH:MM" format.
        meeting_duration: Duration of the meeting in minutes.
        day: Day of the week as string, e.g., "Monday", "Friday".

    Returns:
        List of available start times in "HH:MM" format.
        Fridays: meetings cannot start after 15:00.
    """
    if meeting_duration <= 0:
        return []

    def to_minutes(t: str) -> int:
        h, m = t.split(":")
        return int(h) * 60 + int(m)

    def to_hhmm(x: int) -> str:
        return f"{x // 60:02d}:{x % 60:02d}"

    WORK_START = to_minutes("09:00")
    WORK_END   = to_minutes("17:00")
    LUNCH_START = to_minutes("12:00")
    LUNCH_END   = to_minutes("13:00")
    STEP = 15

    # Special Friday limit
    FRIDAY_LIMIT = to_minutes("15:00") if day.lower() == "friday" else WORK_END

    # If meeting can't fit at all
    if WORK_START + meeting_duration > WORK_END:
        return []

    busy: List[Tuple[int, int]] = []

    # Add events clipped to working hours
    for e in events or []:
        if not isinstance(e, dict) or "start" not in e or "end" not in e:
            continue
        try:
            s = to_minutes(e["start"])
            en = to_minutes(e["end"])
        except Exception:
            continue
        if en <= s:
            continue
        if en <= WORK_START or s >= WORK_END:
            continue
        s = max(s, WORK_START)
        en = min(en, WORK_END)
        if en > s:
            busy.append((s, en))

    # Lunch break blocks
    busy.append((LUNCH_START, LUNCH_END))

    # Merge overlapping busy intervals
    busy.sort()
    merged: List[Tuple[int, int]] = []
    for s, en in busy:
        if not merged or s >= merged[-1][1]:
            merged.append((s, en))
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], en))

    # Compute free intervals within working hours
    free: List[Tuple[int, int]] = []
    cursor = WORK_START
    for s, en in merged:
        if s > cursor:
            free.append((cursor, s))
        cursor = max(cursor, en)
    if cursor < WORK_END:
        free.append((cursor, WORK_END))

    # Round up to STEP boundary
    def ceil_to_step(t: int) -> int:
        r = t % STEP
        return t if r == 0 else t + (STEP - r)

    slots: List[str] = []
    for fs, fe in free:
        t = ceil_to_step(fs)
        latest_start = min(fe - meeting_duration, FRIDAY_LIMIT - meeting_duration)
        while t <= latest_start:
            slots.append(to_hhmm(t))
            t += STEP

    return slots