# test_post.py
import pytest
from post import post_next, _jpeg_size


def test_jpeg_size_reads_sof():
    # SOI + SOF0(len 17): precisão 08, altura 0x0100=256, largura 0x0200=512
    data = b"\xff\xd8\xff\xc0\x00\x11\x08\x01\x00\x02\x00" + b"\x00" * 8
    assert _jpeg_size(data) == (512, 256)


def test_jpeg_size_skips_segments_before_sof():
    # APP0 (len 4, 2 bytes de conteúdo) antes do SOF — o parser tem que pular
    data = b"\xff\xd8\xff\xe0\x00\x04\xaa\xbb\xff\xc0\x00\x11\x08\x01\x00\x02\x00"
    assert _jpeg_size(data) == (512, 256)

MANIFEST = [
    {"index": 0, "file": "frames/00001.jpg", "seconds": 0, "text": "oi"},
    {"index": 1, "file": "frames/00002.jpg", "seconds": 1, "text": ""},
]

def test_advances_on_success():
    posted = []
    def poster(file, text): posted.append((file, text))
    new_index = post_next(MANIFEST, poster, 0)
    assert new_index == 1
    assert posted == [("frames/00001.jpg", "oi")]

def test_does_not_advance_on_failure():
    def poster(file, text): raise RuntimeError("rate limit")
    with pytest.raises(RuntimeError):
        post_next(MANIFEST, poster, 0)

def test_end_of_manifest_returns_same_index():
    def poster(file, text): raise AssertionError("não deveria postar")
    assert post_next(MANIFEST, poster, 2) == 2
