# Armbot

A drawbot using three cheap servo motors and an arduino to make bad drawings. 
This experiment tries to replicate the workig of brachiograph https://www.brachiograph.art/ using a tethered arduino instead of a raspberry pi.

This variation uses an arduino that runs the telemetrix firmware (similar to firmata). The arduino is conencted to a computer running python code that sends the servo positions using serial.

Please first read all the brachiograph documentation in order to understand how the original setup works.

## Setup the arduino

- Connect an arduino 
- Open the arduino IDE
- Install the Telemetrix for arduino library
- Open files -> examples -> Telemetrix 4 arduino
- Upload the example provided (it's the telemetrix for arduino firmware, similar to firmata but more recent)

## Hardware

Connect the servos to the arduino

- Inner servo connected to pin 9
- Outer servo connected to pin 10
- Pen servo connected to pin 11

(you can change those pins when initializing the armbot object).


## Setup the python side

Clone this repository : 

    git clone https://github.com/philippejadin/armbot
    cd armbot

On your computer, install the python requirements :

    pip install -r requirements.txt

## Configure your bot

Either edit armbot.py or when initialiazing armbot, pass the config you want

For example, to set another arm length : 

    from armbot import armbot
    arm = armbot(inner_arm_length = 80, outer_arm_length=120)
    arm.box()
    arm.move(20,20)
    [...]



## Test the bot !
run `python armbot.py` to connect to the arduino and draw a rectangle
run `python gcode.py` to open a gcode and draw it

