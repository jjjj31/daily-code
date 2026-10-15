# daily-code

每天自动生成并提交一批编程练习片段。内容由脚本随机拼装，**不是手写项目**，只用来保持提交活跃度。
生成的片段都是能独立运行或解析的小程序，只用标准库，不含外部依赖。

## 它怎么跑

GitHub Actions 每天 04:17 UTC（北京时间 12:17）触发 `.github/workflows/daily.yml`，
在云端生成当天的文件、提交并推回 `main`。**不需要本机开机，也不需要本机常驻任何进程。**

选 04:17 UTC 是因为 GitHub 贡献日历按 UTC 归属日期，这个时刻在 UTC 和东八区落在同一天，
不会出现“提交到了第二天”的错位。

默认每天生成 4–7 个文件、拆成 1–3 次提交，落在 `snippets/YYYY/MM/DD/`。

## 改配置

编辑 `config.json`，提交推送后云端下次运行即生效：

| 字段 | 说明 |
| --- | --- |
| `files_per_day` | 每天几个文件。可写 `[4, 7]` 表示区间随机，也可写单个数字 |
| `commits_per_day` | 每天拆成几次提交，同样支持区间 |
| `languages` | 参与的语言，可选 `python` `javascript` `typescript` `go` `java` `c` `sql` `shell` |
| `skip_weekends` | 设 `true` 则周六周日不提交 |
| `output_dir` | 输出根目录，默认 `snippets` |
| `git.name` / `git.email` | 提交身份。**邮箱必须是 GitHub 账号已验证的邮箱**，否则 commit 不计入贡献图 |

不想天天提交就把 `files_per_day` 调小，或者直接禁用 workflow（见下）。

## 手动跑

在仓库目录执行（任意 Shell）：

```bash
python scripts/daily_commit.py --status          # 看今天是否已提交
python scripts/daily_commit.py --dry-run         # 只打印计划，不落盘
python scripts/daily_commit.py                   # 生成 + 本地提交
python scripts/daily_commit.py --push            # 生成 + 提交 + 推送
python scripts/daily_commit.py --push --force    # 忽略“今天已提交”检查
python scripts/daily_commit.py --files 8 --commits 2 --seed 42   # 临时覆盖数量、固定随机种子
```

Windows 上也可以直接双击 `run-local.bat`（等价于 `--push`）。

改了 `scripts/snippets.py` 里的模板后，可以跑一次自检，用本机已有的编译器验证生成的代码真的能解析：

```bash
python scripts/check_templates.py --rounds 30
```

`go` 和 `sql` 本机没有工具链时会被标成 `skipped`，其余语言逐个真编译。

想在云端之外再加一道本地定时（可选，例如想让提交时间更随机）：

```powershell
# 运行目录：任意目录；Shell：PowerShell（管理员）
schtasks /create /tn "daily-code" /sc daily /st 21:00 /tr "python C:\Users\kmttjnm\github-daily\scripts\daily_commit.py --push"
```

脚本靠根目录的 `state.json` 记录“今天已经跑过”，本地和云端不会重复提交。

## 关掉它

- 临时停：仓库 `Actions` 页面 → `daily-commit` → `···` → `Disable workflow`
- 彻底停：删掉仓库，或删掉 `.github/workflows/daily.yml`

## 几个前提

贡献图只统计满足这些条件的 commit，脚本已按此配置：

- commit 的 **author email** 绑定在你的 GitHub 账号上（`config.json` 里的邮箱已确认可用）
- 仓库不是 fork，且提交在默认分支上
- 提交由脚本用 `git -c user.email=...` 强制指定身份，不依赖运行环境的 git 配置

另外仓库自身每天都在提交，所以定时 workflow 不会被 GitHub 的“60 天无活动自动停用”规则关掉。
