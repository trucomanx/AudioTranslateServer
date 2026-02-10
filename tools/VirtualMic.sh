#!/bin/bash

SINK_NAME="VirtualMicSink"
SINK_LONG_NAME="Virtual_Microphone_Sink"
SOURCE_NAME="VirtualMicSource"
SOURCE_LONG_NAME="Microfone_Virtual_Processado_Translate"

echo "== Verificando sink virtual =="
if ! pactl list short sinks | grep -q "$SINK_NAME"; then
    pactl load-module module-null-sink \
        sink_name=$SINK_NAME \
        sink_properties=device.description=\"$SINK_LONG_NAME\"
    echo "Sink $SINK_NAME criado"
else
    echo "Sink $SINK_NAME já existe"
fi

echo "== Verificando source (microfone virtual) =="
if ! pactl list short sources | grep -q "$SOURCE_NAME"; then
    pactl load-module module-remap-source \
        source_name=$SOURCE_NAME \
        master="$SINK_NAME.monitor" \
        source_properties=device.description=\"$SOURCE_LONG_NAME\"
    echo "Source $SOURCE_NAME criado"
else
    echo "Source $SOURCE_NAME já existe"
fi

echo ""
echo "== Sinks disponíveis =="
pactl list short sinks

echo ""
echo "== Sources disponíveis =="
pactl list short sources

echo ""
echo "== Configuração concluída =="
echo "Para testar: paplay --device=$SINK_NAME /usr/share/sounds/alsa/Front_Center.wav"
echo "Para configurar visualmente: pavucontrol"



# #Borrar
# pactl list short modules
# pactl unload-module 28

