import logging


class CustomLogger:
    def _get_handlers(self) -> list[logging.Handler]:
        formatter = logging.Formatter(
            fmt="[%(asctime)s] %(levelname)s : [%(name)s] : %(message)s",
            datefmt="%Y-%M-%d %H:%M:%S",
        )
        handler_file = logging.FileHandler(filename='tic-tac-toe.log', mode='w')
        handler_file.setLevel(logging.DEBUG)
        handler_file.setFormatter(formatter)
        handler_stream = logging.StreamHandler()
        handler_stream.setLevel(logging.DEBUG)
        handler_stream.setFormatter(formatter)
        return [handler_file, handler_stream]

    def create_logger(self, name: str) -> logging.Logger:
        logging.basicConfig(handlers=self._get_handlers(), level=logging.DEBUG)
        logging.getLogger('httpx').setLevel(logging.WARNING)
        logger = logging.getLogger(name)
        return logger
