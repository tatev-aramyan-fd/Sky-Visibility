<<<<<<< HEAD
from datetime import datetime
from tzwhere import tzwhere
from pytz import timezone, utc
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.collections import LineCollection
# from matplotlib.patches import Circle, Rectangle
=======
from tzwhere import tzwhere
from pytz import timezone, utc
>>>>>>> chart_drawing

from skyfield.api import Star, load, wgs84
from skyfield.data import hipparcos
from skyfield.projections import build_stereographic_projection


def convert_time_to_utc(dt, long, lat):
    try:
        timezone_str = tzwhere.tzwhere(forceTZ=True).tzNameAt(lat, long, forceTZ=True)
    except ValueError:
        raise ValueError("Unknown timezone, correct your location!!!") from None
    local = timezone(timezone_str)
    local_dt = local.localize(dt, is_dst=None)
    utc_dt = local_dt.astimezone(utc)
    print(timezone_str,long,lat)
    return utc_dt, timezone_str


def input_lonlat():
    try:
        lat = float(input("Latitude: "))
        long = float(input("Longitude: "))
    except ValueError:
        raise ValueError("Enter Only Float Numbers!!!") from None
    if is_valid_lat(lat) and is_valid_long(long):
        return lat, long


def is_valid_lat(lat: float) -> bool:
    if -90 <= lat <= 90:
        return True
    else:
        raise ValueError("Invalid latitude!!!") from None


def is_valid_long(long: float) -> bool:
    if -180 <= long <= 180:
        return True
    else:
        raise ValueError("Invalid longitude!!!") from None
    # return False


def define_observe_time_from_utc(utc_dt):
    ts = load.timescale()
    t = ts.from_datetime(utc_dt)
    print((type(t)))
    return t


<<<<<<< HEAD
def define_sky_obsrve_point(long, lat, t):
    # define an observer using the world geodetic system data
    observer = wgs84.latlon(latitude_degrees=lat, longitude_degrees=long).at(t)
    # define the position in the sky where we will be looking
    # position = observer.from_altaz(alt_degrees=90, az_degrees=0)
=======
def is_valid_lat(lat: float) -> bool:
    if -90 <= lat <= 90:
        return True
    else:
        raise ValueError("Invalid latitude!!!") from None


def is_valid_long(long: float) -> bool:
    if -180 <= long <= 180:
        return True
    else:
        raise ValueError("Invalid longitude!!!") from None


def input_lonlat():
    try:
        lat = float(input("Latitude: "))
        long = float(input("Longitude: "))
    except ValueError:
        raise ValueError("Enter Only Float Numbers!!!") from None
    if is_valid_lat(lat) and is_valid_long(long):
        return lat, long


def define_sky_obsrve_point(long, lat,t):
    # define an observer using the world geodetic system data
    observer = wgs84.latlon(latitude_degrees=lat, longitude_degrees=long).at(t)
>>>>>>> chart_drawing
    # center the observation point in the middle of the sky
    ra, dec, distance = observer.radec()
    center_object = Star(ra=ra, dec=dec)
    return center_object


def get_projection_our_center(earth, t, center_object):
    center = earth.at(t).observe(center_object)
    projection = build_stereographic_projection(center)
    return projection


def calc_star_projection(earth, stars, projection, t):
    # calculate star positions and project them onto a plain space
    star_positions = earth.at(t).observe(Star.from_dataframe(stars))
    stars['x'], stars['y'] = projection(star_positions)

    return stars


def get_stars_locations():
    with load.open(hipparcos.URL) as f:
        stars = hipparcos.load_dataframe(f)
    return stars



