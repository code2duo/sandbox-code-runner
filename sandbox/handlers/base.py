import os


class BaseHandler:
    """
    Base Handler (to be inherited by individual language handlers)
    """

    FOLDER = None
    USERID = None
    SUFFIX = None

    def __check__(self):
        """
        checks if all the necessary super class variables are initialized in sub-class or not
        """
        if self.FOLDER is None:
            raise ValueError(
                "super class variable FOLDER must be initialised in Sub Class"
            )
        if self.USERID is None:
            raise ValueError(
                "super class variable USERID must be initialised in Sub Class"
            )
        if self.SUFFIX is None:
            raise ValueError(
                "super class variable SUFFIX must be initialised in Sub Class"
            )

    def __init__(self, filename: str, timeout: int):
        self.__check__()

        self.dir = os.path.join("/tmp", self.FOLDER, self.USERID, "code")
        try:
            os.makedirs(self.dir)
        except FileExistsError:
            pass
        self.path = os.path.join(self.dir, filename)
        self.timeout = timeout

    def __run__(self):
        os.chdir(self.dir)
