from datetime import datetime

import pytest
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta, SA, MO, SU

from nfcclient.calendar import Calendar


@pytest.mark.asyncio
def test_operating_on_holiday_without_holiday(event_loop):
    e = easter(datetime.now().year + 1) + relativedelta(days=+1)
    d = datetime(year=e.year, month=e.month, day=e.day)
    c = Calendar()
    assert event_loop.run_until_complete(c.is_operating(d)) is True


@pytest.mark.asyncio
def test_operating_on_holiday(event_loop):
    e = easter(datetime.now().year + 1) + relativedelta(days=+1)
    d = datetime(year=e.year, month=e.month, day=e.day)
    c = Calendar(holidays=[d])
    assert event_loop.run_until_complete(c.is_operating(d)) is False


@pytest.mark.asyncio
def test_operating_on_working_weekend(event_loop):
    d1 = datetime.now() + relativedelta(weekday=SA, hour=12)
    d2 = datetime.now() + relativedelta(weekday=SU, hour=12)
    c = Calendar(operating_weekends=True)
    assert event_loop.run_until_complete(c.is_operating(d1)) is True
    assert event_loop.run_until_complete(c.is_operating(d2)) is True


@pytest.mark.asyncio
def test_operating_on_default_weekend(event_loop):
    d1 = datetime.now() + relativedelta(weekday=SA, hour=12)
    d2 = datetime.now() + relativedelta(weekday=SU, hour=12)
    c = Calendar()
    assert event_loop.run_until_complete(c.is_operating(d1)) is False
    assert event_loop.run_until_complete(c.is_operating(d2)) is False


@pytest.mark.asyncio
def test_idle_on_idle_weekend(event_loop):
    d1 = datetime.now() + relativedelta(weekday=SA, hour=12)
    d2 = datetime.now() + relativedelta(weekday=SU, hour=12)
    c = Calendar(operating_weekends=False)
    assert event_loop.run_until_complete(c.is_operating(d1)) is False
    assert event_loop.run_until_complete(c.is_operating(d2)) is False


@pytest.mark.asyncio
def test_operating_without_working_hours(event_loop):
    d = datetime.now() + relativedelta(weekday=MO, hour=12)
    c = Calendar()
    assert event_loop.run_until_complete(c.is_operating(d)) is True


@pytest.mark.asyncio
def test_operating_on_working_hours(event_loop):
    d1 = datetime.now() + relativedelta(weekday=MO, hour=6)
    d2 = datetime.now() + relativedelta(weekday=MO, hour=12)
    d3 = datetime.now() + relativedelta(weekday=MO, hour=20)
    c = Calendar(
        start_working_hour=8,
        end_working_hour=16,
    )
    assert event_loop.run_until_complete(c.is_operating(d1)) is False
    assert event_loop.run_until_complete(c.is_operating(d2)) is True
    assert event_loop.run_until_complete(c.is_operating(d3)) is False


@pytest.mark.asyncio
def test_operating_on_working_hours_only_start(event_loop):
    d1 = datetime.now() + relativedelta(weekday=MO, hour=6)
    d2 = datetime.now() + relativedelta(weekday=MO, hour=12)
    c = Calendar(
        start_working_hour=8,
    )
    assert event_loop.run_until_complete(c.is_operating(d1)) is False
    assert event_loop.run_until_complete(c.is_operating(d2)) is True


@pytest.mark.asyncio
def test_operating_on_working_hours_only_end(event_loop):
    d1 = datetime.now() + relativedelta(weekday=MO, hour=12)
    d2 = datetime.now() + relativedelta(weekday=MO, hour=20)
    c = Calendar(
        end_working_hour=16,
    )
    assert event_loop.run_until_complete(c.is_operating(d1)) is True
    assert event_loop.run_until_complete(c.is_operating(d2)) is False
