from gpiozero import Servo, LED
from time import sleep
import paho.mqtt.client as mqtt
from threading import Thread


BROKER = "192.168.251.227" 
PORT = 1883
TOPIC = "parking/client1"


SERVO_PIN = 13
LED_PIN = 4
servo = Servo(SERVO_PIN, min_pulse_width=0.0005, max_pulse_width=0.0025)  # adjust if needed
led = LED(LED_PIN)

def open_gate():
    print("🚗 Car accepted! Opening gate...")
    led.on()             
    servo.value = 1      # fully open
    sleep(5)             # keep open for 5 seconds
    servo.value = -1     # fully closed
    sleep(1)
    led.off()            
    print("Gate closed.")


def open_gate_thread():
    Thread(target=open_gate).start()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT Broker")
        client.subscribe(TOPIC)
    else:
        print(f"❌ Connection failed with code {rc}")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"📥 Received message: {message}")
    if message.lower().startswith("car_accepted"):
        open_gate_thread()   # run in a separate thread


client = mqtt.Client("ServoSubscriber")
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER, PORT, 60)
    client.loop_forever()
except KeyboardInterrupt:
    print("🛑 Stopping Program")
finally:
    servo.detach()
    led.off()
    client.disconnect()
