#!/usr/bin/python3

from flask import Flask, request, jsonify
import threading
import uuid
import os
import queue

from audio_translate_server.processing import process_audio

import audio_translate_server.about             as about
import audio_translate_server.modules.configure as configure 


# ---------- Path to config gpt file ----------
CONFIG_GPT_PATH = os.path.join( os.path.expanduser("~"),
                                ".config", 
                                about.__package__, 
                                "config.gpt.json" )

DEFAULT_GPT_CONTENT={
    "api_key": "",
    "usage": "https://deepinfra.com/dash/usage",
    "base_url": "https://api.deepinfra.com/v1/openai",
    "model": "openai/whisper-large-v3",
    "play_factor": 1.0,
    "microphone_sink": "VirtualMicSink",
    "host":"127.0.0.1",
    "port": 5001
}

configure.verify_default_config(CONFIG_GPT_PATH,default_content=DEFAULT_GPT_CONTENT)

################################################################################


app = Flask(__name__)

# Estado global
jobs = {}        # job_id -> {"progress": int, "status": str}
results = {}     # job_id -> output filepath

lock = threading.Lock()
job_queue = queue.Queue()


def worker():
    """
    Worker único.
    Processa UM job por vez, em ordem.
    """
    while True:
        job_id, input_path = job_queue.get()
        try:
            process_audio(job_id, input_path, jobs, results, lock)
        finally:
            job_queue.task_done()


# Inicia o worker assim que o server sobe
threading.Thread(target=worker, daemon=True).start()


@app.route("/submit", methods=["POST"])
def submit():
    data = request.json or {}
    input_path = data.get("filepath")

    if not input_path or not os.path.isfile(input_path):
        return jsonify({"error": "invalid filepath"}), 400

    job_id = str(uuid.uuid4())

    with lock:
        jobs[job_id] = {
            "progress": 0,
            "status": "queued"
        }

    # Enfileira o job (não cria thread!)
    job_queue.put((job_id, input_path))

    return jsonify({"job_id": job_id})


@app.route("/progress/<job_id>")
def progress(job_id):
    with lock:
        job = jobs.get(job_id)

    if not job:
        return jsonify({"error": "job not found"}), 404

    return jsonify(job)


@app.route("/result/<job_id>")
def result(job_id):
    with lock:
        output = results.get(job_id)

    if not output:
        return jsonify({"error": "result not ready"}), 404

    return jsonify({"output_file": output})


def main():
    config_gpt=configure.load_config(CONFIG_GPT_PATH)
    
    app.run(
        host=config_gpt["host"],
        port=config_gpt["port"],
        threaded=True
    )

if __name__ == "__main__":
    main()

