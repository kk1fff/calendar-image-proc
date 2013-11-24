#!/usr/bin/env python

from cal import Cal
from PIL import Image, ImageDraw

class PicCal:
    def __init__(self, padding_width, img_file_name, calx, caly,
                 font_file, calw, calh, year, mon):
        self._pw = padding_width
        self._img = Image.open(img_file_name, 'r')
        self._img.convert("RGBA")
        self._cx = calx
        self._cy = caly
        self._cw = calw
        self._ch = calh
        self._font_file = font_file
        self._y = year
        self._m = mon

    def drawPaddingBox(self):
        box_w = self._cw + self._pw * 2
        box_h = self._ch + self._pw * 2
        box_x = self._cx - self._pw
        box_y = self._cy - self._pw
        draw = ImageDraw.Draw(self._img)

        box_channel = Image.new('L', (box_w, box_h), 128)
        bc_draw = ImageDraw.Draw(box_channel)
        self._img.paste("white", (box_x, box_y, box_x + box_w, box_y + box_h), box_channel)

    def makeImage(self):
        self.drawPaddingBox()
        cal = Cal(self._font_file, self._cw, self._ch, self._y, self._m,
                       draw_on = self._img, draw_x = self._cx, draw_y = self._cy)
        cal.makeImage()

    def showImage(self):
        self.makeImage()
        self._img.show()

if __name__ == "__main__":
    # expected command: ./piccal.py <year> <month> <cal-width> <cal-height> <font file> <cal-x> <cal-y> <background-img>
    import sys
    year       = int(sys.argv[1])
    mon        = int(sys.argv[2])
    cal_width  = int(sys.argv[3])
    cal_height = int(sys.argv[4])
    font_file  = sys.argv[5]
    cal_x      = int(sys.argv[6])
    cal_y      = int(sys.argv[7])
    img_file   = sys.argv[8]

    pc = PicCal(10, img_file, cal_x, cal_y, font_file, cal_width, cal_height, year, mon);
    pc.showImage()
