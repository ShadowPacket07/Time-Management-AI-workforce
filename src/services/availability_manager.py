
from src.models.availability import Availability
from src.repositories.availability_repository import (
    AvailabilityRepository
)


class AvailabilityManager:

    def __init__(self):
        self.repository = AvailabilityRepository()
        self.availabilities = (
            self.repository.load_availabilities()
        )

    def add_availability(
        self,
        weekday,
        start_time,
        end_time
    ):

        availability = Availability(
            weekday=weekday,
            start_time=start_time,
            end_time=end_time
        )

        for existing in self.availabilities:

            if existing.weekday != weekday:
                continue

            # Chuyển giờ HH:MM thành số phút
            existing_start = self._to_minutes(
                existing.start_time
            )
            existing_end = self._to_minutes(
                existing.end_time
            )

            new_start = self._to_minutes(start_time)
            new_end = self._to_minutes(end_time)

            if (
                new_start < existing_end
                and existing_start < new_end
            ):
                raise ValueError(
                    "Khoảng thời gian này bị trùng."
                )

        self.availabilities.append(availability)

        self.repository.save_availabilities(
            self.availabilities
        )

        return availability

    def get_all_availabilities(self):
        return self.availabilities.copy()

    def delete_availability(self, index):

        if index < 0 or index >= len(self.availabilities):
            return False

        self.availabilities.pop(index)

        self.repository.save_availabilities(
            self.availabilities
        )

        return True

    @staticmethod
    def _to_minutes(time_string):

        hours, minutes = map(
            int,
            time_string.split(":")
        )

        return hours * 60 + minutes
