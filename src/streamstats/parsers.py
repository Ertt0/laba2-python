import csv

from pydantic import ValidationError

from streamstats.errors import (
    InvalidEvent,
    InvalidTimestamp,
)
from streamstats.models import Event


def mkerror(exc, file, num):
    prob = False
    for er in exc.errors():
        if "timestamp" in er["loc"]:
            prob = True
    if prob:
        return InvalidTimestamp("Неверная временная метка", file, num)
    return InvalidEvent("Неверное событие", file, num)  

def jsonl_parser(file, invalid=None):
    with open(file, "r", encoding="utf-8") as f:
        for num, line in enumerate(f, start=1):
            line = line.strip()
            if line == "":
                continue
            try:
                event = Event.model_validate_json(line)
            except ValidationError as exc:
                error = mkerror(exc, file, num)
                if invalid is None:
                    raise error from exc
                invalid(error)
                continue
            yield event

def csv_parser(file, invalid=None):
    with open(file, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            num = reader.line_num
            try:
                event = Event.model_validate(row)
            except ValidationError as exc:
                error = mkerror(exc, file, num)
                if invalid is None:
                    raise error from exc
                invalid(error)
                continue
            yield event  