#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont
from calendar import monthrange
import datetime, math

class Cal:
    """
    Image is divided into several text boxes, each of them contains a single day
    or weekday names.
    """
    @staticmethod
    def getSingleTextBox(w, h):
        return w/7, h/7

    """
    We can draw on a existed image by passing the image through
    draw_on argument and specifying draw_x, draw_y for position of
    upper left of calendar
    """
    def __init__(self, font_file, width, height, year, month,
                 background="white", draw_on = None, draw_x = 0, draw_y = 0,
                 font_size = 0):
        self._year = year
        self._month = month
        self._h = height
        self._w = width
        self._bg = background
        self._font = ImageFont.truetype(font_file, font_size if font_size > 0
                                                             else int(height / 7 * 0.9) )
        self._bw, self._bh = Cal.getSingleTextBox(width, height)
        self._base_img =  draw_on
        self._x = draw_x
        self._y = draw_y
        self._img = None

    """
    Given box position and return the position where the text suppose to be at
    """
    def getPositionOfText(self, bx, by, text):
        w, h = self._font.getsize(text)
        x = (self._bw - w) / 2
        y = (self._bh - h) / 2
        return bx + x, by + y

    """
    Draw text into box located at x, y, in terms of box count.
        |  0 |  1 |  2 |  3 |  4 |  5 |  6 |
    ----+----+----+----+----+----+----+----+
      0 |    |    |
    ----+----+----+----
      1 |    |    |  <----- (2, 1)
    ...
    """
    def drawInBox(self, draw, x, y, text, color):
        x, y = self.getPositionOfText(self._x + x * self._bw,
                                      self._y + y * self._bh, text)
        draw.text((x, y), text, font=self._font, fill=color)

    def makeImage(self):
        if self._img != None:
            return
        if self._base_img != None:
            self._img = self._base_img
        else:
            self._img = Image.new('RGBA', (self._w, self._h), self._bg)
        img = self._img
        draw = ImageDraw.Draw(img)

        # Draw titles
        titles = ["S", "M", "T", "W", "T", "F", "S"]
        for i in range(0, 7):
            self.drawInBox(draw, i, 0, titles[i], "#000000")

        # Draw days
        first_weekday, days = monthrange(self._year, self._month)
        for i in range(0, days):
            linear_pos = i + (first_weekday + 1) % 7
            self.drawInBox(draw, linear_pos % 7, math.floor(linear_pos / 7) + 1, str(i + 1),
                           "#ff0000" if linear_pos % 7 == 0 or linear_pos % 7 == 6
                                     else "#000000")

    def getImage(self):
        self.makeImage()
        return self._img;

    def showImage(self):
        self.makeImage()
        self._img.show()

if __name__ == "__main__":
    # expected command: ./cal.py <year> <month> <cal-width> <cal-height> <font file>
    import sys
    year       = int(sys.argv[1])
    mon        = int(sys.argv[2])
    cal_width  = int(sys.argv[3])
    cal_height = int(sys.argv[4])
    font_file  = sys.argv[5]

    cal = Cal(font_file, cal_width, cal_height, year, mon, "white")
    cal.showImage()
