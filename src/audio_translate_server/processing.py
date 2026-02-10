#!/usr/bin/python3


import subprocess
import os

import audio_translate_server.about             as about
import audio_translate_server.modules.configure as configure 

from audio_translate_server.modules.work_audio import text_to_wav_audio_file

from deep_consultation.core_audio import speech_file_translate_deepinfra

CONFIG_GPT_PATH = os.path.join( os.path.expanduser("~"),
                                ".config", 
                                about.__package__, 
                                "config.gpt.json" )



def play_to_virtual_mic(wav_path, device):
    subprocess.run(
        ["paplay", f"--device={device}", wav_path],
        check=True
    )


def process_audio(job_id, input_path, jobs, results, lock):
    """
    Processa UM áudio por vez.
    - Atualiza progresso
    - Salva WAV final
    - Toca no VirtualMic
    """
    try:
        config_gpt=configure.load_config(CONFIG_GPT_PATH)
        
        with lock:
            jobs[job_id]["status"] = "processing"
            jobs[job_id]["progress"] = 0

        print("input_path",input_path)
        translate = speech_file_translate_deepinfra(config_gpt["base_url"], 
                                                    config_gpt["api_key"], 
                                                    config_gpt["model"], 
                                                    input_path )
        print("translate",translate)
        wav_path = text_to_wav_audio_file(  translate, 
                                            "en", 
                                            speed=config_gpt["play_factor"] ) 

        print("wav_path:",wav_path)

        # 🎧 TOCA NO MICROFONE VIRTUAL
        play_to_virtual_mic(wav_path, device=config_gpt["microphone_sink"])
        
        print("write in device")

        with lock:
            results[job_id] = wav_path
            jobs[job_id]["status"] = "done"
            jobs[job_id]["progress"] = 100
        
        print("END")

    except Exception as e:
        with lock:
            jobs[job_id]["status"] = "error"
            jobs[job_id]["progress"] = -1


################################################################################

        '''
import soundfile as sf
import time  
        
        # Lê áudio de entrada
        audio, sr = sf.read(input_path)

        # Aqui entra seu processamento real
        processed = audio.copy()

        total_steps = 10
        for i in range(total_steps):
            # Simula processamento pesado
            time.sleep(0.5)

            with lock:
                jobs[job_id]["progress"] = int((i + 1) / total_steps * 100)
                
                
        # Salva resultado
        os.makedirs("output", exist_ok=True)
        output_path = f"output/{job_id}.wav"
        sf.write(output_path, processed, sr)
        '''
