import logging
import sys
import os

class Logger:
    def __init__(self, name, log_level=logging.INFO, log_file=None):
        """
        初始化日志记录器。

        :param name: 日志记录器的名称
        :param log_level: 日志级别，默认为 INFO
        :param log_file: 日志文件名，如果为 None，则只输出到终端
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # 日志格式
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # 输出到终端
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        # 输出到文件（如果指定了日志文件名）
        if log_file:
            # 获取项目根目录
            root_dir = os.path.dirname(os.path.abspath(__file__))
            # 创建 log 文件夹（如果不存在）
            log_dir = os.path.join(root_dir, "log")
            os.makedirs(log_dir, exist_ok=True)
            # 拼接日志文件路径
            log_path = os.path.join(log_dir, log_file)
            # 创建文件处理器
            file_handler = logging.FileHandler(log_path)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def info(self, message):
        """记录 INFO 级别的日志"""
        self.logger.info(message)

    def warning(self, message):
        """记录 WARNING 级别的日志"""
        self.logger.warning(message)

    def error(self, message):
        """记录 ERROR 级别的日志"""
        self.logger.error(message)
        self.logger.error(message)

logger = Logger("Server").logger