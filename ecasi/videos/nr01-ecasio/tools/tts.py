"""Narração PROVISÓRIA com voz neural grátis (edge-tts, pt-BR-AntonioNeural) e tempos palavra a palavra.

Lê assets/narracao.txt e grava:
- assets/narracao-tts.mp3 (voz crua)
- assets/transcript-raw.json ([{text, start, end}] a partir dos WordBoundary do serviço)

Quando o usuário mandar a voz definitiva (ElevenLabs "Will"), troque o MP3 e gere o transcript com
`npx hyperframes transcribe` (ver README do projeto).

Uso: python tools/tts.py [voz] [velocidade]
"""
import asyncio
import json
import os
import sys

import edge_tts

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOZ = sys.argv[1] if len(sys.argv) > 1 else "pt-BR-AntonioNeural"
RATE = sys.argv[2] if len(sys.argv) > 2 else "+6%"


async def main():
    texto = open(os.path.join(BASE, "assets", "narracao.txt"), encoding="utf-8").read().strip()
    texto = " ".join(texto.split())
    com = edge_tts.Communicate(texto, VOZ, rate=RATE, boundary="WordBoundary")
    audio, palavras = bytearray(), []
    async for ch in com.stream():
        if ch["type"] == "audio":
            audio += ch["data"]
        elif ch["type"] == "WordBoundary":
            ini = ch["offset"] / 1e7
            palavras.append({"text": ch["text"], "start": round(ini, 3), "end": round(ini + ch["duration"] / 1e7, 3)})
    open(os.path.join(BASE, "assets", "narracao-tts.mp3"), "wb").write(audio)
    json.dump(palavras, open(os.path.join(BASE, "assets", "transcript-raw.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(palavras), "palavras; fim em", palavras[-1]["end"], "s")


asyncio.run(main())
