
from src.services.task_manager import TaskManager
from src.services.availability_manager import AvailabilityManager
from src.services.scheduling_engine import SchedulingEngine

from src.repositories.schedule_repository import ScheduleRepository
from src.services.schedule_assistant import ScheduleAssistant
from src.services.natural_language_parser import NaturalLanguageParser
from src.services.recommendation_engine import RecommendationEngine
from src.services.recommendation_engine import RecommendationEngine


class WorkforceService:

    def __init__(self):
        self.task_manager = TaskManager()
        self.availability_manager = AvailabilityManager()
        self.scheduling_engine = SchedulingEngine()
        self.schedule_repository = ScheduleRepository()
        self.schedule_assistant = ScheduleAssistant()
        self.natural_language_parser = NaturalLanguageParser()
        self.recommendation_engine = RecommendationEngine()

    # =========================
    # TASK MANAGEMENT
    # =========================

    def add_task(self, task_data):
        return self.task_manager.add_task(task_data)

    def get_tasks(self):
        return self.task_manager.get_all_tasks()

    # =========================
    # AVAILABILITY MANAGEMENT
    # =========================

    def add_availability(
        self,
        weekday,
        start_time,
        end_time
    ):
        return self.availability_manager.add_availability(
            weekday,
            start_time,
            end_time
        )

    def get_availabilities(self):
        return self.availability_manager.get_all_availabilities()

    # =========================
    # SCHEDULING
    # =========================

    def generate_schedule(self, start_date, end_date):

        tasks = self.task_manager.get_all_tasks()

        availabilities = (
            self.availability_manager.get_all_availabilities()
        )

        if not availabilities:
            raise ValueError(
                "Bạn chưa thiết lập thời gian rảnh."
            )

        result = self.scheduling_engine.generate_schedule(
            tasks,
            availabilities,
            start_date,
            end_date
        )

        self.schedule_repository.save_schedules(
            result["scheduled"]
        )

        return result

    # =========================
    # SCHEDULE REPOSITORY
    # =========================

    def get_saved_schedules(self):
        return self.schedule_repository.load_schedules()

    # =========================
    # AI ASSISTANT
    # =========================

    def analyze_schedule(
        self,
        result,
        start_date,
        end_date
    ):
        return self.schedule_assistant.analyze_schedule(
            result,
            self.availability_manager.get_all_availabilities(),
            start_date,
            end_date
        )

    def get_task_by_id(self, task_id):
        return self.task_manager.get_task_by_id(task_id)

    def update_task(self, task_id, updates):
        return self.task_manager.update_task(task_id, updates)

    def delete_task(self, task_id):
        return self.task_manager.delete_task(task_id)

    def complete_task(self, task_id):
        return self.task_manager.complete_task(task_id)

    def parse_and_add_task(self, user_request):
        task_data = self.natural_language_parser.parse(user_request)
        return self.task_manager.add_task(task_data)

    def generate_recommendations(self, result, start_date, end_date):
        return self.recommendation_engine.generate_recommendations(
            result,
            self.availability_manager.get_all_availabilities(),
            start_date,
            end_date
        )
