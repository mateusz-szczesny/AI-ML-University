##########################################
###      Politechnika Łódzka 2020      ###
### Sieć Kohonena do kompresji obrazów ###
###      Mateusz Szczęsny - 233266     ###
###        Dawid Wójcik - 233271       ###
##########################################
import time
import os

DEFAULT_LOG_FILE_PREFIX = "log_"
DEFAULT_DELIMITER = ";"
DEFAULT_FILE_EXTENTION = ".csv"
DEFAULT_PATH = ""


class Logger:
    def __init__(
        self,
        *,
        prefix=DEFAULT_LOG_FILE_PREFIX,
        delimiter=DEFAULT_DELIMITER,
        file_extension=DEFAULT_FILE_EXTENTION,
        path=DEFAULT_PATH,
    ):
        self.prefix = prefix
        self.delimiter = delimiter
        self.file_extension = file_extension
        self.path = path
        self.__resolve_path()
        self.new_log_file()

    def __resolve_path(self):
        is_path_exists = os.path.exists(self.path)
        if not is_path_exists:
            os.mkdir(self.path)

    # Inicjalizacja pliku z wynikami
    def new_log_file(self):
        timestamp = int(time.time())
        self.file_name = f"{self.path}{self.prefix}{timestamp}{self.file_extension}"

    # Zapis argumentów do pliku
    def dump_to_file(self, *args):
        with open(self.file_name, "a+") as f:
            f.write(f"{self.delimiter.join([str(arg) for arg in args])}\n")
