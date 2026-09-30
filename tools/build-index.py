"""校验统一任务索引并生成 Gitee 与旧版 HTTP 兼容索引。"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "index.json"
GITHUB_RAW = "https://raw.githubusercontent.com/Misyra/campus-auth-tasks/master/"
GITEE_RAW = "https://raw.giteeusercontent.com/Misyra/campus-auth-tasks/raw/master/"


def render(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def outputs() -> dict[Path, str]:
    entries = json.loads(SOURCE.read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise ValueError("index.json 必须是数组")
    ids: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("索引条目必须是对象")
        task_id = entry.get("id")
        kind = entry.get("type")
        if not isinstance(task_id, str) or not task_id:
            raise ValueError("索引条目缺少 id")
        if task_id in ids:
            raise ValueError(f"重复任务 ID: {task_id}")
        ids.add(task_id)
        if kind not in {"browser", "http", "script"}:
            raise ValueError(f"{task_id}: type 必须是 browser/http/script")
        task_url = entry.get("url")
        if not isinstance(task_url, str) or not task_url.startswith(GITHUB_RAW + "tasks/"):
            raise ValueError(f"{task_id}: url 必须指向本仓库 tasks/ 下的 GitHub raw 文件")
        task_path = (ROOT / task_url.removeprefix(GITHUB_RAW)).resolve()
        if not task_path.is_relative_to((ROOT / "tasks").resolve()):
            raise ValueError(f"{task_id}: 任务路径越界")
        if not task_path.is_file():
            raise ValueError(f"{task_id}: 任务文件不存在")
        if task_path.stem != task_id:
            raise ValueError(f"{task_id}: ID 与文件名不一致")
        task = json.loads(task_path.read_text(encoding="utf-8"))
        if task.get("type", "browser") != kind:
            raise ValueError(f"{task_id}: 索引 type 与任务文件不一致")
    mirror = []
    for entry in entries:
        item = dict(entry)
        for field in ("url", "screenshot"):
            if isinstance(item.get(field), str):
                item[field] = item[field].replace(GITHUB_RAW, GITEE_RAW, 1)
        mirror.append(item)
    return {
        ROOT / "index.gitee.json": render(mirror),
        ROOT / "index.http.json": render([entry for entry in entries if entry["type"] == "http"]),
        ROOT / "index.http.gitee.json": render([entry for entry in mirror if entry["type"] == "http"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="检查生成文件是否最新")
    args = parser.parse_args()
    expected = outputs()
    for path, content in expected.items():
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                raise SystemExit(f"需要重新生成: {path.name}")
        else:
            path.write_text(content, encoding="utf-8")
    print("索引校验通过")


if __name__ == "__main__":
    main()
