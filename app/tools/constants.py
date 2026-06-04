from enum import Enum


class AggregateMetric(str, Enum):

    COUNT = "count"
    AVG = "avg"
    MIN = "min"
    MAX = "max"
    SUM = "sum"