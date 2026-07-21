import srt


def parse_srt(srt_text: str) -> list:
    """Faz o parse de um SRT em lista de srt.Subtitle, ordenada por início."""
    return list(srt.parse(srt_text))


def text_at(cues: list, seconds: int) -> str:
    """Texto da legenda ativa em `seconds` (start<=seconds<=end), ou "" se silêncio.

    Multi-linha é unido por espaço. Intervalos inclusivos nas duas pontas.
    """
    for cue in cues:
        if cue.start.total_seconds() <= seconds <= cue.end.total_seconds():
            return " ".join(cue.content.splitlines()).strip()
    return ""
