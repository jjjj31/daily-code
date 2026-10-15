#!/usr/bin/env python3
"""抽查模板质量：批量生成片段，用本机可用的工具链做真实语法检查。

只依赖标准库。缺少对应工具链的语言会跳过并明确标注。

用法：
    python scripts/check_templates.py
    python scripts/check_templates.py --rounds 100
"""

from __future__ import annotations

import argparse
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from snippets import TEMPLATES, generate_one  # noqa: E402


def which(name: str) -> str | None:
    path = shutil.which(name)
    if path is None:
        return None
    # Windows 上 System32\\bash.exe 是 WSL 入口，会把 C:\\... 路径吃掉，跳过。
    if name == "bash" and "system32" in path.lower():
        return None
    return path


def run(command: list[str]) -> str | None:
    try:
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    except OSError as exc:
        return f"cannot run {command[0]}: {exc}"
    if result.returncode != 0:
        return (result.stderr or result.stdout or "").strip()[:300]
    return None


def check_language(language: str, folder: Path) -> tuple[str, str | None]:
    """返回 (状态, 问题描述)。状态为 ok / skipped / failed。"""
    files = sorted(path for path in folder.rglob("*") if path.is_file())
    if not files:
        return "skipped", "no files generated"
    paths = [str(path) for path in files]

    if language == "python":
        for path in files:
            try:
                compile(path.read_text(encoding="utf-8"), str(path), "exec")
            except SyntaxError as exc:
                return "failed", f"{path.name}: {exc}"
        return "ok", None

    if language == "javascript":
        node = which("node")
        if not node:
            return "skipped", "node not found"
        for path in files:
            problem = run([node, "--check", str(path)])
            if problem:
                return "failed", f"{path.name}: {problem}"
        return "ok", None

    if language == "typescript":
        npx = which("npx")
        if not npx:
            return "skipped", "npx not found"
        problem = run([
            npx, "--yes", "-p", "typescript", "tsc", "--noEmit", "--strict",
            "--target", "es2020", "--lib", "es2020,dom", *paths,
        ])
        return ("failed", problem) if problem else ("ok", None)

    if language == "java":
        javac = which("javac")
        if not javac:
            return "skipped", "javac not found"
        # 默认包里同名 public 类不能同时编译，逐个来
        for path in files:
            problem = run([
                javac, "-J-Duser.language=en", "-J-Duser.country=US",
                "-d", str(folder / "_classes"), str(path),
            ])
            if problem:
                return "failed", f"{path.name}: {problem}"
        return "ok", None

    if language == "c":
        gcc = which("gcc")
        if not gcc:
            return "skipped", "gcc not found"
        problem = run([gcc, "-fsyntax-only", *paths])
        return ("failed", problem) if problem else ("ok", None)

    if language == "shell":
        bash = which("bash")
        if not bash:
            return "skipped", "bash not found"
        for path in files:
            problem = run([bash, "-n", str(path)])
            if problem:
                return "failed", f"{path.name}: {problem}"
        return "ok", None

    return "skipped", "no checker for this language"


def main() -> int:
    parser = argparse.ArgumentParser(description="模板自检")
    parser.add_argument("--rounds", type=int, default=30, help="每种语言生成多少个样本（默认 30）")
    args = parser.parse_args()

    failures = 0
    with tempfile.TemporaryDirectory(prefix="daily-code-check-") as tmp:
        root = Path(tmp)
        for language, spec in TEMPLATES.items():
            folder = root / language
            folder.mkdir(parents=True, exist_ok=True)
            for index in range(args.rounds):
                rnd = random.Random(f"{language}-{index}")
                _, stem, ext, code = generate_one(rnd, language)
                if language == "java":
                    # javac 要求文件名与 public 类名一致，用子目录区分不同轮次
                    target = folder / f"r{index:03d}" / f"{stem}.java"
                else:
                    target = folder / f"{index:03d}_{stem}.{ext}"
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(code, encoding="utf-8", newline="\n")

            sample_count = len([p for p in folder.rglob("*") if p.is_file()])
            status, detail = check_language(language, folder)
            mark = {"ok": "ok     ", "skipped": "skipped", "failed": "FAILED "}[status]
            print(f"{mark} {language:<12} ({sample_count} samples)"
                  + (f" - {detail}" if detail else ""))
            if status == "failed":
                failures += 1

    print(f"\n{'all checks passed' if failures == 0 else f'{failures} language(s) failed'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
