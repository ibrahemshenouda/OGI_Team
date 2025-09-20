import paho.mqtt.client as mqtt
from gpiozero import DistanceSensor, LED
import time


MQTT_BROKER = "192.168.251.227"  # laptop IP running broker
MQTT_PORT = 1883
MQTT_TOPIC = "parking/client1"

sensor = DistanceSensor(echo=24, trigger=23, max_distance=3)  # distance in meters
led = LED(26)


client = mqtt.Client("RaspberryPiPublisher")
client.connect(MQTT_BROKER, MQTT_PORT)
print("🤖 Raspberry Pi ready. Waiting for objects...")


last_sent_time = 0  

try:
    while True:
        distance_cm = sensor.distance * 100
        current_time = time.time()

        if distance_cm <= 50:  
            led.on()

            if current_time - last_sent_time >= 2:
                print(f"📡 Object detected at {distance_cm:.1f} cm. Sending 'start' signal...")
                client.publish(MQTT_TOPIC, "start")
                last_sent_time = current_time
        else:
            led.off()

        time.sleep(0.1)

except KeyboardInterrupt:
    print("🛑 Exiting...")
finally:
    led.off()
