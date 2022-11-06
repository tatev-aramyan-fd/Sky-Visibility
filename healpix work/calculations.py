from skyfield.api import load, wgs84
from tzwhere import tzwhere
from pytz import timezone, utc


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


def format_ra(ra:float):
    if ra > 180:
        return ra - 360
    return ra

def get_values_from_Quantity_obj(obj):
    value_lst = []
    for i in obj:
        a = format_ra(i.value)
        value_lst.append(a)
    return value_lst


def get_radec_from_my_loc(long:float, lat:float, t) -> tuple:

    observer = wgs84.latlon(latitude_degrees=lat, longitude_degrees=long).at(t)
    ra, dec, distance = observer.radec()
    return ra._degrees, dec._degrees


def define_observe_time_from_utc(utc_dt):
    ts = load.timescale()
    t = ts.from_datetime(utc_dt)
    return t


def convert_time_to_utc(dt, long, lat):
    try:
        timezone_str = tzwhere.tzwhere(forceTZ=True).tzNameAt(lat, long, forceTZ=True)
    except ValueError:
        raise ValueError("Unknown timezone, correct your location!!!") from None
    local = timezone(timezone_str)
    local_dt = local.localize(dt, is_dst=None)
    utc_dt = local_dt.astimezone(utc)
    return utc_dt

