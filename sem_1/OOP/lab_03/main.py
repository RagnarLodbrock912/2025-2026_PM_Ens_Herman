from abc import ABC, abstractmethod
from enum import Enum
import re
import socket
from ftplib import FTP
import os
import tempfile
from datetime import datetime


class LogLevel(Enum):
    WARN = "WARN"
    INFO = "INFO"
    ERROR = "ERROR"

#  LOG FILTER
class ILogFilter(ABC):
    @abstractmethod
    def match(self, log_level: LogLevel, text: str) -> bool:
        ...

class SimpleLogFilter(ILogFilter):
    def __init__(self, match_text: str) -> None:
        self.match_text = match_text

    def match(self, log_level: LogLevel, text: str) -> bool:
        return self.match_text in text

class ReLogFilter(ILogFilter):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def match(self, log_level: LogLevel, text: str) -> bool:
        return re.fullmatch(self.pattern, text)
    
class LevelFilter(ILogFilter):
    def __init__(self, log_level: LogLevel) -> None:
        self.log_level = log_level

    def match(self, log_level: LogLevel, text: str) -> bool:
        return self.log_level == log_level
    
# LOG HANDLER
class ILogHandler(ABC):
    @abstractmethod
    def handle(self, log_level: LogLevel, text: str) -> None:
        ...

class FileHandler(ILogHandler):
    def __init__(self, log_level: LogLevel, file_path: str) -> None:
        self.file_path = file_path

    def handle(self, text: str):
        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write(f"{text}\n")

class SocketHandler(ILogHandler):
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    def handle(self, log_level: LogLevel, text: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.host, self.port))
            client.sendall(text.encode('utf-8'))

class ConsoleHandler(ILogHandler):
    def handle(self, log_level: LogLevel, text: str):
        print(text)

class SyslogHandler(ILogHandler):
    def __init__(self, log_dir: str = "/var/log/myapp", app_name: str = "app") -> None:
            self.log_dir = log_dir
            self.app_name = app_name
            os.makedirs(log_dir, exist_ok=True)
            self.log_file = os.path.join(log_dir, f"{app_name}.log")

    def handle(self, log_level: LogLevel, text: str) -> None:
        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(text)

class FtpHandler(ILogHandler):
    def __init__(self, host: str, username: str, password: str) -> None:
        self.host = host
        self.username = username
        self.password = password

    def handle(self, log_level: LogLevel, text: str):
        with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as tmp:
            tmp.write(text)
            tmp.flush()
            tmp_name = tmp.name

        ftp = FTP(self.host)
        ftp.login(self.username, self.password)
        ftp.cwd("/logs")

        with open(tmp_name, "rb") as f:
            ftp.storbinary(f"STOR log_{os.path.basename(tmp_name)}.txt", f)

        ftp.quit()
        os.remove(tmp_name)

# LOG FORMATTER

class ILogFormatter(ABC):
    @abstractmethod
    def format(self, log_level: LogLevel, text: str) -> str:
        ...

class LevelAndTimeFormatter(ILogFormatter):
    def format(self, log_level: LogLevel, text: str) -> str:
        now = datetime.now()
        data = now.strftime("%Y.%m.%d %H:%M:%S")
        return f'[{log_level}] [data:{data}] {text}'
    
# LOGGER

class Logger():
    def __init__(self, log_filters: list[ILogFilter], log_handlers: list[ILogHandler], log_formatters: list[ILogFormatter]):
        self.log_filters = log_filters
        self.log_handlers = log_handlers
        self.log_formatters = log_formatters

    def log(self, log_level: LogLevel, text: str) -> None:
        if not all(filter.match(log_level, text) for filter in self.log_filters):
            return
        
        for formatter in self.log_formatters:
            text = formatter.format(log_level, text)

        for handler in self.log_handlers:
            handler.handle(text)

    def log_info(self, text: str) -> None:
        self.log(LogLevel.INFO, text)
    
    def log_warn(self, text: str) -> None:
        self.log(LogLevel.WARN, text)

    def log_error(self, text: str) -> None:
        self.log(LogLevel.ERROR, text)

    def add_log_filter(self, log_filter: ILogFilter) -> None:
        self.log_filters.append(log_filter)

    def add_log_formatter(self, log_formatter: ILogFormatter) -> None:
        self.log_formatters.append(log_formatter)

    def add_log_handler(self, log_handler: ILogHandler) -> None:
        self.log_handlers.append(log_handler)

    def remove_log_filter(self, log_filter: ILogFilter) -> None:
        self.log_filters.remove(log_filter)

    def remove_log_formatter(self, log_formatter: ILogFormatter) -> None:
        self.log_formatters.remove(log_formatter)

    def remove_log_handler(self, log_handler: ILogHandler) -> None:
        self.log_handlers.remove(log_handler)


# Фильтры
filters = [
    LevelFilter(LogLevel.WARN),        # только WARN
    SimpleLogFilter("disk"),           # только если есть "disk"
    ReLogFilter(r".*full.*")           # и содержит "full"
]

# Хэндлеры
handlers = [
    ConsoleHandler(),
    FileHandler("log_demo_extended.txt")
]

# Форматтер
formatters = [LevelAndTimeFormatter()]

# Logger
logger = Logger(filters, handlers, formatters)

# Тестовые логи
test_messages = [
    (LogLevel.INFO, "disk space ok"),            # не пройдет (INFO)
    (LogLevel.WARN, "disk almost full"),        # пройдет
    (LogLevel.WARN, "disk usage high"),         # не пройдет (нет "full")
    (LogLevel.WARN, "memory full"),             # не пройдет (нет "disk")
    (LogLevel.ERROR, "disk almost full"),       # не пройдет (ERROR)
    (LogLevel.WARN, "disk full backup"),        # пройдет
]

for level, msg in test_messages:
    logger.log(level, msg)
