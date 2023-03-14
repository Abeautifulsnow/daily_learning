import logging
import os
import time

# public variables
log_path = "./logs"
os.makedirs(log_path, exist_ok=True)


class Log:
    __instance = None
    __init_flag = False

    def __new__(cls, write_file: bool = False, file_name: str = None):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
            return cls.__instance
        else:
            return cls.__instance

    def __init__(self, write_file: bool = False, file_name: str = None):
        if not self.__init_flag:
            self.__init_flag = True
            self._write_file = write_file
            self.now = time.strftime("%Y%m%d-%H%M%S")

            if not file_name:
                self.log_name = os.path.join(log_path, f"{self.now}.log")
            else:
                self.log_name = os.path.join(log_path, f"{file_name}-{self.now}.log")
        else:
            pass

    def __printconsole(self, level: str, message: str):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(self.log_name, "a", encoding="utf-8")
        fh.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)

        formatter_fh = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        if level == "warning" or level == "error":
            formatter_sh = logging.Formatter("%(levelname)s - %(message)s")
        else:
            formatter_sh = logging.Formatter("%(message)s")

        if self._write_file:
            fh.setFormatter(formatter_fh)
            logger.addHandler(fh)

        sh.setFormatter(formatter_sh)
        logger.addHandler(sh)

        if level == "info":
            logger.info(message)
        elif level == "debug":
            logger.debug(message)
        elif level == "warning":
            logger.warn(message)
        elif level == "error":
            logger.error(message)

        logger.removeHandler(sh)
        logger.removeHandler(fh)

        fh.close()

    def debug(self, message: str):
        self.__printconsole("debug", message)

    def info(self, message: str):
        self.__printconsole("info", message)

    def warning(self, message: str):
        self.__printconsole("warning", message)

    def error(self, message: str):
        self.__printconsole("error", message)


# get instance of class Log
log_ins = Log()
