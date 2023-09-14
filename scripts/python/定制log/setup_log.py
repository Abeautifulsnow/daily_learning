import datetime
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

# 项目根路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 日志文件路径
LOG_CONF_FILE = f"/tmp/logs/{os.path.basename(BASE_DIR)}"

# FORMATTER
SIMPLE_FORMATTER = (
    "\033[1;32m%(asctime)s\033[0m |\033[%(color)sm%(levelname)s\033[0m| \033[2m%(name)s\033[0m - %("
    "message)s"
)
VERBOSE_FORMATTER = "[%(asctime)s] |%(levelname)s| -Loc %(filename)s -Row %(lineno)d [%(name)s] - %(message)s"


COLORS = {
    logging.DEBUG: "1;47",  # White
    logging.INFO: "1;42",  # Green
    logging.WARNING: "1;43",  # Yellow
    logging.ERROR: "1;41",  # Red
    logging.CRITICAL: "1;45",  # Magenta
}


class ColoredLogRecord(logging.LogRecord):
    # Define a custom LogRecord class to add a color property based on log level
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = COLORS.get(self.levelno)
        self.levelname = f"{self.levelname:^7}"


class CustomRotatingHandler(RotatingFileHandler):
    # Define a custom RotatingFileHandler class to custom log filename.
    def doRollover(self):
        """Rewrite its implementation.
        Do a rollover, as described in __init__().
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        if self.backupCount > 0:
            name, ext = os.path.splitext(self.baseFilename)

            for i in range(self.backupCount - 1, 0, -1):
                sfn = self.rotation_filename("%s.%d%s" % (name, i, ext))
                dfn = self.rotation_filename("%s.%d%s" % (name, i + 1, ext))
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self.rotation_filename(name + ".1%s" % ext)
            if os.path.exists(dfn):
                os.remove(dfn)
            self.rotate(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()


def setup_logging(
    default_path=LOG_CONF_FILE,
    default_console_level=logging.DEBUG,
    default_file_level=logging.WARNING,
    file_maxsize=5 * 1024 * 1024,
    file_count=20,
):
    """
    配置项目日志信息
    Args:
        default_path: 日志文件默认路径
        default_console_level: 日志默认控制台等级
        default_file_level: 日志默认文件等级
        file_count: 文件个数, 当大于1的时候, 如果单个file已达到最大size, 就会创建file.1, file.2, file.3 等等文件
        file_maxsize: 单个日志文件的最大size
    """
    os.makedirs(LOG_CONF_FILE, exist_ok=True)
    today = datetime.datetime.now().strftime("%Y%m%d%H%M")
    log_file_name = f"{os.path.basename(BASE_DIR)}-{today}.log"
    track_log = os.path.join(default_path, log_file_name)

    # 日志文件
    file_handler = CustomRotatingHandler(
        filename=track_log,
        encoding="utf-8",
        maxBytes=file_maxsize,
        backupCount=file_count,
    )
    file_handler.setLevel(default_file_level)
    file_formatter = logging.Formatter(VERBOSE_FORMATTER)
    file_handler.setFormatter(file_formatter)

    # 控制台输出
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(default_console_level)
    console_formatter = logging.Formatter(SIMPLE_FORMATTER)
    console_handler.setFormatter(console_formatter)

    logging.setLogRecordFactory(ColoredLogRecord)
    logging.basicConfig(
        level=default_console_level, handlers=[console_handler, file_handler]
    )
