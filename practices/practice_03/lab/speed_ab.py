"""Run A/B speed checks for OpenCode agents on question #4.
Standard library only. Measures wall time per run and saves JSONL outputs and metrics.

Note: decode_tokens_per_second is not available from OpenCode JSONL events; set to null.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path


QUESTION = "Какая CI-система запускает тесты? Если сведений нет, скажи об этом."


def run_once(agent: str, out_jsonl: Path) -> dict:
    env = os.environ.copy()
    # Disable external provider; keep ollama
    env["OPENCODE_CONFIG_CONTENT"] = json.dumps({"disabled_providers": ["vsellm"]}, ensure_ascii=False)
    cmd = [
        "opencode",
        "run",
        "--pure",
        "--dir",
        "demo",
        "--agent",
        agent,
        "--model",
        "ollama/itmo-agent",
        "--format",
        "json",
        QUESTION,
    ]
    started = time.perf_counter()
    with out_jsonl.open("xb") as f:
        # Capture stdout to file directly to avoid buffering overhead
        proc = subprocess.run(cmd, env=env, cwd=Path(__file__).parent, stdout=f, stderr=subprocess.PIPE)
    wall = time.perf_counter() - started
    return {
        "agent": agent,
        "question": QUESTION,
        "wall_seconds": wall,
        "decode_tokens_per_second": None,
        "returncode": proc.returncode,
        "stderr": proc.stderr.decode(errors="replace"),
        "output_file": str(out_jsonl),
    }


def median(values):
    vs = sorted(values)
    n = len(vs)
    if n == 0:
        return None
    mid = n // 2
    if n % 2 == 1:
        return vs[mid]
    return (vs[mid - 1] + vs[mid]) / 2.0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--agents", nargs=2, default=["local-guide-A", "local-guide-B"], help="Two agent names A and B")
    p.add_argument("--out", default="results/homework-speed", help="Output directory")
    p.add_argument("--warmups", type=int, default=1)
    p.add_argument("--runs", type=int, default=3)
    args = p.parse_args()

    root = Path(__file__).parent
    out_dir = root / args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = {"question": QUESTION, "agents": {}, "note": "decode_tokens_per_second is not available for OpenCode sessions"}

    for agent in args.agents:
        agent_key = agent
        # warmups
        warm_metrics = []
        for i in range(args.warmups):
            out_jsonl = out_dir / f"warm-{agent}-{i+1}.jsonl"
            m = run_once(agent, out_jsonl)
            warm_metrics.append(m)
            # save metrics sidecar
            with (out_dir / f"warm-{agent}-{i+1}-metrics.json").open("x", encoding="utf-8") as mf:
                json.dump(m, mf, ensure_ascii=False, indent=2)

        # measured runs
        run_metrics = []
        for i in range(args.runs):
            out_jsonl = out_dir / f"{agent}-{i+1}.jsonl"
            m = run_once(agent, out_jsonl)
            run_metrics.append(m)
            with (out_dir / f"{agent}-{i+1}-metrics.json").open("x", encoding="utf-8") as mf:
                json.dump(m, mf, ensure_ascii=False, indent=2)

        walls = [m["wall_seconds"] for m in run_metrics if m.get("returncode") == 0]
        summary["agents"][agent_key] = {
            "runs": len(run_metrics),
            "ok_runs": len(walls),
            "median_wall_seconds": median(walls),
            "files": {
                "warm": [str(out_dir / f"warm-{agent}-{i+1}.jsonl") for i in range(args.warmups)],
                "runs": [str(out_dir / f"{agent}-{i+1}.jsonl") for i in range(args.runs)],
            },
        }

    with (out_dir / "summary.json").open("w", encoding="utf-8") as sf:
        json.dump(summary, sf, ensure_ascii=False, indent=2)
    print("Saved:", out_dir / "summary.json")


if __name__ == "__main__":
    sys.exit(main())
