import json
import os
import sys
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


def _tweepy_poster():
    """Constrói um poster(file, text) que posta imagem+texto no X via tweepy."""
    import tweepy

    auth = tweepy.OAuth1UserHandler(
        os.environ["X_API_KEY"], os.environ["X_API_SECRET"],
        os.environ["X_ACCESS_TOKEN"], os.environ["X_ACCESS_TOKEN_SECRET"],
    )
    api_v1 = tweepy.API(auth)  # upload de mídia é v1.1
    client_v2 = tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )

    def poster(file: str, text: str):
        media = api_v1.media_upload(filename=file)
        client_v2.create_tweet(text=text, media_ids=[media.media_id])

    return poster


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
    new_index = post_next(manifest, _tweepy_poster(), next_index)
    save_next_index(new_index)
    print(f"postado frame {next_index} -> próximo {new_index}")


if __name__ == "__main__":
    main()
