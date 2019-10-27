#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_B, LargeMotor
from ev3dev2.sensor import INPUT_4, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import ColorSensor, InfraredSensor, UltrasonicSensor
from ev3dev2.display import Display
from ev3dev2.button import Button
from ev3dev2.led import Leds
import time, os, sys
import vehicle, steering

PARKING_MODE_PARALLEL = 'PARKING_MODE_PARALLEL'
PARKING_MODE_PERPENDICULAR = 'PARKING_MODE_PERPENDICULAR'

MODE_CALIBRATING = 'MODE_CALIBRATING'
MODE_SEEKING_PARKING_SPACE = 'MODE_SEEKING_PARKING_SPACE'

parking_mode = PARKING_MODE_PARALLEL
mode = MODE_CALIBRATING

def init_hardware():
    global button, display, leds, drive, infraredSensor

    drive = LargeMotor(OUTPUT_B)
    infraredSensor = InfraredSensor(INPUT_3)
    infraredSensor.mode = InfraredSensor.MODE_IR_PROX
    leds = Leds()

    # ultrasonicSensor = UltrasonicSensor(INPUT_2)
    # ultrasonicSensor.mode = UltrasonicSensor.MODE_US_DIST_CM

    display = Display()
    button = Button()
    button.on_enter = btn_on_enter

def process_buttons():
    if button.left:
        steering.turn_left()

    if button.right:
        steering.turn_right()        

def btn_on_enter(pressed):
    global mode

    if not pressed:
        if mode != MODE_SEEKING_PARKING_SPACE:
            mode = MODE_SEEKING_PARKING_SPACE
            leds.set_color('LEFT', 'YELLOW')
            leds.set_color('RIGHT', 'YELLOW')            
            drive.on_for_rotations(speed=-20, rotations=14, block=False)
        else:
            mode = MODE_CALIBRATING
            steering.center()

def timestamp():
    return int(round(time.time() * 1000))

KP = 0.25
KD = 0.2
last_error = 0
measuring_empty_space = False
ms_start = 0

DESIRED_SIDE_DISTANCE = 10 #cm
PARKING_SPACE_DEPTH = 30

os.system('setfont Lat15-TerminusBold14')
init_hardware()
print('READY', file=sys.stderr)
leds.set_color('LEFT', 'AMBER')
leds.set_color('RIGHT', 'AMBER')

while True:

    process_buttons()
    button.process()
    side_distance = infraredSensor.proximity

    if mode == MODE_SEEKING_PARKING_SPACE:
        
        if side_distance > PARKING_SPACE_DEPTH:

            if not measuring_empty_space:
                measuring_empty_space = True
                ms_start = timestamp()

        else:

            if measuring_empty_space:
                measuring_empty_space = False
                ms_length = timestamp() - ms_start
                if ms_length > 99999:
                    #empty space with proper size detected
                    pass

            error = side_distance - DESIRED_SIDE_DISTANCE
            turn_angle = KP * error # + KD * (error - last_error)) 

            last_error = error
            steering.turn_to_angle(turn_angle)

        print('DST='+str(side_distance) + ' ERROR='+str(error)+ ', TURN='+str(turn_angle), file=sys.stderr)

    time.sleep(0.05)
