from astropy_healpix import HEALPix
from astropy.coordinates import Galactic
from datetime import datetime
import calculations as clc
from astropy import units as u
from drawing import *


def run():
    hp = HEALPix(nside=64, order='nested', frame=Galactic())
    dt = datetime.now()
    # lat, long = 40.177200, 44.503490  # Yerevan coords
    lat, long = clc.input_lonlat()
    utc_dt = clc.convert_time_to_utc(dt, long, lat)
    t = clc.define_observe_time_from_utc(utc_dt)
    my_ra, my_dec = clc.get_radec_from_my_loc(long, lat, t)

    visible_pixels = hp.cone_search_lonlat(
        my_ra * u.deg,
        my_dec * u.deg,
        radius=30 * u.deg
    )
    lon, lat = hp.healpix_to_lonlat(visible_pixels) * u.deg  # long[]  lat[]
    ra_lst = clc.get_values_from_Quantity_obj(lon)
    dec_lst = clc.get_values_from_Quantity_obj(lat)
    draw_sphere(ra_lst, dec_lst,40.177200, 44.503490)
    return visible_pixels










run()