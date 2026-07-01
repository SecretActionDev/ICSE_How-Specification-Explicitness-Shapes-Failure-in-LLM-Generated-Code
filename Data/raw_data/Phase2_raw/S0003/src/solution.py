from typing import List, Dict

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    """
    Suggest valid meeting start times for a given day.

    Parameters:
    - events: list of dictionaries with "start" and "end" times in "HH:MM" format
    - meeting_duration: desired meeting duration in minutes
    - day: name of the day (e.g., "Monday", "Friday")

    Returns:
    - List of valid start times as strings in "HH:MM" format.
    - Respects working hours (09:00-17:00), lunch break (12:00-13:00), existing events,
      15:00 limit for meetings on Fridays, and 15-minute increments.
    """
    WORK_START = 9 * 60   # 09:00
    WORK_END = 17 * 60    # 17:00
    STEP_MINUTES = 15

    LUNCH_START = 12 * 60
    LUNCH_END = 13 * 60

    # Validate meeting duration
    if not isinstance(meeting_duration, int) or meeting_duration <= 0:
        return []
    if meeting_duration > (WORK_END - WORK_START):
        return []

    def to_minutes(t: str) -> int:
        hh, mm = t.split(":")
        return int(hh) * 60 + int(mm)

    def to_hhmm(m: int) -> str:
        return f"{m // 60:02d}:{m % 60:02d}"

    # Parse + clamp events into working window
    intervals = []
    for e in events:
        if "start" not in e or "end" not in e:
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
            intervals.append((s, en))

    # Sort + merge overlapping intervals
    intervals.sort()
    merged = []
    for s, en in intervals:
        if not merged:
            merged.append([s, en])
        else:
            if s <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], en)
            else:
                merged.append([s, en])

    def overlaps_with_event(meet_start: int, meet_end: int, ev_start: int, ev_end: int) -> bool:
        # Conflict if meeting overlaps event; meet_end == ev_start counts as conflict
        return (meet_start < ev_end) and (meet_end >= ev_start)

    results: List[str] = []

    # Latest possible start time
    latest_start = WORK_END - meeting_duration

    # Apply Friday-specific constraint
    if day.lower() == "friday":
        friday_limit = 15 * 60  # 15:00 in minutes
        latest_start = min(latest_start, friday_limit)

    # Round start time up to nearest 15-minute increment
    t = WORK_START
    rem = t % STEP_MINUTES
    if rem != 0:
        t += (STEP_MINUTES - rem)

    while t <= latest_start:
        # Lunch constraint blocks START times only
        if LUNCH_START <= t < LUNCH_END:
            t += STEP_MINUTES
            continue

        meet_end = t + meeting_duration

        conflict = False
        for ev_s, ev_e in merged:
            if overlaps_with_event(t, meet_end, ev_s, ev_e):
                conflict = True
                break

        if not conflict:
            results.append(to_hhmm(t))

        t += STEP_MINUTES

    return results