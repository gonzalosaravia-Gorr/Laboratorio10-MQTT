import time
import random
import json
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PUERTO = 1883

def conectar_mqtt():
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )
    client.connect(BROKER, PUERTO, 60)
    return client

def main():
    cliente = conectar_mqtt()
    cliente.loop_start()

    contador = 0

    try:
        while True:
            contador += 1

            # Alternar entre cámaras 1 y 2
            camara_id = random.choice([1, 2])

            topico = f"unmsm/callao/camara/{camara_id}/telemetria"

            # Cada 5 mensajes generar una falla
            if contador % 5 == 0:
                valor = random.choice([150, "ERROR_SENSOR"])
            else:
                valor = round(random.uniform(2.0, 15.0), 2)

            datos_sensor = {
                "sensor_id": camara_id,
                "timestamp": time.time(),
                "valor": valor,
                "unidad": "Celsius"
            }

            mensaje = json.dumps(datos_sensor)

            cliente.publish(topico, mensaje, qos=1)

            print(f"[PUBLISHER] {topico}")
            print(mensaje)

            time.sleep(3)

    except KeyboardInterrupt:
        print("\nPublicador detenido")

    finally:
        cliente.loop_stop()
        cliente.disconnect()

if __name__ == "__main__":
    main()