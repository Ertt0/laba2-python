import json

from streamstats.analysis import Statistics


def to_dict(stats: Statistics) -> dict:
    return {
        "total": stats.total,
        "levels": {
            level.value: count
            for level, count in stats.levels.items()
        },
        "sources": dict(stats.sources),
        "top_error_sources": stats.errors_sources.most_common(5),
        "min_time": (
            stats.min_time.isoformat()
            if stats.min_time is not None
            else None
        ),
        "max_time": (
            stats.max_time.isoformat()
            if stats.max_time is not None
            else None
        ),
        "skip": stats.skip,
    }

def to_report(report: dict, output_file: str) -> None:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
