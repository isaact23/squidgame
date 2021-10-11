import functions

# A controller for all of the LED strips.
class Controller:
    def __init__(self, strip_sizes):
        """
        Create a controller with LED strips turned off.
        :param strip_sizes: a tuple listing the sizes of all connected LED strips (e.g. (150, 150, 50)).
        """
        self.strips = {}
        for i, size in enumerate(strip_sizes):
            self.strips[i] = LightStrip(self, size)

    def get_strip(self, strip):
        """
        :param strip: The index of the LightStrip to access.
        :return: The LightStrip object in the specified index.
        """
        return self.strips[strip]

    def write(self):
        """
        # Send all pixel data to LED strips.
        """
        for i in self.strips:
            self.strips[i].write()


# An LED strip.
class LightStrip:
    def __init__(self, controller, size):
        """
        :param controller: The Controller object this LED strip is assigned to.
        :param size: The number of LEDs on this strip.
        """
        self.controller = controller
        self.size = size
        self.pixels = [(0, 0, 0)] * size
        self.func = None  # Color generation anonymous function
        # self.neopixel = neopixel.NeoPixel(board.D18, 150, auto_write=False)

    def get_segment(self, start, end):
        """
        Generate a Segment, which controls only some of the pixels on this LightStrip.
        :param start: The first pixel to control (inclusive).
        :param end: The last pixel to control (exclusive).
        :return: A Segment object with control over the specified pixels.
        :raises IndexError: If start or end are outside the bounds of this LightStrip.
        """
        # Assert start/end are within the bounds of this strip.
        if start < 0 or end > self.size:
            raise IndexError("Attempted to create a Segment outside the bounds of a LightStrip")

        return self.Segment(self, start, end)

    def set_func(self, f):
        """
        Set a function for LED color generation to be used on every use_func() call.
        :param f: The anonymous function.
        """
        self.func = f

    def use_func(self):
        """
        Apply the function set by set_func() to generate LED strip colors on this LightStrip.
        """
        if self.func is not None:
            self.apply_func(self.func, 0, self.size)

    def apply_func(self, f, start, end):
        """
        Apply an anonymous function to generate colors for LEDs on this LightStrip between start and end.
        :param f: The anonymous function to use.
        :param start: The first pixel (inclusive) to modify.
        :param end: The final pixel (exclusive) to modify.
        """
        for i in range(start, end):
            self.pixels[i] = f(pixel=i, strip_size=self.size)

    def get_pixels(self):
        """
        :return: An array of colors for each pixel on this LightStrip.
        """
        return self.pixels

    def write(self):
        """
        Send pixel data to this LED strip.
        """
        pass

    # A segment of pixels, defined by the start and end pixels of one of the light strips.
    class Segment:
        def __init__(self, strip, start, end):
            """
            Initialize a new segment. If end is less than start, flip the Segment.
            :param strip: The strip object this array lies on.
            :param start: The first pixel to activate
            :param end: The last pixel to activate
            """
            self.strip = strip
            self.start = start
            self.end = end
            if self.end < self.start:
                temp = self.end
                self.end = self.start
                self.start = temp
                self.flip = True
            else:
                self.flip = False
            self.func = None

        def func(self, f):
            """
            Apply an anonymous function to generate colors for LEDs on this Segment.
            :param f: The anonymous function to use.
            """
            self.strip.func(f, self.start, self.end)

        def set_func(self, f):
            """
            Set a function for LED color generation to be used on every use_func() call.
            :param f: The anonymous function.
            """
            if self.flip:
                self.func = functions.flip(f)
            else:
                self.func = f

        def use_func(self):
            """
            Apply the function set by set_func() to generate LED strip colors on this Segment.
            """
            if self.func is not None:
                self.strip.apply_func(self.func, self.start, self.end)

        def get_pixels(self):
            """
            :return: An array of colors for each pixel on this Segment.
            """
            return self.strip.get_pixels()[self.start:self.end]

        def size(self):
            """
            :return: The number of LEDs this Segment controls.
            """
            return self.end - self.start
