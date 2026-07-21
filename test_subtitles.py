# test_subtitles.py
from subtitles import parse_srt, text_at

SAMPLE = """1
00:00:00,000 --> 00:00:02,000
Olá mundo

2
00:00:05,000 --> 00:00:07,500
Segunda fala
"""

def test_text_at_within_cue():
    cues = parse_srt(SAMPLE)
    assert text_at(cues, 0) == "Olá mundo"
    assert text_at(cues, 1) == "Olá mundo"

def test_text_at_silence_returns_empty():
    cues = parse_srt(SAMPLE)
    assert text_at(cues, 3) == ""      # entre as duas falas
    assert text_at(cues, 100) == ""    # depois do fim

def test_text_at_boundary_inclusive():
    cues = parse_srt(SAMPLE)
    assert text_at(cues, 2) == "Olá mundo"   # 00:00:02,000 = fim inclusivo
    assert text_at(cues, 5) == "Segunda fala"

def test_multiline_cue_joined():
    srt_text = """1
00:00:00,000 --> 00:00:01,000
linha um
linha dois
"""
    cues = parse_srt(srt_text)
    assert text_at(cues, 0) == "linha um linha dois"
