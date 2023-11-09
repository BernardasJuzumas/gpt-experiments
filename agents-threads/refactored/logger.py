import logging
from config import DEBUG

class Logger:
    def __init__(self, name, level=logging.INFO, log_file='run.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.log_file = log_file
        self._setup_file_handler()
        if DEBUG:
            self._setup_console_handler()

    def _setup_console_handler(self):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def _setup_file_handler(self):
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)
    
    def info(self, message):
        self.logger.info(message)
    
    def error(self, message):
        self.logger.error(message)
    
    # Add more logging levels if needed