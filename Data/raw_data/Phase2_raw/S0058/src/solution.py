from typing import List, Dict
from datetime import datetime, timedelta

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

    weekday = date_obj.weekday()  # Monday=0, Sunday=6
    if weekday >= 5:  # weekend
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

    parsed.sort()

    # -----------------------------
    # Merge overlapping events
    # -----------------------------
    merged = []
    for s, e_ in parsed:
        if not merged or merged[-1][1] < s:
            merged.append([s, e_])
        else:
            merged[-1][1] = max(merged[-1][1], e_)
    merged = [(s, e_) for s, e_ in merged]

    # -----------------------------
    # Working blocks
    # -----------------------------
    MORNING = (9*60, 12*60)
    AFTERNOON = (13*60 + 15, 17*60)  # 13:15 start
    blocks = [MORNING, AFTERNOON]

    # Friday cutoff
    is_friday = weekday == 4
    FRIDAY_LAST_START = 15*60  # cannot start after 15:00

    # -----------------------------
    # Filter events into working hours
    # -----------------------------
    working_events = []
    for s, e_ in merged:
        for ws, we in blocks:
            if not (e_ <= ws or s >= we):
                working_events.append((max(s, ws), min(e_, we)))

    # -----------------------------
    # Generate candidate start times
    # -----------------------------
    candidates = []
    for ws, we in blocks:
        t = ws
        while t + meeting_duration <= we:
            # Apply Friday cutoff rule
            if is_friday and t >= FRIDAY_LAST_START:
                break
            candidates.append(t)
            t += 15  # 15-min increments

    # -----------------------------
    # Validate candidates
    # -----------------------------
    valid = []
    for start in candidates:
        end = start + meeting_duration
        ok = True

        for es, ee in working_events:
            # Overlap check
            if not (end <= es or start >= ee):
                ok = False
                break
            # 15-min buffer after event
            if ee <= start < ee + 15:
                ok = False
                break

        # Ensure Friday meeting doesn't end after 17:00
        if is_friday and end > 17*60:
            ok = False

        if ok:
            valid.append(start)

    # -----------------------------
    # Output
    # -----------------------------
    return [to_str(t) for t in sorted(valid)]