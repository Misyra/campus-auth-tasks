#!/usr/bin/env python3
"""将 snap/ 门户截图统一转为 AVIF（仓库只收录 .avif）。

提交任务前运行::

    python tools/convert-snaps-avif.py

转换成功后默认删除源文件。转完后记得把 index.json / index.gitee.json 里
对应条目的 screenshot 字段后缀同步改为 .avif 后再提交。

依赖：ffmpeg（需含 libaom-av1 或 libsvtav1 编码器及 avif muxer）。
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SNAP_DIR = Path(__file__).resolve().parent.parent / "snap"
SRC_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


def pick_encoder() -> str:
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-encoders"],
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    if "libaom-av1" in out:
        return "libaom-av1"
    if "libsvtav1" in out:
        return "libsvtav1"
    raise SystemExit("当前 ffmpeg 缺少 AV1 编码器（libaom-av1 / libsvtav1），无法输出 AVIF。")


def convert(src: Path, dst: Path, encoder: str, crf: int) -> bool:
    quality = (
        ["-crf", str(crf), "-b:v", "0", "-cpu-used", "4"]
        if encoder == "libaom-av1"
        else ["-crf", str(crf), "-preset", "6"]
    )
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
         "-i", str(src), "-c:v", encoder, *quality, str(dst)],
        check=False,
    )
    return proc.returncode == 0 and dst.is_file()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snap-dir", default=SNAP_DIR, type=Path)
    parser.add_argument("--crf", default=24, type=int)
    parser.add_argument("--keep-source", action="store_true")
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        raise SystemExit("未找到 ffmpeg，请先安装（https://ffmpeg.org/download.html）再运行本脚本。")

    files = sorted(
        p for p in args.snap_dir.iterdir()
        if p.is_file() and p.suffix.lower() in SRC_SUFFIXES
    )
    if not files:
        print("snap/ 下没有需要转换的图片。")
        return

    encoder = pick_encoder()
    failed: list[str] = []
    for src in files:
        dst = src.with_suffix(".avif")
        print(f"转换 {src.name} -> {dst.name}（{encoder}）")
        if not convert(src, dst, encoder, args.crf):
            failed.append(src.name)
            continue
        if not args.keep_source:
            src.unlink()

    if failed:
        raise SystemExit(f"转换失败：{', '.join(failed)}")
    print("完成。别忘了把 index.json / index.gitee.json 中 screenshot 字段后缀改为 .avif 后再提交。")


if __name__ == "__main__":
    sys.exit(main())
