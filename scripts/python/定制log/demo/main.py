import logging
import sys

sys.path.append("..")

from logs import setup_logging


def main():
    setup_logging()

    logger = logging.getLogger(__name__)
    logger.debug("debug log test")
    logger.info("info log test")
    logger.warning("warning log test")
    logger.error("error log test")

    # 日志在其他模块中使用演示
    import demo

    demo.log_test1()
    demo.log_test2()
    demo.LogDemo.log_test()


if __name__ == "__main__":
    main()
