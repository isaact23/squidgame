SEG_COUNT = 29


# A container class for all Segments that are part of the game. This class also has an emulator.
class Grid:
    def __init__(self, controller):
        self.controller = controller
        self.segments = [
            controller.get_strip(0).get_segment(0, 20),
            controller.get_strip(1).get_segment(0, 20)
        ]
        for i in range(27):
            self.segments.append(controller.get_strip(2).get_segment(i * 20, (i + 1) * 20))
        self.segments[12] = controller.get_strip(3).get_segment(0, 20)
        self.segments[15] = controller.get_strip(4).get_segment(0, 20)
        self.segments[18] = controller.get_strip(5).get_segment(0, 20)
        self.segments[21] = controller.get_strip(6).get_segment(0, 20)
        self.segments[24] = controller.get_strip(7).get_segment(0, 20)

    def get_seg(self, segment):
        """
        Get one of the segments from this grid.
        :param segment: The segment index to get.
        :return: A Segment given by the index specified.
        :raises IndexError: When segment index is out of bounds.
        """
        if segment >= SEG_COUNT or segment < 0:
            raise IndexError("Segment index out of bounds")

        return self.segments[segment]

    def use_rule(self):
        """
        Tell all segments to update LEDs as per their functions.
        """
        for segment in self.segments:
            segment.use_rule()
        self.controller.write()
