from datetime import datetime
from geopy import Nominatim
from tzwhere import tzwhere
from pytz import timezone, utc

# import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, Rectangle

from skyfield.api import Star, load, wgs84
from skyfield.data import hipparcos
from skyfield.projections import build_stereographic_projection


# def get_current_location(dt):
#     location = 'Yerevan, Armenia'
#     # location = input('Enter your location name')
#     when = '2023-01-01 00:00'
#     # convert date string into datetime object
#     # get latitude and longitude of our location
#     locator = Nominatim(user_agent='myGeocoder')
#     location = locator.geocode(location)
#     lat, long = location.latitude, location.longitude
#     return long, lat


def convert_time_to_utc(dt, long, lat):
    # timezone_str = tzwhere.tzwhere().tzNameAt(40.1776245, 44.5126174)

    timezone_str = tzwhere.tzwhere().tzNameAt(lat, long)
    local = timezone(timezone_str)
    local_dt = local.localize(dt, is_dst=None)
    utc_dt = local_dt.astimezone(utc)
    print(timezone_str,long,lat)
    return utc_dt


def define_observe_time_from_utc(utc_dt):
    ts = load.timescale()
    t = ts.from_datetime(utc_dt)
    return t

def define_sky_obsrve_point(long, lat,t):
    # define an observer using the world geodetic system data
    observer = wgs84.latlon(latitude_degrees=lat, longitude_degrees=long).at(t)
    # define the position in the sky where we will be looking
    position = observer.from_altaz(alt_degrees=90, az_degrees=0)
    # center the observation point in the middle of the sky
    ra, dec, distance = observer.radec()
    center_object = Star(ra=ra, dec=dec)
    return center_object


def get_projection_our_center(earth, t, center_object):
    center = earth.at(t).observe(center_object)
    projection = build_stereographic_projection(center)
    # field_of_view_degrees = 180.0
    return projection


def calc_star_projection(earth, stars, projection, t):
    # calculate star positions and project them onto a plain space
    star_positions = earth.at(t).observe(Star.from_dataframe(stars))
    stars['x'], stars['y'] = projection(star_positions)
    # print(stars)
    return stars
