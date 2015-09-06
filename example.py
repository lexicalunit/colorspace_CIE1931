#!/usr/bin/env python

import math
from random import randint


def xyY_from_rgb(rgb):
    """
        Returns CIE xyY colorspace given rgb values [0, 255].
        Y is brightness or luminance. The xy values are chromaticity.

    """
    norm = lambda i: i / 255.0
    rgb = tuple(norm(i) for i in rgb)
    gamma = lambda i: (i / 12.92 if i <= 0.04045
                       else math.pow((i + 0.055) / (1.0 + 1.055), 2.4))
    rgb = tuple(gamma(i) for i in rgb)
    XYZ = (rgb[0] * 0.649926 + rgb[1] * 0.103455 + rgb[2] * 0.197109,
           rgb[0] * 0.234327 + rgb[1] * 0.743075 + rgb[2] * 0.022598,
           rgb[0] * 0.000000 + rgb[1] * 0.053077 + rgb[2] * 1.035763)
    s = sum(XYZ)
    if s == 0:
        return (0, 0, 0)
    xyz = tuple(i / s for i in XYZ)
    return xyz[0:2] + (XYZ[1], )


def rgb_from_xyY(xyY):
    """
        Returns rgb colorspace values [0, 255] from CIE xyY colorspace.
        Y is brightness or luminance. The xy values are chromaticity.

    """
    xyz = xyY[0:2] + (1.0 - xyY[0] - xyY[1], )
    XYZ = (xyY[2] / xyz[1] * xyz[0],
           xyY[2],
           xyY[2] / xyz[1] * xyz[2])
    RGB = (XYZ[0] * 1.6117500 + XYZ[1] * -0.2028050 + XYZ[2] * -0.302298,
           XYZ[0] * -0.509057 + XYZ[1] * 1.41191000 + XYZ[2] * 0.0660705,
           XYZ[0] * 0.0260848 + XYZ[1] * -0.0723524 + XYZ[2] * 0.9620860)
    ungamma = lambda i: (i * 12.92 if i <= 0.000631995310323
                         else (1.0 + 1.055) * math.pow(i, 1.0 / 2.4) - 0.055)
    RGB = tuple(ungamma(i) for i in RGB)
    denorm = lambda i: int(round(255.0 * i))
    return tuple(denorm(i) for i in RGB)

if __name__ == '__main__':
    rgb = tuple(randint(0, 256) for _ in range(3))
    print rgb
    print rgb_from_xyY(xyY_from_rgb(rgb))
