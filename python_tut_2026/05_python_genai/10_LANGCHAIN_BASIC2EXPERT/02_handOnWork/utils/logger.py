import logging

def get_logger(name: str = __name__):
    """
    Create and return a logger obj
    """
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s - %(levelname)s - %(message)s"
    )

    return logging.getLogger(name)