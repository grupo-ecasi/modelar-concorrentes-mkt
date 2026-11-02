"""Master final do áudio: loudnorm em duas passagens (EBU R128) para -14 LUFS e -1 dBTP, padrão do Instagram.

Mede o MP4 renderizado, aplica a correção linear com os valores medidos e copia o vídeo sem recodificar.
Reaproveita a técnica do preparar.mjs do C:\\Editor.Videos (tema 08).

Uso: python -I tools/master.py renders/entrada.mp4 renders/saida.mp4
"""
import json
import re
import subprocess
import sys

I, TP, LRA = -14.0, -1.0, 11.0


def measure(path, extra=""):
    af = f"loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json{extra}"
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", af, "-f", "null", "-"], capture_output=True, text=True).stderr
    return json.loads(re.findall(r"\{[^{}]+\}", err)[-1])


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    m = measure(src)
    print(f"antes: {m['input_i']} LUFS · pico {m['input_tp']} dBTP · LRA {m['input_lra']}")
    af = (
        f"loudnorm=I={I}:TP={TP}:LRA={LRA}:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
        f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
        "aresample=48000"
    )
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", src, "-map", "0:v", "-map", "0:a", "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", dst],
        check=True,
    )
    out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", dst, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    summ = out[out.rfind("Summary:") :]
    il = re.search(r"I:\s+(-?[\d.]+) LUFS", summ).group(1)
    pk = re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ).group(1)
    print(f"depois: {il} LUFS · pico verdadeiro {pk} dBFS -> {dst}")
