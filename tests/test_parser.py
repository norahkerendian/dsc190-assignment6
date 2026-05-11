from datetime import date

from nldate import parser

def test_tomorrow():
    assert parser.parse("tomorrow", today=date(2025,1,1)) == date(2025,1,2)

def test_a_week():
    assert parser.parse("a week from today", today=date(2025,1,1)) == date(2025,1,8)

def test_yesterday():
    assert parser.parse("yesterday", today=date(2025,1,2)) == date(2025,1,1)

def test_a_date():
    assert parser.parse("January 1st, 2025") == date(2025,1,1)

def test_one_month():
    assert parser.parse("one month after January 1st, 2025") == date(2025,2,1)

def test_in_3_days():
    assert parser.parse("in 3 days", today=date(2025,1,1)) == date(2025,1,4)

def test_five_days_before_dec_31():
    assert parser.parse("5 days before December 1st, 2025") == date(2025, 11, 26)

def test_next_tuesday():
    assert parser.parse("Next Tuesday", today=date(2025,1,1)) == date(2025, 1,7)

def test_two_weeks_from_tomorrow():
    assert parser.parse("two weeks from tomorrow", today=date(2025,1,1)) == date(2025, 1, 16)

def test_one_year_and_2_months_after_yesterday():
    assert parser.parse("1 year and 2 months after yesterday", today=date(2025,1,2)) == date(2026,3,1)
