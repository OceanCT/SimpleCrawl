class Logger:
    def __init__(self, log_file_name='crawl.log') -> None:
        self.log_file_name = log_file_name
        self.log_file = open(log_file_name, "w")

    def log(self, message) -> None:
        self.log_file.write(message + "\n")
        self.log_file.flush()

    def close(self) -> None:
        self.log_file.close()
        self.log_file = None
        self.log_file_name = None
