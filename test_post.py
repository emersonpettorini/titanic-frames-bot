# test_post.py
import pytest
from post import post_next

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
