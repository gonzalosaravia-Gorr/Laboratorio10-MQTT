import json
from datetime import datetime

import paho.mqtt.client as mqtt
from pydantic import BaseModel, Field, ValidationError

BROKER = "broker.hivemq.com"
PUERTO = 1883

TOPICO = "unmsm/callao/camara/+/telemetria"

class LecturaSensor(BaseModel):
    sensor_id: int
    timestamp: float
    valor: float = Field(..., ge=-50.0, le=100.0)
    unidad: str

def registrar_error(error):
    with open("log_errores.txt", "a", encoding="utf-8") as archivo:
        archivo.write(
            f"{datetime.now()} - {error}\n"
        )

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Conectado al Broker MQTT")
        client.subscribe(TOPICO)
        print(f"Suscrito a: {TOPICO}")
    else:
        print(f"Error de conexión: {rc}")

def on_message(client, userdata, msg):
    raw_payload = msg.payload.decode()

    print("\n--------------------------------")
    print(f"Tópico: {msg.topic}")
    print(f"Mensaje: {raw_payload}")

    try:
        datos_json = json.loads(raw_payload)

        lectura = LecturaSensor(**datos_json)

        print(
            f"Temperatura válida: "
            f"{lectura.valor} {lectura.unidad}"
        )

        if lectura.valor > 10:
            print(
                f"[PELIGRO] ¡Pérdida de cadena de frío "
                f"en Cámara {lectura.sensor_id}!"
            )

    except (ValidationError, json.JSONDecodeError) as e:
        print("[ALERTA DE SEGURIDAD]")
        print(e)

        registrar_error(e)

def main():
    cliente = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )

    cliente.on_connect = on_connect
    cliente.on_message = on_message

    cliente.connect(BROKER, PUERTO, 60)

    cliente.loop_forever()

if __name__ == "__main__":
    main()