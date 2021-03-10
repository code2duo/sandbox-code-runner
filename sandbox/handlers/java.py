from sandbox.tasks import async_execute
from .base import BaseHandler


class JavaHandler(BaseHandler):
    """
    Handler class for handling Java code
    """

    FOLDER = "java"
    SUFFIX = ".java"

    def __init__(self, userid: str, timeout: int):
        self.USERID = userid
        super().__init__(timeout)

    def __write__(self, code: str):
        with open(self.path, "w+") as f:
            f.write(code)

    def __run__(self):
        super().__run__()

        cmds = [
            [
                "javac",
                self.path,
            ],
            [
                "java",
                "-cp",
                self.dir,
                "Solution",
            ],
        ]

        res = async_execute.delay(cmds, self.timeout, self.dir, self.FOLDER)
        return res

    def execute(self, code: str):
        """
        Method to be called for executing codes and returning the id of the celery process
        """
        self.__write__(code)
        res = self.__run__()

        return res.id
