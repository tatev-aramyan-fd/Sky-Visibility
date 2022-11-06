from datetime import datetime
from geopy import Nominatim
from tzwhere import tzwhere
from pytz import timezone, utc

# import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, Rectangle
import pandas as pd
from skyfield.api import Star, load, wgs84
from skyfield.data import hipparcos
from skyfield.projections import build_stereographic_projection


# load celestial data
# de421 shows position of earth and sun in space
eph = load('de421.bsp')
# hipparcos dataset contains star location data
with load.open(hipparcos.URL) as f:
    stars = hipparcos.load_dataframe(f)
    print(type(stars))
# ++++++++++
location = 'New York'
when = '2023-01-01 00:00'
# convert date string into datetime object
# dt = datetime.strptime(when, '%Y-%m-%d %H:%M')
dt = datetime.now()
# get latitude and longitude of our location
locator = Nominatim(user_agent='myGeocoder')
location = locator.geocode(location)
lat, long = location.latitude, location.longitude
#
# timezone_str = tzwhere.tzwhere().tzNameAt(lat, long)
timezone_str = tzwhere.tzwhere().tzNameAt(40.1776245, 44.5126174)
local = timezone(timezone_str)
local_dt = local.localize(dt, is_dst=None)
utc_dt = local_dt.astimezone(utc)


# hour = dt.hour-4   # set utc time by current timezone(+4)
# dt = dt.replace(hour= hour)

# find location of earth and sun and set the observer position
sun = eph['sun']
earth = eph['earth']


# for i in :
#     print(i)
# define observation time from our UTC datetime
ts = load.timescale()
t = ts.from_datetime(utc_dt)
# define an observer using the world geodetic system data
observer = wgs84.latlon(latitude_degrees=lat, longitude_degrees=long).at(t)
# define the position in the sky where we will be looking
position = observer.from_altaz(alt_degrees=90, az_degrees=0)
# center the observation point in the middle of the sky
ra, dec, distance = observer.radec()
center_object = Star(ra=ra, dec=dec)


# find where our center object is relative to earth and build a projection with 180 degree view
center = earth.at(t).observe(center_object)
projection = build_stereographic_projection(center)
field_of_view_degrees = 60.0
# calculate star positions and project them onto a plain space
star_positions = earth.at(t).observe(Star.from_dataframe(stars))

print('++++++++', type(Star.from_dataframe(stars)), Star.from_dataframe(stars))
stars['x'], stars['y'] = projection(star_positions)
#



chart_size = 10
max_star_size = 100
limiting_magnitude = 10

bright_stars = (stars.magnitude <= limiting_magnitude)
magnitude = stars['magnitude'][bright_stars]

fig, ax = plt.subplots(figsize=(chart_size, chart_size))
border = plt.Rectangle((-100, -100), 400, 200, color='black', fill=True)
ax.add_patch(border)
marker_size = max_star_size * 10 ** (magnitude / -2.5)
ax.scatter(stars['x'][bright_stars], stars['y'][bright_stars],
           s=marker_size, color='blue', marker='.', linewidths=0,
           zorder=2)
# plnetsPLANETS0000000000000000000000000000000000000000000000000000000
mars = eph['mars']
mars_position = earth.at(t).observe(mars)  #
stars['mr'],stars['md'] = projection(mars_position)#
sun = eph['sun']
sun_position = earth.at(t).observe(sun)
stars['sr'],stars['sd'] = projection(sun_position)#
moon = eph['URANUS BARYCENTER']
moon_position = earth.at(t).observe(moon)
stars['r'],stars['d'] = projection(moon_position)#
df =  pd.DataFrame(['planets'])
# df['x'],df['y'] = projection(mars_position)
x,y =projection(mars_position)
print(df)
ax.scatter(x, y,s=100, color='yellow', marker='.')
ax.text(x, y, s='Sun',fontsize=15, c="yellow")
# ax.scatter(stars['mr'][bright_stars], stars['md'][bright_stars],
#            s=marker_size, color='red', marker='.', linewidths=0,
#            zorder=2)
# ax.scatter(stars['sr'][bright_stars], stars['sd'][bright_stars],
#            s=marker_size, color='yellow', marker='s', linewidths=0,
#            zorder=2)
# ax.scatter(stars['r'][bright_stars], stars['d'][bright_stars],
#            s=marker_size, color='green', marker='.', linewidths=0,
#            zorder=2)
# print(stars)
# 000000000000000000000000000000000000000000000000000000000000000000000
# print(stars)
# ax.text(stars['x'][bright_stars], stars['y'][bright_stars],
#            s=str(stars['epoch_year']), color='blue', fontsize=20)
# ax.text(0,0, s='Hello', fontdict=None, fontsize=25, c= "green")
# ax.scatter(0,0,s= 30, color='red',marker='.', linewidths=0,
#            zorder=2)




# astrometric = earth.at(t).observe(mars)
# ra, dec, distance = astrometric.radec()

# print(ra)
# print(dec)
# ax.scatter(stars['x'][bright_stars], stars['y'][bright_stars],
#            s=marker_size, color='blue', marker='.', linewidths=0,
#            zorder=2)
horizon = Circle((0, 0), radius=1, transform=ax.transData)
# horizon = Rectangle((-50, -50), 100, 100, transform=ax.transData)
# for col in ax.collections:
#     col.set_clip_path(horizon)


# other settings
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_xlabel("ssssss")
plt.axis('on')
fig.savefig('sky.png')
plt.show()












#
# # Սա մենակ հիմայի համարա անում. ու կոորդինատ պետք չի
# from datetime import datetime
# import pytz
# # Get current time in local timezone
# local_dt = datetime.now()
# print('Current Local Time: ', local_dt)
# # Convert local to UTC timezone
# dt_utc = local_dt.astimezone(pytz.UTC)
# print('Current time in UTC Time-zone: ', dt_utc)