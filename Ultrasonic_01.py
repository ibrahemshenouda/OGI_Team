from gpiozero import DistanceSensor, LED
import time

sensor = DistanceSensor(echo=24, trigger=23, max_distance=3)
led = LED(26)


while True:
	dist = sensor.distance * 100
	if dist <= 50:
		led.on()
		print("75 EGP")
		time.sleep(1)
		led.off()
		time.sleep(2)
            
 
