import time
import pigpio
import numpy.random as random

# Constants
MOTOR = 18  # Connect servomotor to BCM 18
BUTTON = 15 # Connect button pin to BCM 15

# Starts pigpio and checks if that worked
pi = pigpio.pi()
if not pi.connected:
    exit(0)

# Setup pins
pi.set_mode(BUTTON, pigpio.INPUT)           # Set button pin as input
pi.set_pull_up_down(BUTTON, pigpio.PUD_UP)  # Set pullup resistor for button
pi.set_glitch_filter(BUTTON, 100)           # Debounce button input

state = "WAIT_FOR_RANDOM_MOVE"

# Translates a value from one range to another
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Find range of each range
    leftRange = leftMax - leftMin 
    rightRange = rightMax - rightMin

    # Finds scale using floating point division
    floatScale = float(value - leftMin) / float(leftRange)
    return rightMin + (intScale * rightRange) # Returns scaled value

# Sets the pwm for the given pulsewidth
def move_to_angle(degrees):
    pi.set_servo_pulsewidth(MOTOR, translate(degrees, -90, 90, 1000, 2000))

# Defines the button callback
def button_pushed(gpio, level, tick):
    global state
    state = "RANDOM_MOVE"

callback1 = pi.callback(BUTTON, pigpio.RISING_EDGE, button_pushed)

while(True):

    # State 1: waits for button input
    if state == "WAIT_FOR_BUTTON":
        time.sleep(.1)

    # State 2: executes a random move
    if state == "RANDOM_MOVE":
        move_to_angle(random.randint(-90,90))
        state = "WAIT_FOR_BUTTON"

