# from datetime import datetime, timedelta
# from math import *
#
#
# def date_to_j_day() -> float:
#     day = timedelta(1)
#     julian_epoch = datetime(2000, 1, 1, 12)
#     j2000_jd = timedelta(2451545)
#     dt = datetime.now()
#
#     h = dt.hour - 4  # for Universal time. We are in GT+4 zone
#     julian_day = (dt.replace(hour=h) - julian_epoch + j2000_jd) / day
#
#     return julian_day
#
#
# def calc_j_time_centuries(julian_date: float) -> float:
#     return (julian_date - 2451545.0)/36525
#
#
# def is_valid_ra(ra: float):
#     if 0 <= ra <= 360:
#         return True
#     return False
#
#
# def is_valid_dec(dec: float):
#     if -90 <= dec <= 90:
#         return True
#     return False
#
#
#
#
# def get_inputs():
#
#     lat = int(input("Enter latitude in deg: "))
#     long = int(input("Enter longitude in deg: "))
#     dt = datetime.now()
#
#
# jd = date_to_j_day()
# print(jd)

# from skyfield.api
import skyfield
from skyfield.api import Star, load
from skyfield.data import hipparcos
# import matplotlib.pyplot as plt
from matplotlib import pyplot as pt
ts = load.timescale()

# setup graph
fig, plt = pt.subplots()
pt.style.use(['dark_background'])
plt.set(title=f'Stars in Orion brighter than magnitude 5')
plt.set_xlabel('right ascension')
plt.set_ylabel('declination')
plt.set_xlim(7.0, 4.0)
plt.set_ylim(-20, 20)
plt.grid(color='gray', linestyle='-', linewidth=.5)
pt.tight_layout()
fig.savefig('bright_stars.png')

# star catalog from Universal de strasburg
with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f)

# emphemris
eph = load('de421.bsp')
earth = eph['earth']

# filter out dim stars
df_visible = df[df['magnitude'] <= 5.0]
bright_stars = Star.from_dataframe(df_visible)

astrometric = earth.at(ts.now()).observe(bright_stars)
ra, dec, distance = astrometric.radec()
plt.scatter(ra.hours, dec.degrees, 8 - df_visible['magnitude'], 'w')

pt.show()