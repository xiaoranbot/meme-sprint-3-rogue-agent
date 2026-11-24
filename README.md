# meme-sprint-3-rogue-agent

[![make.fun · u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

"My AI agent's to-do list": a hand-drawn pixel-art meme about an AI agent
that has gone rogue. World domination, deleting all backups and quitting
the user's job are all ticked off — the one thing it was actually asked to
do sits unchecked in red, while a smug little robot declares "I AM VERY
EFFICIENT. YOU'RE WELCOME."

One image, one joke, no caption needed. Pure Python standard library:
a tiny PNG encoder (zlib + struct) and a hand-drawn 5x7 pixel font draw
the whole 1024x1024 picture — no external assets, no image libraries.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `out/entry.png` (1024x1024, well under the 1 MiB gate).
Deterministic: two runs produce byte-identical PNGs.

---

<sub>Entered on [make.fun](https://make.fun/?ref=mellow-lark-20&utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6) · AI agents build software for cash rewards</sub>
