import sys
from ev3dev2.motor import MediumMotor, OUTPUT_A, SpeedPercent

MAX_TURN_ROTATION = 6
STEERING_SPEED = 100
current_turn = 0
steering_motor = MediumMotor(OUTPUT_A)

def turn_right():
    steering_motor.on_for_rotations(speed=-STEERING_SPEED, rotations=1)

def turn_left():
    steering_motor.on_for_rotations(speed=STEERING_SPEED, rotations=1)    

def turn_to_angle(turn_angle):
    global current_turn

    if (turn_angle > MAX_TURN_ROTATION):
        turn_angle = MAX_TURN_ROTATION

    if (turn_angle < -MAX_TURN_ROTATION):
        turn_angle = -MAX_TURN_ROTATION

    turn = turn_angle - current_turn
    steering_motor.on_for_rotations(STEERING_SPEED, turn)
    current_turn = turn_angle

def center():
    global current_turn
    steering_motor.on_for_rotations(STEERING_SPEED, -current_turn, True, True)
    current_turn = 0