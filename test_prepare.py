# test_prepare.py
from prepare import build_manifest, read_srt

SAMPLE = """1
00:00:00,000 --> 00:00:01,000
oi

2
00:00:03,000 --> 00:00:04,000
tchau
"""

def test_build_manifest_matches_text_by_second():
    # cue 1: seg 0–1 ("oi"); cue 2: seg 3–4 ("tchau"); seg 2 = silêncio
    frames = ["frames/00001.jpg", "frames/00002.jpg",
              "frames/00003.jpg", "frames/00004.jpg", "frames/00005.jpg"]
    m = build_manifest(frames, SAMPLE)
    assert len(m) == 5
    assert m[0] == {"index": 0, "file": "frames/00001.jpg", "seconds": 0, "text": "oi"}
    assert m[1]["text"] == "oi"        # segundo 1 ainda dentro da cue 1
    assert m[2]["text"] == ""          # segundo 2 = silêncio
    assert m[3]["text"] == "tchau"     # segundo 3 = início da cue 2
    assert m[4]["text"] == "tchau"     # segundo 4 = fim inclusivo da cue 2


def test_read_srt_cp1252_fallback(tmp_path):
    # legenda BR típica: "á" (0xE1) em cp1252 não é UTF-8 válido
    p = tmp_path / "leg.srt"
    p.write_bytes("olá coração".encode("cp1252"))
    assert read_srt(str(p)) == "olá coração"


def test_read_srt_utf8_with_bom(tmp_path):
    p = tmp_path / "leg.srt"
    p.write_bytes("olá".encode("utf-8-sig"))  # utf-8-sig prefixa o BOM nos bytes
    assert read_srt(str(p)) == "olá"           # e read_srt deve removê-lo
