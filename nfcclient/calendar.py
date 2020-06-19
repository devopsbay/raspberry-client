from datetime import datetime
from typing import List


class Calendar:
    def __init__(
            self,
            holidays: List[datetime] = None,
            operating_weekends: bool = False,
            start_working_hour: int = None,
            end_working_hour: int = None,
    ):
        if not holidays:
            holidays = []

        self.holidays = holidays
        self.operating_weekends = operating_weekends
        self.start_working_hour = start_working_hour
        self.end_working_hour = end_working_hour

    async def is_operating(self, d: datetime = None) -> bool:
        if not d:
            d = datetime.now()

        return all([
            await self.is_in_working_hours(d),
            await self.is_working_if_on_weekend(d),
            await self.is_outside_of_holidays(d),
        ])

    async def is_in_working_hours(self, d: datetime) -> bool:
        if not self.start_working_hour and not self.end_working_hour:
            return True

        if self.start_working_hour and d.hour < self.start_working_hour:
            return False

        if self.end_working_hour and d.hour > self.end_working_hour:
            return False

        return True

    async def is_working_if_on_weekend(self, d: datetime) -> bool:
        if d.isoweekday() > 5 and not self.operating_weekends:
            return False

        return True

    async def is_outside_of_holidays(self, d: datetime) -> bool:
        if d in self.holidays:
            return False

        return True
