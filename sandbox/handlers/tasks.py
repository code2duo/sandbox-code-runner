import os
import subprocess

import resource
from celery import Task, current_app
from django.conf import settings

from code_runner.celery import app


class ExecuteTask(Task):
    """
    Task Class to execute codes
    """

    name = "execute_code"
    ignore_result = True

    def __cleanup__(self, path: str):
        os.remove(path)

    def run(self, cmd: list, timeout: int, path: str, *args, **kwargs):
        print("hi")
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            user=settings.RESTRICTED_USER,
        )

        try:
            usage_start = resource.getrusage(resource.RUSAGE_CHILDREN)
            output, err = proc.communicate(timeout=timeout)
            usage_end = resource.getrusage(resource.RUSAGE_CHILDREN)
            exec_time = usage_end.ru_utime - usage_start.ru_utime
        except subprocess.TimeoutExpired:
            proc.kill()
            output = ""
            err = "TLE"
            exec_time = None

        self.__cleanup__(path)


current_app.tasks.register(ExecuteTask())
