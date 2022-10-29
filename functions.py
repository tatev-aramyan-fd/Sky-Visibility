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

def get_current_time():
    return datetime.now()


def get_current_location(dt):
    location = 'Yerevan, Armenia'
    when = '2023-01-01 00:00'
    # convert date string into datetime object
    # dt = datetime.strptime(when, '%Y-%m-%d %H:%M')
    # dt = datetime.now()
    # get latitude and longitude of our location
    locator = Nominatim(user_agent='myGeocoder')
    location = locator.geocode(location)
    lat, long = location.latitude, location.longitude
    return long, lat


def convert_time_to_utc(dt):
    timezone_str = tzwhere.tzwhere().tzNameAt(40.1776245, 44.5126174)
    local = timezone(timezone_str)
    local_dt = local.localize(dt, is_dst=None)
    utc_dt = local_dt.astimezone(utc)
    return  utc_dt


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

