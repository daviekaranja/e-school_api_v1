import logging


class MyLogger:
    name: str
    separator: str

    def __init__(self, name: str, separator: str = '\t'):
        self.name = name
        self.separator = separator

    def to_console(self, message: str):
        logger = logging.getLogger(self.name)
        return logger.warning(message)

    def formatter(self):
        format = "[%(levelname)s]"


log = MyLogger(name=__name__)

log.to_console("this is a message")


class Person:
    name: str
    age: int
    description: str

    def __init__(self, name, age, description):
        self.name = name
        self.age = age
        self.description = description
