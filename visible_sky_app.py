from chart_drawing import print_on_plain
from datetime import datetime
import calculations as clc


def run():
    eph = clc.load('de421.bsp')
    dt = datetime.now()
    # lat, long = 40.177200, 44.503490  # Yerevan coords
    lat, long = clc.input_lonlat()

    utc_dt = clc.convert_time_to_utc(dt, long, lat)
    stars = clc.get_stars_locations()
    t = clc.define_observe_time_from_utc(utc_dt[0])
    center_object = clc.define_sky_obsrve_point(long, lat, t)
    earth = eph['earth']
    projection = clc.get_projection_our_center(earth, t, center_object)
    stars = clc.calc_star_projection(earth, stars, projection, t)
    print_on_plain(stars, t, projection, eph, utc_dt[1])


run()

