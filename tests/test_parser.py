from datetime import date

from nldate import parser


def test_tomorrow():
    assert parser.parse("tomorrow", today=date(2025, 1, 1)) == date(2025, 1, 2)


def test_a_week():
    assert parser.parse("a week from today", today=date(2025, 1, 1)) == date(2025, 1, 8)


def test_yesterday():
    assert parser.parse("yesterday", today=date(2025, 1, 2)) == date(2025, 1, 1)


def test_a_date():
    assert parser.parse("January 1st, 2025") == date(2025, 1, 1)


def test_one_month():
    assert parser.parse("one month after January 1st, 2025") == date(2025, 2, 1)


def test_in_3_days():
    assert parser.parse("in 3 days", today=date(2025, 1, 1)) == date(2025, 1, 4)


def test_five_days_before_dec_31():
    assert parser.parse("5 days before December 1st, 2025") == date(2025, 11, 26)


def test_next_tuesday():
    assert parser.parse("Next Tuesday", today=date(2025, 1, 1)) == date(2025, 1, 7)


def test_two_weeks_from_tomorrow():
    assert parser.parse("two weeks from tomorrow", today=date(2025, 1, 1)) == date(
        2025, 1, 16
    )


def test_one_year_and_2_months_after_yesterday():
    assert parser.parse(
        "1 year and 2 months after yesterday", today=date(2025, 1, 2)
    ) == date(2026, 3, 1)


def test_month_end_clamp_non_leap():
    assert parser.parse("1 month after January 31st, 2025") == date(2025, 2, 28)


def test_month_end_clamp_leap():
    assert parser.parse("1 month after January 31st, 2024") == date(2024, 2, 29)


def test_month_before_clamp():
    assert parser.parse("1 month before March 31st, 2025") == date(2025, 2, 28)


def test_next_monday_from_monday():
    assert parser.parse("Next Monday", today=date(2025, 1, 6)) == date(2025, 1, 13)


def test_next_friday():
    assert parser.parse("Next Friday", today=date(2025, 1, 1)) == date(2025, 1, 3)


def test_singular_unit():
    assert parser.parse("in 1 day", today=date(2025, 1, 1)) == date(2025, 1, 2)


def test_today_keyword():
    assert parser.parse("today", today=date(2025, 1, 5)) == date(2025, 1, 5)


def test_compound_offset():
    assert parser.parse(
        "2 weeks and 3 days from today", today=date(2025, 1, 1)
    ) == date(2025, 1, 18)


def test_year_before():
    assert parser.parse("1 year before January 1st, 2025") == date(2024, 1, 1)


def test_unparseable_empty():
    import pytest
    with pytest.raises(ValueError):
        parser.parse("")


def test_unparseable_garbage():
    import pytest
    with pytest.raises(ValueError):
        parser.parse("some garbage text")
