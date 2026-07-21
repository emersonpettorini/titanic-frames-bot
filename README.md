# Bot every frame in order

Extrai 1 frame/segundo de um vídeo e posta no X em ordem, com a legenda.

## Setup

1. Instale o ffmpeg e garanta que `ffmpeg` está no PATH.
2. `py -m venv .venv && .venv\Scripts\activate`
3. `py -m pip install -r requirements.txt`
4. Copie `.env.example` para `.env` e preencha as 4 chaves do X.

## Uso

```
py prepare.py video.mp4 legenda.srt
py post.py
```

`prepare.py` roda uma vez. Um agendador (Task Scheduler / GitHub Actions / cron)
chama `py post.py` a cada 1h30.
