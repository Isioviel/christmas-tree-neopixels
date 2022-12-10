from microbit import sleep, display, Image
from microbit import pin0, pin1, pin2, pin3, pin8
from microbit import pin12, pin13, pin14, pin15
import neopixel
from random import randint, choice

np = neopixel.NeoPixel(pin8, 122)
display.show(Image.XMAS)

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

def ccc_colour():
    pass


# -------------------------------------------------------------------------------------------------------
# The below section controls the pattern types.

def flashing(g, r, b):
    display.off()
    low = 100
    high = 1000
    for pixel in range(0, len(np)):
        np[pixel] = (g, r, b)
    np.show()
    t = convertInput(pin3.read_analog(), low, high)
    sleep(t)

def running(g, r, b):
    display.off()
    low = 10
    high = 500
    for pixel in range(0, len(np)):
        np[pixel] = (g, r, b)
        np.show()
        t = convertInput(pin3.read_analog(), low, high)
        sleep(t)

def random(g, r, b):
    display.off()
    low = 100
    high = 1000
    on_off = [(g, r, b), (0, 0, 0)]
    for pixel in range(0, len(np)):
        np[pixel] = choice(on_off)
    np.show()
    t = convertInput(pin3.read_analog(), low, high)
    sleep(t)

def solid(g, r, b):
    display.on()
    for pixel in range(0, len(np)):
        np[pixel] = (g, r, b)
    np.show()

def fading(g, r, b):
    display.off()
    pass

def ccc_pattern(g, r, b):
    display.on()
    pass


# -------------------------------------------------------------------------------------------------------
# The below section links the DIP switch to select modes.

modes = {'0000': [solid, plain_white],
         '0001': [flashing, white],
         '0010': [running, white],
         '0011': [random, white],
         # '0100': [fading, white],
         # '0101': [solid, random],
         '0110': [flashing, multi],
         '0111': [running, multi],
         '1000': [random, multi],
         # '1001': [fading, multi],
         '1010': [solid, plain_chosen],
         '1011': [flashing, chosen],
         '1100': [running, chosen],
         '1101': [random, chosen],
         # '1110': [fading, chosen],
         # '1111': [ccc_pattern, ccc_colour]
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
    if display.is_on():
        display.show(Image.XMAS)
    try:
        g, r, b = modes.get(mode)[1]()
        modes.get(mode)[0](g, r, b)
    except:
        pass
