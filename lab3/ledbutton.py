import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.OUT)
ledstate = 0

# Callback function
def button_pushed(channel):
    global ledstate
    # If the led is off, turn it on
    if ledstate == 0:
        GPIO.output(16, True)
        ledstate=1
    # If the led is on, turn it off
    else:
        GPIO.output(16,False)
        ledstate=0

# Calss the callback function if a rising edge is detected
GPIO.add_event_detect(12, GPIO.RISING, callback=button_pushed, bouncetime=200)

# Puts the pi in a sleep loop, it will detect edges while this is
# running 
while True:
    time.sleep(1)