from .base import BaseHandler
from .tasks import ExecuteTask


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
        task = ExecuteTask()
        res = task.delay(
            cmd=cmd, timeout=self.timeout, path=self.path, queue="code_runner"
        )
        return res

    def execute(self, code: str):
        """
        Method to be called for executing codes and returning the id of the celery process
        """
        self.__write__(code)
        res = self.__run__()

        return res.id
