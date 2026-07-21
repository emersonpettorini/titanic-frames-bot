import json
import shutil
import subprocess
import sys
from pathlib import Path

from subtitles import parse_srt, text_at

FRAMES_DIR = "frames"
MANIFEST = "manifest.json"


def extract_frames(video_path: str, out_dir: str = FRAMES_DIR) -> list[str]:
    """Extrai 1 frame/segundo via ffmpeg -> out_dir/NNNNN.jpg. Retorna os caminhos ordenados."""
    out = Path(out_dir)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", "fps=1",
        "-q:v", "2",
        str(out / "%05d.jpg"),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg falhou:\n{result.stderr}")
    return sorted(str(p) for p in out.glob("*.jpg"))


def build_manifest(frame_files: list[str], srt_text: str) -> list[dict]:
    """Casa cada frame (segundo = índice) com a legenda ativa. Frames em ordem."""
    cues = parse_srt(srt_text)
    manifest = []
    for i, file in enumerate(sorted(frame_files)):
        manifest.append({
            "index": i,
            "file": file.replace("\\", "/"),
            "seconds": i,
            "text": text_at(cues, i),
        })
    return manifest


def main():
    if len(sys.argv) != 3:
        print("uso: py prepare.py <video> <srt>")
        sys.exit(1)
    video, srt_path = sys.argv[1], sys.argv[2]
    srt_text = Path(srt_path).read_text(encoding="utf-8")
    frames = extract_frames(video)
    manifest = build_manifest(frames, srt_text)
    Path(MANIFEST).write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(manifest)} frames -> {MANIFEST}")


if __name__ == "__main__":
    main()
