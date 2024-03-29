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

    def __init__(self, timeout: int):
        from datetime import datetime

        self.__check__()

        self.dir = os.path.join(
            "/tmp",
            self.FOLDER,
            self.USERID,
            "code",
            datetime.utcnow().strftime("%H%M%S"),
        )
        try:
            os.makedirs(self.dir)
        except FileExistsError:
            pass

        filename = self.__generate_filename()
        self.path = os.path.join(self.dir, filename)
        self.timeout = timeout

    def __run__(self):
        os.chdir(self.dir)

    def __generate_filename(self):
        from datetime import datetime

        return datetime.utcnow().strftime("%Y%m%d") + self.SUFFIX
