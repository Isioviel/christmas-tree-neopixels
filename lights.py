from microbit import sleep, pin0
import neopixel
from random import randint, choice

np = neopixel.NeoPixel(pin0, 100)


'''
The following three functions control the rgb values of the lights.
Either white, multicoloured, or random around a range chosen by three potentiometers.
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
    r = 10  # R POT between 10 and 50
    g = 50  # G POT between 10 and 50
    b = 10  # B POT between 10 and 50
    col = (randint(g-10, g+10),
           randint(r-10, r+10),
           randint(b-10, b+10))
    return col


'''
The following three functions control the pattern types.
They take a colour function as an argument, and can use any of the colour types.
'''
def flashing(colour):
    t = 200  # TIME POT
    col = colour()
    for pixel in range(0, len(np)):
        np[pixel] = col
    np.show()
    sleep(t)

def running(colour):
    t = 100  # TIME POT
    col = colour()
    for pixel in range(0, len(np)):
        np[pixel] = col
        np.show()
        sleep(t)

def random(colour):
    t = 200  # TIME POT
    col = colour()
    on_off = [col, (0, 0, 0)]
    for pixel in range(0, len(np)):
        np[pixel] = choice(on_off)
    np.show()
    sleep(t)


'''    
The following two functions control additional pattern types.
Instead of the colour functions, they take a specific r, g, b value as arguments.
This can be 60, 60, 60 or the r, g, b chosen by three potentiometers.
'''
def solid(r, g, b):  # either the pot values or 60,60,60
    col = g, r, b
    for pixel in range(0, len(np)):
        np[pixel] = col
    np.show()

# def fading(r, g, b):


while True:
    running(multi)
