> 简介

- custom_log.py

该实例可在同一个项目下多个地方多次实例化引用，不会出现多文件被创建的情况。保证将log都输出到同一个日志文件中。既可以在 `console` 窗口滚动打印，也会在根目录下创建 `logs` 目录，并创建 `xxx.log` 文件。

- setup_log.py

该文件可在整个模块的入口处初始化 - `setup_logging()`，然后在模块下的其他文件内，只需要 `logger = logging.getLogger(__name__)` 使用即可。

- logs

logs目录内是配置文件的log日志使用方式，使用案例请参考demo目录。
