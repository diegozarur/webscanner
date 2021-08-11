from celery import current_app
from app.task.base_task import BaseTask
from app.views.scanning.scanner.service import Scanner


class Scanning(BaseTask):
    name = __name__

    def run(self, request_data):
        scanner = Scanner(**request_data)
        return scanner.doing()


current_app.register_task(Scanning)
