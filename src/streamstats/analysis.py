from collections import Counter
from dataclasses import dataclass
from datetime import datetime

from streamstats.models import Level


@dataclass
class Statistics:
    total: int
    levels: Counter
    sources: Counter
    errors_sources: Counter
    min_time: datetime | None
    max_time: datetime | None
    skip: int = 0

def analyze(events, skip: int = 0) -> Statistics:
    stats = Statistics(
        total=0,
        levels=Counter(),
        sources=Counter(),
        errors_sources=Counter(),
        min_time=None,
        max_time=None,
        skip=skip,
    )

    for event in events:
        stats.total += 1
        stats.levels[event.level] += 1
        stats.sources[event.source] += 1
        if event.level == Level.ERROR  or event.level == Level.CRITICAL:
            stats.errors_sources[event.source] += 1
        if stats.min_time is None or event.timestamp < stats.min_time:
            stats.min_time = event.timestamp
        if stats.max_time is None or event.timestamp > stats.max_time:
            stats.max_time = event.timestamp
 
    return stats