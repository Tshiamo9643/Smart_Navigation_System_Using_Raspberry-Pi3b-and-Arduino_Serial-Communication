# Libraries
import RPi.GPIO as GPIO
import time
import Ultrasonic_Sensor as t
# GPIO Mode (Board / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


GPIO_TRIG = 10
GPIO_ECHO = 9
#Set GPIO Pins

# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIG, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def dist2():
    # Set Trigger to HIGH
    GPIO.output(GPIO_TRIG, True)
    
    # Set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIG, False)
    
    StartTime = time.time()
    StopTime = time.time()
    
    # Save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    # Save StopTime
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    
    # Time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # Multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance

if __name__ == '__main__':
    try:
        while True:
            dist = dist2()
            print("Measured Distance = %.1f cm" % dist)
            print("=============")
            print("Measured Distance = %.1f cm" % dist)
            time.sleep(1)  # Sleep for one second before next measurement
            
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()


