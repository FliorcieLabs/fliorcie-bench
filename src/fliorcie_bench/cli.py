from __future__ import annotations

import argparse
from pathlib import Path

from .core import read_record, write_record
from .render import render_markdown
from .runner import run_demo_benchmark


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="fl-bench")
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo", help="write a demo local benchmark record")
    demo.add_argument("--iterations", type=int, default=100)
    demo.add_argument("--output", type=Path, required=True)
    render = sub.add_parser("render", help="render a JSON record to Markdown")
    render.add_argument("record", type=Path)
    render.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    if args.command == "demo":
        write_record(args.output, run_demo_benchmark(args.iterations))
        print(str(args.output))
        return 0
    if args.command == "render":
        args.output.write_text(render_markdown(read_record(args.record)), encoding="utf-8")
        print(str(args.output))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

