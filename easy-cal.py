#!/usr/bin/env python

from piccal import PicCal
from PIL import Image

# @proportion tuple (w, h)
#   Desired proportion
# @size tuple (w, h)
#   Actual size
# return (x1, y1, x2, y2)
#   Croping box.
def GetCropBox(proportion, size):
    coefficient = min(size[0]/proportion[0], size[1]/proportion[1])
    tw, th = int(proportion[0] * coefficient), int(proportion[1] * coefficient)
    w, h = size
    return int((w - tw)/2), int((h - th)/2), int((w + tw)/2), int((h + th)/2)

# Template
# {
#   proportion: [w, h]
#   pending: px
#   box: [x1, y1, x2, y2] all in ratio.
# }

# Form calendar with preset template.
# 1. Crop image to desired proportion.
# 2. Describe calendar by percent.
# 3. Draw.
def MakeCalendarWithTemplate(font_file, year, mon,
                             template = None,
                             background_file = None):
    img = Image.open(background_file, 'r')
    im2 = img.crop(GetCropBox(template['proportion'], img.size))
    w, h = im2.size
    pc = PicCal(template['pending'], font_file,
                int(w * template['box'][0]),
                int(h * template['box'][1]),
                int(w * (template['box'][2] - template['box'][0])),
                int(h * (template['box'][3] - template['box'][1])),
                year, mon,
                img = im2);
    return pc.getImage()

# expected command:
# easy-cal.py [-stdout] <year> <mon> <font> <background_file>
if __name__ == "__main__":
    import sys

    temp = {
        "proportion": (16, 10),
        "pending": 10,
        "box": [0, 0, 0.5, 1]
    }

    argv = sys.argv[1:]
    to_stdout = False
    if argv[0] == '-stdout':
        to_stdout = True
        argv.pop(0)

    im = MakeCalendarWithTemplate(argv[2],          # Font file
                                  int(argv[0]),     # Year
                                  int(argv[1]),     # Month
                                  temp,             # Template
                                  argv[3])          # Background file.
    if to_stdout:
        im.save(sys.stdout, 'JPEG', quality=100)
    else:
        im.show()
