import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time


MQTT_BROKER = "192.168.72.189"  
MQTT_PORT = 1883
MQTT_TOPIC = "cam1_Parking/client1"

BUTTON_PIN = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


client = mqtt.Client("RaspberryPiPublisher")
client.connect(MQTT_BROKER, MQTT_PORT)

print("🤖 Raspberry Pi ready. Press the button to trigger the laptop.")


prev_state = GPIO.input(BUTTON_PIN)

try:
    while True:
        curr_state = GPIO.input(BUTTON_PIN)
        if prev_state == GPIO.HIGH and curr_state == GPIO.LOW:
            client.publish(MQTT_TOPIC, "start")
            print("📤 Button pressed. Sent 'start' signal to laptop.")
            time.sleep(0.3)  
        prev_state = curr_state
        time.sleep(0.05)  
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
