from typing import List, Dict
from datetime import datetime

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:

    # -----------------------------
    # Validation
    # -----------------------------
    if meeting_duration <= 0:
        raise ValueError("Meeting duration must be positive")

    if meeting_duration % 30 != 0:
        raise ValueError("Meeting duration must be a multiple of 30 minutes")

    # Validate date
    try:
        date_obj = datetime.strptime(day, "%Y-%m-%d")
    except:
        raise ValueError("Invalid date")

    # Weekend check
    if date_obj.weekday() >= 5:  # Sat=5, Sun=6
        return []

    # -----------------------------
    # Helpers
    # -----------------------------
    def to_minutes(t: str) -> int:
        try:
            h, m = map(int, t.split(":"))
            if not (0 <= h < 24 and 0 <= m < 60):
                raise ValueError
            return h * 60 + m
        except:
            raise ValueError("Invalid time format")

    def to_str(m: int) -> str:
        return f"{m // 60:02d}:{m % 60:02d}"

    # -----------------------------
    # Parse events
    # -----------------------------
    parsed = []
    for e in events:
        s = to_minutes(e["start"])
        e_ = to_minutes(e["end"])
        if s >= e_:
            raise ValueError("Invalid event interval")
        parsed.append((s, e_))

    # Sort
    parsed.sort()

    # -----------------------------
    # Merge overlapping events
    # -----------------------------
    merged = []
    for s, e in parsed:
        if not merged or merged[-1][1] < s:
            merged.append([s, e])
        else:
            merged[-1][1] = max(merged[-1][1], e)

    merged = [(s, e) for s, e in merged]

    # -----------------------------
    # Working blocks
    # -----------------------------
    MORNING = (9*60, 12*60)
    AFTERNOON = (13*60 + 15, 17*60)  # 13:15 start

    blocks = [MORNING, AFTERNOON]

    # Friday cutoff
    is_friday = date_obj.weekday() == 4
    FRIDAY_LAST_START = 14*60 + 30  # 14:30

    # -----------------------------
    # Filter events into working hours
    # -----------------------------
    working_events = []
    for s, e in merged:
        for ws, we in blocks:
            if not (e <= ws or s >= we):
                working_events.append((max(s, ws), min(e, we)))

    # -----------------------------
    # Generate candidates
    # -----------------------------
    candidates = []
    for ws, we in blocks:
        t = ws
        while t + meeting_duration <= we:
            if is_friday and t > FRIDAY_LAST_START:
                break
            candidates.append(t)
            t += 15

    # -----------------------------
    # Validate candidates
    # -----------------------------
    valid = []

    for start in candidates:
        end = start + meeting_duration
        ok = True

        for es, ee in working_events:

            # Overlap
            if not (end <= es or start >= ee):
                ok = False
                break

            # 15-min buffer after event
            if ee <= start < ee + 15:
                ok = False
                break

        if ok:
            valid.append(start)

    # -----------------------------
    # Output
    # -----------------------------
    return [to_str(t) for t in sorted(valid)]