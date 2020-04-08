# merge_trace_events

This is a Python 3 script that takes multiple files in Chrome Trace Event format
and merges them while preserving relative timing.

A producer of those files must include the `beginningOfTime` key in the JSON,
whose value should be equal to UNIX time of the zero timestamp.

## Usage

You can enumerate the files that you want to merge:

```
$ ./merge_trace_events file1.json file2.json file3.json ...
```

Or you can specify directories, which will be searched recursively for files
with suffix `.dump-time-trace`:

```
$ ./merge_trace_events . ../hello/
```
