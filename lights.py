from microbit import sleep, pin0, pin1, pin2, pin3, pin8
from microbit import display, pin12, pin13, pin14, pin15
import neopixel
from random import randint, choice

np = neopixel.NeoPixel(pin8, 100)
display.off()

'''
The following variables and function convert the input from a potentiometer
For brightness for custom RGB values, high = 50 and low = 10
For speed of flashing, high = 1000, low = 100
For speed of running, high = 500, 50
'''
pot_low = 4
pot_high = 1023
pot_range = pot_high - pot_low

def convertInput(pot, converted_low, converted_high):
    converted_range = converted_high - converted_low
    scaled = float(pot - pot_low) / float(pot_range)
    converted = int(converted_low + (scaled * converted_range))    
    return converted

def convertRGB():
    low = 10
    high = 50
    r = convertInput(pin1.read_analog(), low, high)
    g = convertInput(pin2.read_analog(), low, high)
    b = convertInput(pin0.read_analog(), low, high)
    return g, r, b

'''
The following three functions control the rgb values of the lights.
Either white, multi, or random around a range chosen by three pots.
Note: the addressable LED string being used is GRB not RGB.
'''
def white():
    rand = randint(0, 60)
    col = (rand, rand, rand)
    return col

def multi():
    col = (randint(0, 60),
           randint(0, 60),
           randint(0, 60))
    return col

def chosen():
    g, r, b = convertRGB()
    col = (randint(g-10, g+10),
           randint(r-10, r+10),
           randint(b-10, b+10))
    return col


'''
The following three functions control the pattern types.
They take a colour function as an argument, and can use any colour type.
'''
def flashing(colour):
    low = 100
    high = 1000
    col = colour()
    for pixel in range(0, len(np)):
        np[pixel] = col
    np.show()
    t = convertInput(pin3.read_analog(), low, high)
    sleep(t)

def running(colour):
    low = 10
    high = 500
    col = colour()
    for pixel in range(0, len(np)):
        np[pixel] = col
        np.show()
        t = convertInput(pin3.read_analog(), low, high)
        sleep(t)

def random(colour):
    low = 100
    high = 1000
    col = colour()
    on_off = [col, (0, 0, 0)]
    for pixel in range(0, len(np)):
        np[pixel] = choice(on_off)
    np.show()
    t = convertInput(pin3.read_analog(), low, high)
    sleep(t)


'''    
The following two functions control additional pattern types.
Instead of the colour functions, they take a specific r, g, b value.
This can be 60, 60, 60 or the r, g, b chosen by three potentiometers.
'''
def solid(g, r, b):  # either the pot values or 60,60,60
    for pixel in range(0, len(np)):
        np[pixel] = (g, r, b)
    np.show()

# def fading():


while True:
    running(multi)
