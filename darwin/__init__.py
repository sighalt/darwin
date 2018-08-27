import logging
from .evolution import Environment

logging.basicConfig(format="%(levelname)s %(name)s %(msg)s",
                    level=logging.INFO)


__all__ = ["Environment"]
