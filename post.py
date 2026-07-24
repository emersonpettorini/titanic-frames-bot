import json
import os
from pathlib import Path

from state import load_next_index, save_next_index

MANIFEST = "manifest.json"


def post_next(manifest: list[dict], poster, next_index: int) -> int:
    """Posta o item em next_index via poster(file, text). Avança só em sucesso.

    Se next_index passou do fim, não faz nada e retorna next_index.
    Se poster levanta exceção, ela propaga e o índice NÃO avança.
    """
    if next_index >= len(manifest):
        return next_index
    item = manifest[next_index]
    poster(item["file"], item["text"])
    return next_index + 1


def _bluesky_poster():
    """Constrói um poster(file, text) que posta imagem+texto no Bluesky.

    A API do AT Protocol recebe os bytes da imagem direto (blob), sem precisar
    hospedar em URL pública. Login via handle + App Password (Settings → App
    Passwords no Bluesky — nunca a senha principal).
    """
    from atproto import Client

    client = Client()
    client.login(os.environ["BLUESKY_HANDLE"], os.environ["BLUESKY_APP_PASSWORD"])

    def poster(file: str, text: str):
        client.send_image(text=text, image=_load_image(file), image_alt=text)

    return poster


def _load_image(file: str) -> bytes:
    """Lê os bytes do frame: de uma URL base (nuvem) ou do disco local (teste).

    Com FRAMES_BASE_URL setado (ex: raw.githubusercontent.com/<user>/<repo>/main),
    busca {base}/{file}. Sem ele, lê o arquivo local — o mesmo post.py serve nos dois.
    """
    base = os.environ.get("FRAMES_BASE_URL")
    if base:
        import urllib.request
        with urllib.request.urlopen(f"{base}/{file}") as resp:
            return resp.read()
    return Path(file).read_bytes()


def _load_env(path=".env"):
    """Carrega KEY=VALUE do .env para os.environ (sem dependência extra)."""
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


def main():
    _load_env()
    manifest = json.loads(Path(MANIFEST).read_text(encoding="utf-8"))
    next_index = load_next_index()
    if next_index >= len(manifest):
        print("fim do vídeo — nada a postar")
        return
    new_index = post_next(manifest, _bluesky_poster(), next_index)
    save_next_index(new_index)
    print(f"postado frame {next_index} -> próximo {new_index}")


if __name__ == "__main__":
    main()
