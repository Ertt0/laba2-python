import pytest

from streamstats.analysis import analyze
from streamstats.errors import InvalidTimestamp
from streamstats.models import Event, Level
from streamstats.parsers import csv_parser, jsonl_parser


def test_analyze_counts_events():
    event1 = Event(
        timestamp="2077-12-01T15:00:00+04:00",
        level=Level.INFO,
        source="web",
        message="meooow"
    )

    event2 = Event(
        timestamp="1984-11-11T11:11:11Z",
        level=Level.ERROR,
        source="payment",
        message="rr"
    )

    events = [event1, event2]
    stats = analyze(events)

    assert stats.total == 2
    assert stats.levels[Level.INFO] == 1
    assert stats.levels[Level.ERROR] == 1
    assert stats.sources["web"] == 1
    assert stats.sources["payment"] == 1

def test_empty_jsonl():
    with open("empty.jsonl", "w", encoding="utf-8"):
        pass
    events = list(jsonl_parser("empty.jsonl"))

    assert len(events) == 0

def test_jsonl_parser_events():
    with open("events.jsonl", "w", encoding="utf-8") as file:
        file.write(
            '{"timestamp":"2052-10-10T08:00:00+01:00",'
            '"level":"ERROR","source":"auth","message":"ww"}\n'
        )

    events = list(jsonl_parser("events.jsonl"))

    assert len(events) == 1
    assert events[0].source == "auth"
    assert events[0].message == "ww"

def test_csv_parser_events():
    with open("events.csv", "w", encoding="utf-8") as file:
        file.write(
        "timestamp,level,source,message\n"
        "2053-10-10T08:00:00+01:00,ERROR,auth,ww\n"
        )

    events = list(csv_parser("events.csv"))

    assert len(events) == 1
    assert events[0].level == Level.ERROR

def test_invalid_timestamp_error():
    with open("err.jsonl", "w", encoding="utf-8") as file:
        file.write(
            '{"timestamp":"no",'
            '"level":"INFO","source":"auth","message":"ww"}\n'
        )

    with pytest.raises(InvalidTimestamp):
        list(jsonl_parser("err.jsonl"))
    
def test_skip_invalid_timestamp():
    with open("skip_err.jsonl", "w", encoding="utf-8") as file:
        file.write(
            '{"timestamp":"no",'
            '"level":"INFO","source":"auth","message":"ww"}\n'
        )

    errors = []
    events = list(jsonl_parser("skip_err.jsonl", invalid=errors.append))

    assert len(events) == 0
    assert len(errors) == 1

def test_combine_files():
    with open("file1.jsonl", "w", encoding="utf-8") as file1:
        file1.write(
            '{"timestamp":"2001-09-10T00:00:01Z",'
            '"level":"ERROR","source":"payment","message":"q"}\n'
        )


    with open("file2.jsonl", "w", encoding="utf-8") as file2:
        file2.write(
            '{"timestamp":"2022-02-22T00:00:01Z",'
            '"level":"ERROR","source":"auth","message":"f"}\n'
        )

    events1 = list(jsonl_parser("file1.jsonl"))
    events2 = list(jsonl_parser("file2.jsonl"))
    events = events1 + events2
    stats = analyze(events)

    assert stats.total == 2
    assert stats.sources["payment"] == 1
    assert stats.sources["auth"] == 1