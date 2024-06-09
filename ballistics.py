
import windage
import constants
import angles
import math
import drag
import utils
from holdover import holdover
from points import points
from math import log, degrees, atan, e
from utils import metersToYards


def solve(drag_function, drag_coefficient, vi, sight_height, shooting_angle, zero_angle, wind_speed, wind_angle, computationMeters):

    t = 0
    dt = 0
    v = 0
    vx = 0
    vx1 = 0
    vy = 0
    vy1 = 0
    dv = 0
    dvx = 0
    dvy = 0
    x = 0
    y = 0


    computationYards = metersToYards(computationMeters)

    hwind = windage.headwind(wind_speed, wind_angle)
    cwind = windage.crosswind(wind_speed, wind_angle)

    gy = constants.GRAVITY * \
        math.cos(angles.deg_to_rad((shooting_angle + zero_angle)))

    gx = constants.GRAVITY * \
        math.sin(angles.deg_to_rad((shooting_angle + zero_angle)))

    vx = vi * math.cos(angles.deg_to_rad(zero_angle))
    vy = vi * math.sin(angles.deg_to_rad(zero_angle))

    # y is in feet
    y = -sight_height/12

    n = computationYards

    hold_overs = points()


    while True:
        vx1 = vx
        vy1 = vy
        v = math.pow(math.pow(vx, 2)+math.pow(vy, 2), 0.5)
        dt = 0.5/v

        # Compute acceleration using the drag function retardation
        dv = drag.retard(drag_function, drag_coefficient, v+hwind)
        dvx = -(vx/v)*dv
        dvy = -(vy/v)*dv

        # Compute velocity, including the resolved gravity vectors.
        vx = vx + dt*dvx + dt*gx
        vy = vy + dt*dvy + dt*gy

        if x/3 >= n:

            if x > 0:
                # range_yards = round(x/3)
                # print("range_yards {}".format(range_yards))
                # # if range_yards == 400:
                moa_correction = -angles.rad_to_moa(math.atan(y / x))
                # liczenie odchylenia w poziomie //todo skalibrowac dla pocisku
                if(cwind>0):
                    B = 0.045289 * cwind + 0.000011
                    correction_horizontal = t * cwind - 5000 / 313 * B * log(5000 * B + 313 * t * cwind, e) + 5000 / 313 * B * log(5000 * B, e)
                    moa_correction_horizontal = 60 * degrees(atan(correction_horizontal / computationMeters))
                else:
                    cwind*=-1
                    B = 0.045289 * cwind + 0.000011
                    correction_horizontal = t * cwind - 5000 / 313 * B * log(5000 * B + 313 * t * cwind, e) + 5000 / 313 * B * log(5000 * B, e)
                    moa_correction_horizontal = 60 * degrees(atan(correction_horizontal / computationMeters))
                    moa_correction_horizontal *= -1
                return moa_correction, moa_correction_horizontal
                # path_inches = y*12
                # print("path_inches {}". format(path_inches))
                # impact_in = utils.moaToInch(moa_correction, x)
                # seconds = t+dt
                # print("seconds {}". format(seconds))
                # hold_overs.add_point(
                #     holdover(range_yards, moa_correction, impact_in, path_inches, seconds))
                # print("\n")
            n = n + 1

        # Compute position based on average velocity.
        x = x + dt * (vx+vx1)/2
        y = y + dt * (vy+vy1)/2

        if (math.fabs(vy) > math.fabs(3*vx) or n >= computationYards + 1):
            break

        t = t + dt

    return hold_overs
