import os

from sandbox.tasks import async_execute
from .base import BaseHandler


class CHandler(BaseHandler):
    """
    Handler class for handling C code
    """

    FOLDER = "c"
    SUFFIX = ".c"

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
                "gcc",
                "-o",
                os.path.join(self.dir, "a.out"),
                self.path,
            ],
            [
                os.path.join(self.dir, "a.out"),
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
