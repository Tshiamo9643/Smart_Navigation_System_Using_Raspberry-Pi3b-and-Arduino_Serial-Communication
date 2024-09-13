import RPi.GPIO as GPIO
import time
import ultr1 as u
import ultr2 as t
import gps2
from sqliteDatabase import Database

# GPIO Mode (Board / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set GPIO Pins
GPIO_TRIG = 3
GPIO_ECHO = 2
BUZZER_PIN = 4

# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIG, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def distance():
    GPIO.output(GPIO_TRIG, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIG, False)

    StartTime = time.time()
    StopTime = time.time()

    timeout = time.time() + 1
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        if time.time() > timeout:
            return float('inf')

    timeout = time.time() + 1
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
        if time.time() > timeout:
            return float('inf')

    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance

def buzz(pitch, duration):
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(delay)

def play_buzzer(distance, distance2, distance3):
    buzzer_on = False
    if distance < 50:
        buzzer_on = True
        buzz(1000, 0.1)
    if distance2 < 50:
        buzzer_on = True
        buzz(1000, 0.1)
    if distance3 < 50:
        buzzer_on = True
        buzz(1000, 0.1)

    if not buzzer_on:
        GPIO.output(BUZZER_PIN, GPIO.LOW)

if __name__ == '__main__':
    db = Database('project_data.db')
    try:
        while True:
            dist = distance()
            dist2 = t.dist2()
            dist3 = u.dist1()
            print("ULTRASONIC ONE")
            print("Measured Distance = %.1f cm" % dist)
            print("ULTRASONIC TWO")
            print("Measured Distance = %.1f cm" % dist2)
            print("ULTRASONIC THREE")
            print("Measured Distance = %.1f cm" % dist3)
            play_buzzer(dist, dist2, dist3)
            
            if dist < 50 or dist2 < 50 or dist3 < 50:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                latitude, longitude, date = gps2.read_gps()
                if latitude and longitude:
                    db.insert_data(timestamp, dist, dist2, dist3, latitude, longitude, date)
                    print("inserted")
            time.sleep(1)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
    finally:
        GPIO.cleanup()
        db.close()
