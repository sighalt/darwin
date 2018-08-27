import logging
from .evolution import Environment
from .exceptions import MaxFitnessReached
from .statistics import HallOfFame, PerformanceHistory

logging.basicConfig(format="%(levelname)s %(name)s %(msg)s",
                    level=logging.INFO)


__all__ = ["Environment", "MaxFitnessReached", "HallOfFame",
           "PerformanceHistory"]
