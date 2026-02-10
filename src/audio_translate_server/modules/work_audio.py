#!/usr/bin/python3

import tempfile
import os
import subprocess
from gtts import gTTS
from pydub import AudioSegment


def text_to_wav_audio_file(text, language, speed=1.0):
    """
    Converte texto em WAV (PCM 16kHz mono).
    speed = 1.0  -> normal
    speed = 1.5  -> 50% mais rápido (pitch preservado)
    """

    if speed <= 0:
        raise ValueError("speed must be > 0")

    # 1) gera MP3 temporário
    tts = gTTS(text=text, lang=language)
    mp3_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(mp3_file.name)

    # 2) converte para WAV normalizado (sem mexer em tempo/pitch)
    wav_raw = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

    audio = AudioSegment.from_mp3(mp3_file.name)
    audio = (
        audio
        .set_frame_rate(16000)
        .set_channels(1)
        .set_sample_width(2)
    )
    audio.export(wav_raw.name, format="wav")

    # 3) aplica time-stretch SEM alterar pitch
    if speed != 1.0:
        wav_final = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

        subprocess.run([
            "ffmpeg", "-y",
            "-i", wav_raw.name,
            "-filter:a", f"atempo={speed}",
            wav_final.name
        ], check=True)

        os.remove(wav_raw.name)
    else:
        wav_final = wav_raw

    # 4) limpa MP3
    os.remove(mp3_file.name)

    return wav_final.name






