#!/bin/bash

curl -X POST http://127.0.0.1:5001/submit \
     -H "Content-Type: application/json" \
     -d '{"filepath": "/home/fernando/Downloads/audio_server/tools/example.wav"}'


#curl http://127.0.0.1:5001/progress/<JOB_ID>
#curl http://127.0.0.1:5001/result/<JOB_ID>


