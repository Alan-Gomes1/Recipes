import logging


_logger = logging.getLogger("recipes")


def logger(levelname: str, extra: dict, message: str = ""):
    if levelname not in logging._nameToLevel:
        raise ValueError(f"Nível de logging inválido: {levelname}")
    level = logging.getLevelName(levelname)
    _logger.log(level, message, extra=extra)
