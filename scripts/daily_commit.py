#!/usr/bin/env python3
"""每日生成一批练习代码，分批提交，可选推送。

用法（在仓库任意位置执行都可以）：
    python scripts/daily_commit.py --status        查看今天是否已经提交过
    python scripts/daily_commit.py --dry-run       只打印将要生成的文件，不落盘
    python scripts/daily_commit.py                 生成并本地提交（不推送）
    python scripts/daily_commit.py --push          生成、提交并推送
    python scripts/daily_commit.py --push --force  忽略“今天已提交”检查

日期一律按 UTC 计算，因为 GitHub 贡献日历也按 UTC 归属。
"""

from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from snippets import make_pool, render  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO / "config.json"
STATE_PATH = REPO / "state.json"

DEFAULT_CONFIG = {
    "files_per_day": [4, 7],
    "commits_per_day": [1, 3],
    "languages": ["python", "javascript", "typescript", "go", "java", "c", "sql", "shell"],
    "skip_weekends": False,
    "git": {"name": "", "email": ""},
    "output_dir": "snippets",
}

MESSAGE_TEMPLATES = [
    "add {topic}",
    "practice: {topic}",
    "{topic}",
    "solve {topic}",
    "add {topic} snippet",
    "exercise: {topic}",
    "{date} practice",
]


# ---------------------------------------------------------------------------
# 基础设施
# ---------------------------------------------------------------------------


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if check and result.returncode != 0:
        message = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {message}")
    return result


def load_config() -> dict:
    config = json.loads(json.dumps(DEFAULT_CONFIG))
    if CONFIG_PATH.exists():
        config.update(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))
    return config


def load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {"last_run_date": None, "history": []}


def today_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _span(value, rnd: random.Random) -> int:
    """配置项允许写成 [min, max] 或单个数字。"""
    if isinstance(value, (list, tuple)) and len(value) == 2:
        return rnd.randint(int(value[0]), int(value[1]))
    return int(value)


# ---------------------------------------------------------------------------
# 生成
# ---------------------------------------------------------------------------


def build_files(config: dict, rnd: random.Random, date: str) -> list[tuple[str, str]]:
    """返回 [(相对路径, 内容)]。同一天内尽量不重复使用同一个模板。"""
    count = _span(config["files_per_day"], rnd)
    languages = list(config["languages"])
    if not languages:
        raise ValueError("config.languages is empty")

    year, month, day = date.split("-")
    folder = Path(config["output_dir"]) / year / month / day

    pool = make_pool(rnd, languages)
    files: list[tuple[str, str]] = []
    for index in range(1, count + 1):
        if not pool:
            pool = make_pool(rnd, languages)
        language, builder = pool.pop()
        _, stem, ext, code = render(rnd, language, builder)
        name = f"{index:02d}_{stem}.{ext}"
        files.append((str(folder / name).replace("\\", "/"), code))
    return files


def plan_commits(files: list[tuple[str, str]], count: int, rnd: random.Random) -> list[list[tuple[str, str]]]:
    """把文件分到若干次提交里，返回分组后的文件列表。"""
    shuffled = list(files)
    rnd.shuffle(shuffled)
    count = max(1, min(count, len(shuffled)))
    buckets: list[list[tuple[str, str]]] = [[] for _ in range(count)]
    for index, item in enumerate(shuffled):
        buckets[index % count].append(item)
    return buckets


def commit_message(stem_paths: list[str], date: str, rnd: random.Random) -> str:
    stems = []
    for path in stem_paths:
        name = Path(path).stem
        stems.append(name.split("_", 1)[1] if "_" in name else name)
    topic = ", ".join(dict.fromkeys(stems)) if stems else "practice"
    return rnd.choice(MESSAGE_TEMPLATES).format(topic=topic, date=date)


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description="每日生成练习代码并提交")
    parser.add_argument("--push", action="store_true", help="提交后推送到远端")
    parser.add_argument("--force", action="store_true", help="忽略“今天已提交”检查")
    parser.add_argument("--dry-run", action="store_true", help="只打印计划，不写文件不提交")
    parser.add_argument("--status", action="store_true", help="打印状态后退出")
    parser.add_argument("--no-pull", action="store_true", help="跳过提交前的 git pull")
    parser.add_argument("--seed", type=int, default=None, help="固定随机种子，便于复现")
    parser.add_argument("--files", type=int, default=None, help="覆盖今天的文件数量")
    parser.add_argument("--commits", type=int, default=None, help="覆盖今天的提交次数")
    args = parser.parse_args()

    config = load_config()
    state = load_state()
    date = today_utc()

    if args.status:
        print(f"repo        : {REPO}")
        print(f"today (utc) : {date}")
        print(f"last run    : {state.get('last_run_date')}")
        print(f"done today  : {state.get('last_run_date') == date}")
        return 0

    if state.get("last_run_date") == date and not args.force:
        print(f"[skip] already committed for {date}; use --force to override")
        return 0

    if config.get("skip_weekends") and datetime.strptime(date, "%Y-%m-%d").weekday() >= 5:
        print(f"[skip] {date} is a weekend and skip_weekends is enabled")
        return 0

    rnd = random.Random(args.seed)
    if args.files is not None:
        config["files_per_day"] = args.files
    if args.commits is not None:
        config["commits_per_day"] = args.commits

    files = build_files(config, rnd, date)
    if not files:
        print("[skip] files_per_day resolved to 0")
        return 0
    commit_count = _span(config["commits_per_day"], rnd)
    batches = plan_commits(files, commit_count, rnd)

    if args.dry_run:
        print(f"[dry-run] {date}: {len(files)} file(s) in {len(batches)} commit(s)")
        for index, batch in enumerate(batches, start=1):
            print(f"  commit {index}: {commit_message([p for p, _ in batch], date, rnd)}")
            for path, _ in batch:
                print(f"    {path}")
        return 0

    if not args.no_pull:
        pulled = git("pull", "--rebase", "--autostash", check=False)
        if pulled.returncode != 0:
            print("[warn] git pull failed, continuing with local state", file=sys.stderr)

    if git("status", "--porcelain").stdout.strip():
        print("[warn] working tree is dirty before generation", file=sys.stderr)

    # 写文件
    for path, content in files:
        target = REPO / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")

    # 记录状态，并把它并入最后一次提交
    history = state.get("history", [])
    history.append({"date": date, "files": len(files), "commits": len(batches)})
    state = {"last_run_date": date, "history": history[-60:]}
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    batches[-1].append((STATE_PATH.name, ""))

    identity = config.get("git", {})
    identity_args = []
    if identity.get("name"):
        identity_args += ["-c", f"user.name={identity['name']}"]
    if identity.get("email"):
        identity_args += ["-c", f"user.email={identity['email']}"]

    for index, batch in enumerate(batches, start=1):
        paths = [path for path, _ in batch]
        git("add", "--", *paths)
        message = commit_message([p for p in paths if p != STATE_PATH.name], date, rnd)
        git(*identity_args, "commit", "-m", message)
        print(f"[commit {index}/{len(batches)}] {message} ({len(paths)} file(s))")

    if args.push:
        branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        git("push", "origin", f"HEAD:refs/heads/{branch}")
        print(f"[push] {branch} -> origin")
    else:
        print("[done] committed locally; re-run with --push to publish")

    return 0


if __name__ == "__main__":
    sys.exit(main())
