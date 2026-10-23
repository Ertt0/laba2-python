import logging
from enum import Enum
from typing import Annotated

import typer

from streamstats.analysis import analyze as analyze_events
from streamstats.errors import StreamStatsError
from streamstats.parsers import csv_parser, jsonl_parser
from streamstats.report import to_dict, to_report

logger = logging.getLogger(__name__)
app = typer.Typer()

class InputFormat(str, Enum):
    csv = "csv"
    jsonl = "jsonl"

@app.callback()
def main():
    pass

@app.command()
def analyze(
    inputs: Annotated[list[str], typer.Argument()],
    format: Annotated[InputFormat, typer.Option("--format")],
    output: Annotated[str, typer.Option("--output")],
    skip_invalid: Annotated[bool, typer.Option("--skip-invalid")] = False,
    ):
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s: %(message)s",
    )
    skipped = 0

    def on_invalid(error):
        nonlocal skipped
        skipped += 1
        logger.warning("%s", error)
    
    parser_func = (csv_parser if format == InputFormat.csv else jsonl_parser)

    def all_events():
        for f in inputs:
            yield from parser_func(f, invalid=on_invalid if skip_invalid else None)
    
    try:
        stats = analyze_events(all_events())
        stats.skip = skipped
        report = to_dict(stats)
        to_report(report, output)
    except StreamStatsError as exc:
        typer.echo(f"Ошибка: {exc}", err=True)
        raise typer.Exit(code=2) from exc

if __name__ == "__main__":
    app()