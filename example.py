from bdc import calcBDC
# from utils import get_incline_compensation
# from utils import get_cant_compensation
# import math


# The ballistic coefficient for the projectile.
bc = 0.269
# Intial velocity, in m/s
v = 1006 #807.110400000768
# The Sight height over bore, in cm.
sh = 3.81
# The zero range of the rifle, in meters.
zero = 46#91.4399998610112
#
drag_function = "G1"
#metry ogległośćod celu
computationMeters = 150
# The wind speed in miles per hour.
windspeed = 10
# The wind angle (0=headwind, 90=right to left, 180=tailwind, 270/-90=left to right)
windangle = -90

moa_correction_vertical, moa_correction_horizontal = calcBDC(bc, v, sh, zero, drag_function, computationMeters, windspeed, windangle)
print("MOA Góra-dół: ", moa_correction_vertical)
print("MOA prawo-lewo: ", moa_correction_horizontal)

