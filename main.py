import board
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn
from time import sleep

# setup pins
microphone = AnalogIn(board.IO1)  # Microphone connected to IO1
status = DigitalInOut(board.IO17)  # Status LED connected to IO17
status.direction = Direction.OUTPUT

# list of led pins
led_pins = [
    board.IO21,
    board.IO26,
    board.IO47,
    board.IO33,
    board.IO34,
    board.IO48,
    board.IO35,
    board.IO36,
    board.IO37,
    board.IO38,
    board.IO39
]

# initialize leds
leds = [DigitalInOut(pin) for pin in led_pins]
for led in leds:
    led.direction = Direction.OUTPUT

def scale_volume(value, min_input, max_input, output_max):
    # scale input value between minimum and maximum readings
    scaled_value = (value - min_input) / (max_input - min_input) * output_max
    return int(scaled_value)

# initial volume to help with smoothing changes
smooth_volume = 0

# main loop
while True:
    current_volume = microphone.value  # read the mic value
    print("Volume:", current_volume)

    # apply smoothing to volume changes
    if current_volume > smooth_volume:
        smooth_volume = current_volume  # Update immediately if current volume is greater
    else:
        smooth_volume -= (smooth_volume - current_volume) * 0.002  # speed of volume decrease

    # scale volume to match number of leds
    num_leds_on = scale_volume(smooth_volume, 23000, 36000, len(leds))

    # turn on leds in respect to volume
    for i, led in enumerate(leds):
        led.value = i < num_leds_on
    
