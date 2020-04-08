#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

def _search(files, suffix=None):
    for file in files:
        file = Path(file)
        if file.is_dir():
            for child in _search(file.iterdir(), ".dump-time-trace"):
                yield child
        elif suffix is None or file.suffix == suffix:
            yield file

def _merged_events(logs, earliest_beginning_of_time):
    for log in logs:
        local_beginning_of_time = log["beginningOfTime"]
        delta = local_beginning_of_time - earliest_beginning_of_time
        for event in log["traceEvents"]:
            if "ts" in event:
                event["ts"] += delta
            yield event


def merge(files):
    logs = [json.loads(file.read_bytes()) for file in _search(files)]
    earliest_beginning_of_time = min([log["beginningOfTime"] for log in logs])
    result = {
        "traceEvents": list(_merged_events(logs, earliest_beginning_of_time)),
        "beginningOfTime": earliest_beginning_of_time
    }
    return json.dumps(result)        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge multiple .dump-time-trace files into one file and preserve relative timing.")
    parser.add_argument("paths",
                        metavar="file",
                        nargs="+",
                        help="Paths to files to merge. If a directory is specified, it is searched recursively for .dump-time-trace files")
    args = parser.parse_args()
    print(merge(args.paths))
