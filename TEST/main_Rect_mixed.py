from datetime import datetime
from geopy import Nominatim
from tzwhere import tzwhere
from pytz import timezone, utc
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from skyfield.api import Star, load, wgs84
from skyfield.data import hipparcos
from skyfield.projections import build_stereographic_projection
# /////////////////////////////////////////////////////////////////////
from astropy.io import fits
import numpy as np
# Set up the HEALPix projection
from astropy_healpix import HEALPix
from astropy.coordinates import Galactic
from astropy import units as u
from astropy.coordinates import SkyCoord

import math
from astropy import units as u
from astropy_healpix import HEALPix

hp = HEALPix(nside=16, order='nested',frame=Galactic())
my_lon = 44.0
my_lat = 40.0
r = 10
# Sample a 300x200 grid in RA/Dec-  ոնց որ բաժանի -15 15ը 300 մասի
# ra = np.linspace(-15., 15.,300 ) * u.deg
# dec = np.linspace(-10., 10., 200) * u.deg
# ra_grid, dec_grid = np.meshgrid(ra, dec)
# coords = SkyCoord(ra_grid.ravel(), dec_grid.ravel(), frame='icrs')   #coordinat  (ra,dec), 200*300հատ

hp = HEALPix(nside=32, order='ring',frame=Galactic)
print()
# print(hp.cone_search_lonlat(my_lon * u.deg, my_lat * u.deg, radius=r * u.deg)) # lon lat
ra = 0
dec = 0
# loop for in ra dec and create sky coords
coords = SkyCoord(ra, dec, unit='deg')




# [1269 160 162 1271 1270 1268 1246 1247 138 139 161 1245 136 137
# 140 142 130 131 1239 1244 1238 1241 1243 1265 1267 1276 1273 1277
# 168 169 163 166 164]

