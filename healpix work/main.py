from astropy_healpix import HEALPix
from astropy.coordinates import Galactic, SkyCoord
from datetime import datetime
from astropy import units as u
from drawing import draw_sphere
import calculations as clc


def run():
    hp = HEALPix(nside=64, order='nested', frame=Galactic())
    dt = datetime.now()
    # long, lat = 44.503490, 40.177200  # Yerevan coords
    long, lat = clc.input_lonlat()
    utc_dt = clc.convert_time_to_utc(dt, long, lat)
    t = clc.define_observe_time_from_utc(utc_dt)
    my_ra, my_dec = clc.get_radec_from_my_loc(long, lat, t)

    visible_pixels = hp.cone_search_lonlat(
        my_ra * u.deg,
        my_dec * u.deg,
        radius=30 * u.deg
    )
    longitude, latitude = hp.healpix_to_lonlat(visible_pixels) * u.deg
    c = SkyCoord(longitude, latitude, frame='galactic').transform_to("icrs")
    ras = c.ra.degree
    decs = c.dec.degree
    ra_lst = clc.get_converted_data_lst(ras)
    dec_lst = clc.get_converted_data_lst(decs)
    my_ra = clc.format_ra(my_ra)
    draw_sphere(ra_lst, dec_lst, my_ra, my_dec)
    return visible_pixels


if __name__ == "__main__":
    print(run())
