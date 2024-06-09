import atmosphere
import angles
import ballistics
from utils import metersToFeet, cmToInches, metersToYards


def calcBDC(bc, v, sh, zero, drag_function, computationMeters):
    # k = 0

    v = metersToFeet(v)
    sh = cmToInches(sh)
    zero = metersToYards(zero)
    computationYards = metersToYards(computationMeters)

    # The shooting angle (uphill / downhill), in degrees.
    angle = 0

    # The wind speed in miles per hour.
    windspeed = 0
    # The wind angle (0=headwind, 90=right to left, 180=tailwind, 270/-90=left to right)
    windangle = 0

    altitude = 109.3
    barometer = 29.5  # cale słupka rtęci
    temperature = 68
    relative_humidity = 0.8



    # If we wish to use the weather correction features, we need to
    # Correct the BC for any weather conditions.  If we want standard conditions,
    # then we can just leave this commented out.

    bc = atmosphere.atmosphere_correction(
        bc, altitude, barometer, temperature, relative_humidity)
    #
    # print("bc {}".format(bc))

    # First find the angle of the bore relative to the sighting system.
    # We call this the "zero angle", since it is the angle required to
    # achieve a zero at a particular yardage.  This value isn't very useful
    # to us, but is required for making a full ballistic solution.
    # It is left here to allow for zero-ing at altitudes (bc) different from the
    # final solution, or to allow for zero's other than 0" (ex: 3" high at 100 yds)
    zeroangle = angles.zero_angle(drag_function, bc, v, sh, zero, 0)

    # Now we have everything needed to generate a full solution.
    # So we do.  The solution is stored in the pointer "sln" passed as the last argument.
    # k has the number of yards the solution is valid for, also the number of rows in the solution.
    hold_overs = ballistics.solve(drag_function, bc, v, sh, angle,
                                  zeroangle, windspeed, windangle, computationYards)

    return hold_overs
