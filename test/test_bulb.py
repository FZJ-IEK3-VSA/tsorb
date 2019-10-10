import numpy as np

from tsorb.Bulb import Bulb

def test_bulbs():

    bulbs = [None] * 10
    for i in range(10):
        b = Bulb("BULB_" + str(i), 10)
        bulbs[i] = b

    for bulb in bulbs:
        bulb.switch_on(0)
        print(bulb)
        print(bulb.consumption[0], bulb.consumption[1])
