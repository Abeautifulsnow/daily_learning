# log_demo.py 文件

import logging

logger = logging.getLogger(__name__)  # 维护一个全局日志对象

logger.debug("debug log test")


def log_test1():
    logger.info("info log test")


def log_test2():
    try:
        a = 1 / 0
    except Exception as e:
        logger.error(e)


class LogDemo(object):
    @staticmethod
    def log_test():
        logger.warning("warning log test")
