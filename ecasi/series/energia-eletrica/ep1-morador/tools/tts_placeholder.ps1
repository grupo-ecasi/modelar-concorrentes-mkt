# Gera uma narração PROVISÓRIA com a voz do Windows (Maria, pt-BR), só para montar e sincronizar o vídeo
# enquanto a narração do ElevenLabs não chega. Uso: powershell -File tools/tts_placeholder.ps1
param([int]$Rate = 1)
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.SelectVoice("Microsoft Maria Desktop")
$s.Rate = $Rate
$base = Split-Path -Parent $PSScriptRoot
$s.SetOutputToWaveFile((Join-Path $base "assets\narracao-provisoria.wav"))
$s.Speak((Get-Content -Raw -Encoding UTF8 (Join-Path $PSScriptRoot "narracao-ep1.txt")))
$s.Dispose()
