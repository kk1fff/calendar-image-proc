#!/usr/bin/env python

from cal import Cal
from PIL import Image, ImageDraw

class PicCal:
    def __init__(self,
                 padding_width, font_file,
                 calx, caly,
                 calw, calh,
                 year, mon,
                 img_file_name = None,
                 img = None):
        print "Draw calendar at: ", calx, caly, calw, calh

        self._pw = padding_width

        if img_file_name != None:
            self._img = Image.open(img_file_name, 'r')
        elif img != None:
            self._img = img
        else:
            raise Exception("No img_file_name specified or img provided")

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
        cal = Cal(self._font_file,
                  self._cw - self._pw * 2, self._ch - self._pw * 2,
                  (self._y, self._m),
                  draw_on = self._img,
                  draw_x = self._cx + self._pw, draw_y = self._cy + self._pw)
        cal.makeImage()

    def getImage(self):
        self.makeImage()
        return self._img

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

    pc = PicCal(10, font_file,
                cal_x, cal_y,
                cal_width, cal_height,
                year, mon,
                img_file_name = img_file);
    pc.showImage()
