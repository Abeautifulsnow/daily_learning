import logging
import os
import sys
from logging.handlers import RotatingFileHandler

# 项目根路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 日志文件路径
LOG_CONF_FILE = f"/tmp/logs/{os.path.basename(BASE_DIR)}/logs"

# FORMATTER
SIMPLE_FORMATTER = (
    "\033[2m%(asctime)s\033[0m [%(levelname)-5.5s] \033[2m[%(name)s]\033[0m %(message)s"
)
VERBOSE_FORMATTER = "\033[2m%(asctime)s\033[0m [%(levelname)-5.5s] -Loc \033[32m%(filename)s\033[0m -Row \033[31m%(lineno)d\033[0m \033[2m[%(name)s]\033[0m %(message)s"


def setup_logging(
    default_path=LOG_CONF_FILE,
    default_control_level=logging.DEBUG,
    default_file_level=logging.INFO,
    file_maxsize=20971520,
    file_count=20,
):
    """
    配置项目日志信息
    Args:
        default_path: 日志文件默认路径
        default_control_level: 日志默认控制台等级
        default_file_level: 日志默认文件等级
        file_count: 文件个数, 当大于1的时候, 如果单个file已达到最大size, 就会创建file.1, file.2, file.3 等等文件
        file_maxsize: 单个日志文件的最大size
    """
    os.makedirs(LOG_CONF_FILE, exist_ok=True)
    track_log = os.path.join(default_path, "track.log")

    # 日志文件
    file_handler = RotatingFileHandler(
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
    console_handler.setLevel(default_control_level)
    console_formatter = logging.Formatter(SIMPLE_FORMATTER)
    console_handler.setFormatter(console_formatter)

    logging.basicConfig(
        level=default_control_level, handlers=[file_handler, console_handler]
    )
