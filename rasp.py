import time
import paho.mqtt.client as mqtt
import cv2
import re
import pandas as pd
import os
from datetime import datetime
import easyocr
from threading import Thread

# ----------------------
# Configuration
# ----------------------
MQTT_BROKER = "192.168.251.227"  # Laptop IP running broker
MQTT_PORT = 1883
MQTT_TOPIC = "parking/client1"

EXCEL_FILE = r"D:\SKADA\numbers.xlsx"
IMAGE_DIR = r"D:\SCADA\text recognetion\captured_images"
os.makedirs(IMAGE_DIR, exist_ok=True)

reader = easyocr.Reader(['en'], gpu=False)
processing = False

# ----------------------
# OCR & Image Processing
# ----------------------
def enhance_and_extract_numbers(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    cv2.GaussianBlur(gray, (3,3),0)
    rgb_frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    results = reader.readtext(rgb_frame, detail=1)
    numbers_only = []

    for bbox, text, prob in results:
        digits = re.findall(r'\d+', text)
        if digits:
            numbers_only.extend(digits)
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))
            cv2.rectangle(frame, top_left, bottom_right, (0,255,0),2)
            cv2.putText(frame, text, (top_left[0], top_left[1]-5),
                        cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)
    return numbers_only, frame

# ----------------------
# Capture Camera
# ----------------------
def capture_and_extract_numbers(client):
    global processing
    processing = True
    cap = cv2.VideoCapture(0)
    time.sleep(2)
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        cap.release()
        processing = False
        return

    numbers_only, frame_with_boxes = enhance_and_extract_numbers(frame)
    accepted_numbers = [num for num in numbers_only if len(num)==4]

    if accepted_numbers:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = os.path.join(IMAGE_DIR,f"capture_{timestamp}.jpg")
        cv2.imwrite(image_filename, frame_with_boxes)
        print(f"Image saved: {image_filename}")

        if os.path.exists(EXCEL_FILE):
            df_existing = pd.read_excel(EXCEL_FILE)
        else:
            df_existing = pd.DataFrame(columns=["Detected Numbers"])
        for num in accepted_numbers:
            df_existing = pd.concat([df_existing, pd.DataFrame([[num]], columns=["Detected Numbers"])],
                                    ignore_index=True)
        df_existing.to_excel(EXCEL_FILE,index=False)
        print(f"✅ Accepted numbers saved to Excel: {EXCEL_FILE}")

        for num in accepted_numbers:
            msg = f"car_accepted:{num}"
            client.publish(MQTT_TOPIC, msg)
            print(f"📡 MQTT sent: {msg}")
    else:
        print("No 4-digit numbers detected")

    cap.release()
    processing = False

def on_message(client, userdata, msg):
    global processing
    payload = msg.payload.decode().lower()
    print(f"MQTT received: {payload}")
    if payload == "casher_on" and not processing:
        Thread(target=capture_and_extract_numbers,args=(client,)).start()
    elif payload == "casher_on" and processing:
        print("Already processing previous request, ignoring this one.")

# ----------------------
# MQTT Setup
# ----------------------
client = mqtt.Client("LaptopSubscriber")
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT)
client.subscribe(MQTT_TOPIC)
client.loop_start()

print("📡 Waiting for Blynk trigger...")

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n🛑 Exiting...")
    client.loop_stop()
