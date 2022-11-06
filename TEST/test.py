# import numpy as np
# from matplotlib import pyplot as plt
# from matplotlib.collections import LineCollection, PolyCollection
#
# from skyfield.api import Star, load, wgs84, N, S, W, E
# from skyfield.data import hipparcos, mpc, stellarium
# # import dsos
# from skyfield.projections import build_stereographic_projection
# from datetime import datetime
# from pytz import timezone
#
# # time `t` we use for everything else.
#
# AMS = timezone('Europe/Amsterdam')
# ts = load.timescale()
# t = ts.from_datetime(AMS.localize(datetime(2021, 9, 12, 23, 0, 0)))
# # 180 = South 0 = North
# degrees = 0.0
#
#
# amsterdam = wgs84.latlon(52.377956*N, 4.897070*E, elevation_m=28).at(t)
# position = amsterdam.from_altaz(alt_degrees=90, az_degrees=degrees)
#
# # An ephemeris from the JPL provides Sun and Earth positions.
#
# eph = load('de421.bsp')
# sun = eph['sun']
# earth = eph['earth']
#
# # Center on Albireo middle of Summer Triangle
#
# albireo = Star(ra_hours=(19, 30, 45.40),
#                dec_degrees=(27, 57, 55.0))
#
# # The Hipparcos mission provides our star catalog.
#
# with load.open(hipparcos.URL) as f:
#     stardata = hipparcos.load_dataframe(f)
#
# # DSO's from stellarium
#
# with open('catalog.txt') as f:
#     dsodata = dsos.load_dataframe(f)
#
# # starnames
#
# with open('starnamesHIP.tsv') as f:
#     starnames = dsos.load_names(f)
#
# # And the constellation outlines come from Stellarium.  We make a list
# # of the stars at which each edge stars, and the star at which each edge
# # ends.
#
# url = ('https://raw.githubusercontent.com/Stellarium/stellarium/master'
#        '/skycultures/western_SnT/constellationship.fab')
#
# with load.open(url) as f:
#     consdata = stellarium.parse_constellations(f)
#
# url2 = ('https://raw.githubusercontent.com/Stellarium/stellarium/master'
#        '/skycultures/western_SnT/star_names.fab')
#
# with load.open(url2) as f2:
#     star_names = stellarium.parse_star_names(f2)
#
# summer_triangle = [
#     [   "Summer Triangle",
#         [
#             [102098, 91262],
#             [91262, 97649],
#             [97649, 102098]
#         ]
#     ]
# ]
#
#
# def generate_constellation_lines(data, polygon=False):
#     edges = [edge for name, edges in data for edge in edges]
#     edges_star1 = [star1 for star1, star2 in edges]
#     edges_star2 = [star2 for star1, star2 in edges]
#     xy1 = stardata[['x', 'y']].loc[edges_star1].values
#     xy2 = stardata[['x', 'y']].loc[edges_star2].values
#
#     if polygon:
#         return [xy1]
#     else:
#
#         # The constellation lines will each begin at the x,y of one star and end
#         # at the x,y of another.  We have to "rollaxis" the resulting coordinate
#         # array into the shape that matplotlib expects.
#
#         return np.rollaxis(np.array([xy1, xy2]), 1)
#
#
# # We will center the chart on the comet's middle position.
#
# center = earth.at(t).observe(albireo)
# #projection = build_stereographic_projection(center)
# projection = build_stereographic_projection(position)
# field_of_view_degrees = 180.0
# limiting_magnitude = 6.0
# dso_limit_magnitude = 8.0
#
# # Now that we have constructed our projection, compute the x and y
# # coordinates that each star will have on the plot.
#
# star_positions = earth.at(t).observe(Star.from_dataframe(stardata))
# stardata['x'], stardata['y'] = projection(star_positions)
#
# dso_positions = earth.at(t).observe(Star.from_dataframe(dsodata))
# dsodata['x'], dsodata['y'] = projection(dso_positions)
#
#
# # Create a True/False mask marking the stars bright enough to be
# # included in our plot.  And go ahead and compute how large their
# # markers will be on the plot.
#
# bright_stars = (stardata.magnitude <= limiting_magnitude)
# magnitude = stardata['magnitude'][bright_stars]
# marker_size = (0.7 + limiting_magnitude - magnitude) ** 2.0
#
# bright_dsos = (dsodata.magnitude <= dso_limit_magnitude)
# dso_magnitude = dsodata['magnitude'][bright_dsos]
# dso_size = (0.9 + dso_limit_magnitude - dso_magnitude) ** 2.0
#
# # Time to build the figure!
#
# fig, ax = plt.subplots(figsize=[12, 12])
#
# # Draw Horizon as dashed line
# # 24 points horizon
#
# horizon = []
# h0 = projection(amsterdam.from_altaz(alt_degrees=0, az_degrees=0.0))
# for i in range(1, 73):
#     delta = 5.0
#     current = i * delta
#     h1 = projection(amsterdam.from_altaz(alt_degrees=0, az_degrees=current))
#     horizon.append([h0, h1])
#     h0 = h1
#
# ax.add_collection(LineCollection(horizon,
#                          colors='#00f2', linewidths=1, linestyle='dashed', zorder=-1, alpha=0.5))
#
# # Draw the constellation lines.
#
# constellations = LineCollection(generate_constellation_lines(consdata),
#                                 colors='#00f2', linewidths=1, zorder=-1, alpha=0.5)
# ax.add_collection(constellations)
#
# # Draw the Summer Triangle lines.
#
# print(f"triangle poly = {generate_constellation_lines(summer_triangle, polygon=True)}")
# triangle = PolyCollection(generate_constellation_lines(summer_triangle, polygon=True), facecolors='orange',
#                           edgecolors='orange', alpha=0.5, linewidths=0, zorder=-2)
# ax.add_collection(triangle)
#
#
# # Draw the stars.
#
# ax.scatter(stardata['x'][bright_stars], stardata['y'][bright_stars],
#            s=marker_size, color='k')
#
# ax.scatter(dsodata['x'][bright_dsos], dsodata['y'][bright_dsos],
#            s=dso_size, color='red')
#
# # Finally, title the plot and set some final parameters.
#
# angle = np.pi - field_of_view_degrees / 360.0 * np.pi
# limit = np.sin(angle) / (1.0 - np.cos(angle))
#
# print(f"starnames = {starnames}")
# for i, s in stardata[bright_stars].iterrows():
#     if -limit < s['x'] < limit and -limit < s['y'] < limit:
#         if i in starnames:
#             print(f"star {starnames[i]} mag {s['magnitude']}")
#             ax.text(s['x'] + 0.004, s['y'] - 0.004, starnames[i], color='k',
#                     ha='left', va='top', fontsize=9, weight='bold', zorder=1).set_alpha(0.5)
#
# for i, d in dsodata[bright_dsos].iterrows():
#     if -limit < d['x'] < limit and -limit < d['y'] < limit:
#         print(f"dso {d['label']} mag {d['magnitude']}")
#         ax.text(d['x'] + 0.004, d['y'] - 0.004, d['label'], color='red',
#                 ha='left', va='top', fontsize=9, weight='bold', zorder=1).set_alpha(0.5)
#
#
# ax.set_xlim(-limit, limit)
# ax.set_ylim(-limit, limit)
# ax.xaxis.set_visible(True)
# ax.yaxis.set_visible(True)
# ax.set_aspect(1.0)
# ax.set_title(f"To the South in Amsterdam on {t.utc_strftime('%Y %B %d %H:%M')}")
#
# # Save.
#
# fig.savefig('summer-triangle.png', bbox_inches='tight')


#
# from skyfield.api import position_of_radec, load_constellation_map
# constellation_at = load_constellation_map()
# north_pole = position_of_radec(0, 90)
# x = constellation_at(north_pole)
# print(x)
# from skyfield.api import load_constellation_names
# d = dict(load_constellation_names())
# print(d['UMa'])



# from skyfield.api import Star, load
# from skyfield.data import hipparcos
# from matplotlib import pyplot as plt
# ts = load.timescale()
# fig, ax = plt.subplots()#(figsize=(100, 100))
#
# plt.style.use('dark_background')
# # plt.set(title=f'Stars in Orion constellation')
# ax.set_xlabel("right_ascension")
# ax.set_ylabel("declination")
# ax.set_ylim(-20, 20)
# ax.set_xlim(7.0, 4.0)
#
# with load.open(hipparcos.URL) as f:
#     df = hipparcos.load_dataframe(f)
# eph =load('de421.bsp')
# earth = eph['earth']
# df_visible = df[df['magnitude'] <= 5.0]
# bright_stars = Star.from_dataframe(df_visible)
#
# astrometric = earth.at(ts.now()).observe(bright_stars)
# ra, dec, distance = astrometric.radec()
# ax.scatter(ra.hours, dec.degrees, s= 8 - df_visible['magnitude'], c='red')
# print(type(df_visible))
# # a = []
# ax.add_line()
# # for i in df_visible['magnitude']:
# #     a.append(i)
#
# # ax.text(0, dec.degrees, s='aaa', c='blue', fontsize=12)
# plt.show()



#
# FULL WORKING PART

import skychart as sch
from datetime import datetime
import matplotlib.pyplot as plt

t = datetime.now()
obs_loc = (44.5, 40.1566)  #long lat  Yerevan

fig, ax, df = sch.draw(obs_loc, t, mag_max=5, alpha=0.3)
fig.savefig('now.png')
plt.show()
# ******************


# def is_valid_lat(lat: float) -> bool:
#     if -90 <= lat <= 90:
#         return True
#     else:
#         raise ValueError("Invalid latitude!!!") from None
#
#
# def is_valid_long(long: float) -> bool:
#     if -180 <= long <= 180:
#         return True
#     else:
#         raise ValueError("Invalid longitude!!!") from None
#     # return False
#
#
# def input_lonlat():
#     try:
#         lat = float(input("Latitude: "))
#         long = float(input("Longitude: "))
#     except ValueError:
#         raise ValueError("Enter Only Float Numbers!!!") from None
#     if is_valid_lat(lat) and is_valid_long(long):
#         return lat, long



# from datetime import datetime
# from geopy import Nominatim
# from tzwhere import tzwhere
# from pytz import timezone, utc
#
# from timezonefinder import TimezoneFinder
#
# obj = TimezoneFinder()
# latitude = 50
# longitude = 106
# now = datetime.utcnow()
# dt = datetime.now()
# print(now)
# print(dt)
# hour = dt.hour-4   # set utc time by current timezone(+4)
# dt = dt.replace(hour= hour)
# x = obj.timezone_at(lng=longitude, lat=latitude)
# print(x,x[-2:])
# # print(x,type(x))


















# def print_on_plain(stars):
#     chart_size = 10
#     max_star_size = 100
#     limiting_magnitude = 10
#
#     bright_stars = (stars.magnitude <= limiting_magnitude)
#     magnitude = stars['magnitude'][bright_stars]
#
#     fig, ax = plt.subplots(figsize=(chart_size, chart_size))
#     border = plt.Rectangle((-100,-100), 200, 200, color='black', fill=True)
#     ax.add_patch(border)
#     marker_size = max_star_size * 10 ** (magnitude / -2.5)
#     ax.scatter(stars['x'][bright_stars], stars['y'][bright_stars],
#                s=marker_size, color='blue', marker='.', linewidths=0,
#                zorder=2)
#     horizon = Circle((0, 0), radius=1, transform=ax.transData)
#     # horizon = Rectangle((-100, -100), 200, 200, transform=ax.transData)
#     # for col in ax.collections:
#     #     col.set_clip_path(horizon)
#
#     # other settings
#     ax.set_xlim(-1, 1)
#     ax.set_ylim(-1, 1)
#     plt.axis('off')
#     fig.savefig('sky.png')
#     plt.show()
# # def find_earth_sun_loc():
# #     eph = load('de421.bsp')
# #     # hipparcos dataset contains star location data
# #     with load.open(hipparcos.URL) as f:
# #         stars = hipparcos.load_dataframe(f)
# #     sun = eph['sun']
# #     earth = eph['earth']
#
# def get_stars_locations():
#     # hipparcos dataset contains star location data
#     with load.open(hipparcos.URL) as f:
#         stars = hipparcos.load_dataframe(f)
#     return stars
#
#
# def find_earth_loc():
#     eph = load('de421.bsp')
#     # sun = eph['sun']
#     return eph['earth']
#
#
# def run():
#     dt = datetime.now()
#     # lat, long = get_current_location(dt)
#     lat, long =40.0, 45.0
#     utc_dt = convert_time_to_utc(dt,long, lat)
#     stars = get_stars_locations()
#     t = define_observe_time_from_utc(utc_dt)
#     center_object = define_sky_obsrve_point(long, lat,t)
#     earth = find_earth_loc()
#     projection = get_projection_our_center(earth, t, center_object)
#     stars = calc_star_projection(earth, stars, projection, t)
#     print_on_plain(stars)
#
#
# run()

# x= u'\U0001f31e'
# x = '🌞'
# u = ord('🌞')
# print( "🪐".encode('utf-16'))
# print(	"\u2600")
# st = u"\u2600"  # sun
# st = u"\u263E"  #moon
# # print("🌐")
# st = '✹'
# print("\U0001f52d",)
# print("\U00002022") # dot




#
# def print_on_plain(stars, t, projection, eph,title):
#     chart_size = 10
#     fig, ax = plt.subplots(figsize=(chart_size, chart_size))
#     draw(ax, stars)
#     draw_planets_sun_moon("venus", ax, t, projection, eph)
#     draw_planets_sun_moon("mars", ax, t, projection, eph)
#     draw_planets_sun_moon("mercury", ax, t, projection, eph)
#     draw_planets_sun_moon("sun", ax, t, projection, eph)
#     draw_planets_sun_moon("moon", ax, t, projection, eph)
#     title = title[title.index('/')+1:]
#     plt.title(f"★STARRY SKY★\n{title}", fontsize=25)
#     ax.set_xlim(-1, 1)
#     ax.set_ylim(-1, 1)
#     plt.axis('off')
#     fig.savefig('sky.png')
#     plt.show()
