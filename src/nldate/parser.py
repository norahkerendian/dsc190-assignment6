import re
from datetime import date, timedelta
import calendar

_MONTH_NAMES = {m.lower(): i for i, m in enumerate(calendar.month_name) if m}
_MONTH_NAMES.update({m.lower(): i for i, m in enumerate(calendar.month_abbr) if m})
_DAY_NAMES = [calendar.day_name[i].lower() for i in range(7)]
_ABS_DATE_RE = re.compile(r"(\w+)\.?\s+(\d+)(?:st|nd|rd|th)?,?\s*(\d{4})")
_ISO_DATE_RE = re.compile(r"(\d{4})-(\d{1,2})-(\d{1,2})")
_SLASH_DATE_RE = re.compile(r"(\d{4})/(\d{1,2})/(\d{1,2})")


def _parse_int(word: str) -> int:
    w = word.lower()
    if w.isdigit():
        return int(w)
    return {
        "a": 1,
        "an": 1,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }.get(w, 0)


def _add_months(d: date, n: int) -> date:
    total = d.month - 1 + n
    year = d.year + total // 12
    month = total % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def _apply_offset(d: date, n: int, unit: str) -> date:
    unit = unit.lower().rstrip("s")
    if unit == "day":
        return d + timedelta(days=n)
    if unit == "week":
        return d + timedelta(weeks=n)
    if unit == "month":
        return _add_months(d, n)
    if unit == "year":
        return _add_months(d, n * 12)
    return d


def _parse_abs_date(s: str) -> date | None:
    m = _ISO_DATE_RE.match(s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = _SLASH_DATE_RE.match(s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = _ABS_DATE_RE.match(s)
    if not m:
        return None
    month = _MONTH_NAMES.get(m.group(1).lower())
    if month is None:
        return None
    return date(int(m.group(3)), month, int(m.group(2)))


def _resolve_base(s: str, today: date) -> date | None:
    s = s.strip().lower()
    if s in ("today", "now"):
        return today
    if s == "tomorrow":
        return today + timedelta(days=1)
    if s == "yesterday":
        return today - timedelta(days=1)
    return _parse_abs_date(s)


_OFFSET_UNIT_RE = re.compile(
    r"(a|an|one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+"
    r"(day|week|month|year)s?$",
    re.IGNORECASE,
)


def _parse_compound_offset(s: str) -> list[tuple[int, str]]:
    parts = re.split(r"\s+and\s+|,\s*", s, flags=re.IGNORECASE)
    result: list[tuple[int, str]] = []
    for part in parts:
        m = _OFFSET_UNIT_RE.match(part.strip())
        if m:
            result.append((_parse_int(m.group(1)), m.group(2).lower()))
    return result


def _apply_compound_offset(base: date, offset_str: str, sign: int) -> date:
    parts = _parse_compound_offset(offset_str)
    if not parts:
        return base
    result = base
    for n, unit in parts:
        result = _apply_offset(result, sign * n, unit)
    return result


def parse(s: str, today: date | None = None) -> date | None:
    if today is None:
        today = date.today()
    s = s.strip()

    m = re.match(r"next\s+(\w+)", s, re.IGNORECASE)
    if m:
        day_name = m.group(1).lower()
        try:
            target = _DAY_NAMES.index(day_name)
        except ValueError:
            pass
        else:
            cur = today.weekday()
            diff = (target - cur) % 7
            if diff == 0:
                diff = 7
            return today + timedelta(days=diff)

    m = re.match(r"last\s+(\w+)", s, re.IGNORECASE)
    if m:
        day_name = m.group(1).lower()
        try:
            target = _DAY_NAMES.index(day_name)
        except ValueError:
            pass
        else:
            cur = today.weekday()
            diff = (cur - target) % 7
            if diff == 0:
                diff = 7
            return today - timedelta(days=diff)

    if s.lower() == "today":
        return today
    if s.lower() == "tomorrow":
        return today + timedelta(days=1)
    if s.lower() == "yesterday":
        return today - timedelta(days=1)

    m = re.match(
        r"in\s+(a|an|one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+"
        r"(day|week|month|year)s?$",
        s,
        re.IGNORECASE,
    )
    if m:
        return _apply_offset(today, _parse_int(m.group(1)), m.group(2))

    m = re.match(
        r"(a|an|one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+"
        r"(day|week|month|year)s?\s+ago$",
        s,
        re.IGNORECASE,
    )
    if m:
        return _apply_offset(today, -_parse_int(m.group(1)), m.group(2))

    d = _parse_abs_date(s)
    if d is not None:
        return d

    m = re.match(r"(.+?)\s+(from|before|after)\s+(.+)", s, re.IGNORECASE)
    if m:
        base = _resolve_base(m.group(3), today)
        if base is not None:
            sign = 1 if m.group(2).lower() in ("from", "after") else -1
            return _apply_compound_offset(base, m.group(1), sign)

    return None
