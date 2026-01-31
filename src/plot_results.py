#!/usr/bin/env python3
"""Plot helper for Collatz analysis.

Reads the JSON output of src/analyze.py and emits PNGs.

Usage:
  python3 plot_results.py --in collatz_results.json --outdir ../data/plots
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ModuleNotFoundError:  # optional
    matplotlib = None
    plt = None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    data = json.loads(Path(args.inp).read_text())
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    limit = data.get("limit")

    # Always export CSVs (lightweight, no extra deps)
    hist = data.get("stopping_time_histogram", [])
    (outdir / "stopping_time_histogram.csv").write_text(
        "steps,count\n" + "\n".join(f"{i},{c}" for i, c in enumerate(hist) if c)
    )

    mod12 = sorted(data.get("mod12", []), key=lambda r: r["mod"])
    (outdir / "mod12.csv").write_text(
        "mod,count,avg_stopping_time\n" + "\n".join(
            f"{r['mod']},{r['count']},{r['avg_stopping_time']}" for r in mod12
        )
    )

    pc = data.get("popcount", [])
    (outdir / "popcount.csv").write_text(
        "popcount,count,avg_stopping_time\n" + "\n".join(
            f"{r['popcount']},{r['count']},{r['avg_stopping_time']}" for r in pc
        )
    )

    if plt is None:
        print(f"matplotlib not installed; wrote CSVs to: {outdir}")
        return

    # 1) stopping time histogram
    xs = list(range(len(hist)))
    ys = hist
    plt.figure(figsize=(10, 5))
    plt.plot(xs, ys, linewidth=1)
    plt.title(f"Stopping time histogram (n=1..{limit:,})")
    plt.xlabel("stopping time (steps)")
    plt.ylabel("count")
    plt.yscale("log")
    plt.tight_layout()
    plt.savefig(outdir / "stopping_time_histogram.png", dpi=160)
    plt.close()

    # 2) mod 12 avg stopping time
    plt.figure(figsize=(10, 4))
    plt.bar([r["mod"] for r in mod12], [r["avg_stopping_time"] for r in mod12])
    plt.title("Avg stopping time by n mod 12")
    plt.xlabel("n mod 12")
    plt.ylabel("avg stopping time")
    plt.tight_layout()
    plt.savefig(outdir / "mod12_avg.png", dpi=160)
    plt.close()

    # 3) popcount vs avg stopping time
    xs = [r["popcount"] for r in pc]
    ys = [r["avg_stopping_time"] for r in pc]
    sizes = [max(10, (r["count"] ** 0.5)) for r in pc]
    plt.figure(figsize=(10, 5))
    plt.scatter(xs, ys, s=sizes, alpha=0.6)
    plt.title("Avg stopping time by popcount (marker size ~ sqrt(count))")
    plt.xlabel("popcount (number of 1-bits)")
    plt.ylabel("avg stopping time")
    plt.tight_layout()
    plt.savefig(outdir / "popcount_avg.png", dpi=160)
    plt.close()

    print(f"Wrote plots+CSVs to: {outdir}")


if __name__ == "__main__":
    main()
