from microbit import sleep, display
from microbit import pin0, pin1, pin2, pin3, pin8
from microbit import pin12, pin13, pin14, pin15
import neopixel
from random import randint, choice

np = neopixel.NeoPixel(pin8, 122)
display.off()

# -------------------------------------------------------------------------------------------------------
# The below section converts the input from a potentiometer.

pot_low = 0
pot_high = 1023
pot_range = pot_high - pot_low

def convertInput(pot, converted_low, converted_high):
    converted_range = converted_high - converted_low
    scaled = float(pot - pot_low) / float(pot_range)
    converted = int(converted_low + (scaled * converted_range))
    if converted_low <= converted <= converted_high:
        return converted
    else:
        pass
    
def convertRGB():
    low = 10
    high = 50
    r = convertInput(pin1.read_analog(), low, high)
    g = convertInput(pin2.read_analog(), low, high)
    b = convertInput(pin0.read_analog(), low, high)
    return g, r, b


# -------------------------------------------------------------------------------------------------------
# The below section controls the colours.
# Note: the addressable LED string being used is GRB not RGB.

def white():
    rand = randint(0, 60)
    g, r, b = (rand, rand, rand)
    return g, r, b

def plain_white():
    g, r, b = (60, 60, 60)
    return g, r, b

def multi():
    g, r, b = (randint(0, 60),
               randint(0, 60),
               randint(0, 60))
    return g, r, b

def chosen():
    g, r, b = convertRGB()
    g, r, b = (randint(g-10, g+10),
               randint(r-10, r+10),
               randint(b-10, b+10))
    return g, r, b

def plain_chosen():
    g, r, b = convertRGB()
    return g, r, b


# -------------------------------------------------------------------------------------------------------
# The below section controls the pattern types.

def flashing(g, r, b):
    low = 100
    high = 1000
    for pixel in range(0, len(np)):
        np[pixel] = (g, r, b)
    np.show()
    t = convertInput(pin3.read_analog(), low, high)
    sleep(t)

def running(g, r, b):
    low = 10
    high = 500
    for pixel in range(0, len(np)):
        np[pixel] = (g, r, b)
        np.show()
        t = convertInput(pin3.read_analog(), low, high)
        sleep(t)

def random(g, r, b):
    low = 100
    high = 1000
    on_off = [(g, r, b), (0, 0, 0)]
    for pixel in range(0, len(np)):
        np[pixel] = choice(on_off)
    np.show()
    t = convertInput(pin3.read_analog(), low, high)
    sleep(t)

def solid(g, r, b):
    for pixel in range(0, len(np)):
        np[pixel] = (g, r, b)
    np.show()

# def fading(g, r, b):

# def multi_switch(g, r, b):


# -------------------------------------------------------------------------------------------------------
# The below section links the DIP switch to select modes.

modes = {'0000': [solid, plain_white],
         '1000': [flashing, white],
         '1100': [running, white],
         '1110': [random, white],
         # '1111': [fading, white],
         '0100': [flashing, multi],
         '0110': [running, multi],
         '0111': [random, multi],
         '0001': [solid, plain_chosen],
         '0010': [flashing, chosen],
         '0011': [running, chosen],
         '1011': [random, chosen],
         # '1101': [fading, plain_chosen]
         }

def dip():
    dip = [pin12.read_digital(),
           pin13.read_digital(),
           pin14.read_digital(),
           pin15.read_digital()]
    switch = str(dip[0]) + str(dip[1]) + str(dip[2]) + str(dip[3])
    return switch


# -------------------------------------------------------------------------------------------------------
# Loop to check switch positions & run appropriate pattern and colour options.

while True:
    mode = dip()
    try:
        g, r, b = modes.get(mode)[1]()
        modes.get(mode)[0](g, r, b)
    except:
        pass
