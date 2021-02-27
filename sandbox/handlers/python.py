import os
import subprocess
from threading import Timer

from django.conf import settings

from .base import BaseHandler


class PythonHandler(BaseHandler):
    """
    Handler class for handling python3 code
    """

    FOLDER = "python"
    SUFFIX = ".py"

    @staticmethod
    def __generate_filename(suffix: str):
        from datetime import datetime

        return datetime.utcnow().strftime("%Y%m%d-%H%M%S") + suffix

    def __init__(self, userid: str, timeout: int):
        self.USERID = userid
        filename = self.__generate_filename(self.SUFFIX)
        super().__init__(filename, timeout)

    def __write__(self, code: str):
        with open(self.path, "w+") as f:
            f.write(code)

    def __run__(self):
        super().__run__()
        # "cd", self.dir, "&&",
        cmd = ["python3", self.path]
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            user=settings.RESTRICTED_USER,
        )
        try:
            output, err = proc.communicate(timeout=self.timeout)
        except subprocess.TimeoutExpired as e:
            proc.kill()
            output = ""
            err = str(e)

        return output, err

    def execute(self, code: str):
        """
        Method to be called for executing codes and returning the id of the celery process
        """
        self.__write__(code)
        output, err = self.__run__()
        self.__cleanup__()

        return output, err