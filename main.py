# Squid Game - Glass Stepping Stones
# Code for LED strips, sound control, camera, etc.

# import neopixel, board
import colorsys, random, math, fpstimer
from time import perf_counter
import colors
import functions
from controller import Controller, LightStrip
from grid import Grid
from emulator import Emulator


def main():
    controller = Controller((20, 20, 1000))
    grid = Grid(controller)
    grid.get_seg(7).set_func(functions.fill(colors.RED))
    grid.get_seg(4).set_func(functions.animate(functions.stripes((colors.RED, colors.BLUE), 3), 15))
    grid.get_seg(2).set_func(functions.flip(functions.animate(functions.stripes((colors.RED, colors.BLUE), 3), 15)))

    # Begin emulation
    emulator = Emulator(grid)
    timer = fpstimer.FPSTimer(60)
    i = 0
    while True:
        grid.use_func()
        emulator.update()
        timer.sleep()


if __name__ == "__main__":
    main()
