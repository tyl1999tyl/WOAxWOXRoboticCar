import RPi.GPIO as gpio

import time

def init():

    gpio.setmode(gpio.BOARD)

    gpio.setup(7, gpio.OUT)

    gpio.setup(11, gpio.OUT)

    gpio.setup(13, gpio.OUT)

    gpio.setup(15, gpio.OUT)

def forward():


    gpio.output (7, True)

    gpio.output (11, False)

    gpio.output (13, False)

    gpio.output (15, True)


def reverse():

    gpio.output (7, False)

    gpio.output (11, True)

    gpio.output (13, True)

    gpio.output (15, False)



def turn_left():


    gpio.output (7, True)

    gpio.output (11, True)

    gpio.output (13, True)

    gpio.output (15, False)

def turn_right():


    gpio.output (7, False)

    gpio.output (11, True)

    gpio.output (13, False)

    gpio.output (15, False)

def pivot_left():


    gpio.output (7, True)

    gpio.output (11, False)

    gpio.output (13, True)

    gpio.output (15, False)

def pivot_right():


    gpio.output (7, False)

    gpio.output (11, True)

    gpio.output (13, False)

    gpio.output (15, True)


if __name__ == "__main__":

    init()
    forward()
    time.sleep(1)
    gpio.cleanup()


