#!/usr/bin/python3

import requests
import time

SERVER = "http://127.0.0.1:5001"
AUDIO_PATH = "/caminho/para/audio.wav"

# 1. envia o arquivo
resp = requests.post(
    f"{SERVER}/submit",
    json={"filepath": AUDIO_PATH}
)

job_id = resp.json()["job_id"]
print("Job:", job_id)

# 2. acompanha progresso
while True:
    r = requests.get(f"{SERVER}/progress/{job_id}")
    data = r.json()

    print("Status:", data["status"], "|", data["progress"], "%")

    if data["status"] == "done":
        break
    if data["status"] == "error":
        raise RuntimeError("Erro no processamento")

    time.sleep(0.5)

# 3. pega resultado
r = requests.get(f"{SERVER}/result/{job_id}")
print("Arquivo final:", r.json()["output_file"])

