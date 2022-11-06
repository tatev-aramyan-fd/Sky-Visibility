import numpy as np
import matplotlib.pyplot as plt
np.random.seed(1234)
(RA, Dec)=(np.random.rand(100)*60 for _ in range(2))
arr = np.ndarray((10,20))
ar = np.ndarray((45,0))

print(type(RA))
# Creating projection
projection='mollweide'
fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(111, projection=projection)

# ax.scatter(np.radians(RA),np.radians(Dec))
# ax.scatter(1,45,c='red')
# Creating axes
xtick_labels = ["$150^{\circ}$", "$120^{\circ}$", "$90^{\circ}$", "$60^{\circ}$", "$30^{\circ}$", "$0^{\circ}$",
                "$330^{\circ}$", "$300^{\circ}$", "$270^{\circ}$", "$240^{\circ}$", "$210^{\circ}$"]

ytick_labels = ["$-75^{\circ}$", "$-60^{\circ}$", "$-45^{\circ}$", "$-30^{\circ}$", "$-15^{\circ}$",
                "$0^{\circ}$","$15^{\circ}$", "$30^{\circ}$", "$45^{\circ}$", "$60^{\circ}$",
                "$75^{\circ}$"]
#
# ax.set_yticklabels(ytick_labels,fontsize=12)
# labels = ax.set_xticklabels(xtick_labels, fontsize=15)
# # ax.set_xticklabels([1,47])
# # ax.set_yticklabels([0,0])
# ax.set_xlabel("RA")
# ax.xaxis.label.set_fontsize(20)
# ax.set_ylabel("Dec")
# ax.yaxis.label.set_fontsize(20)
# ax.grid(True)
# plt.axis('on')
# plt.show()




import matplotlib.pyplot as plt
import numpy as np
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
r = 0.05
u, v = np.mgrid[0:2 * np.pi:30j, 0:np.pi:20j]
x = np.cos(u) * np.sin(v)
y = np.sin(u) * np.sin(v)
z = np.cos(v)
ax.plot_surface(x, y, z)
plt.show()


# ////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////

# import matplotlib.pyplot as plt
# import numpy as np
# plt.rcParams["figure.figsize"] = [7.00, 3.50]
# plt.rcParams["figure.autolayout"] = True
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# r = 0.05
# u, v = np.mgrid[0:2 * np.pi:30j, 0:np.pi:20j]
# x = np.cos(u) * np.sin(v)
# y = np.sin(u) * np.sin(v)
# z = np.cos(v)
# ax.plot_surface(x, y, z)
# plt.show()


# ra dec to galactic
# from astropy import units as u
# from astropy.coordinates import SkyCoord
# from astropy_healpix import HEALPix
# from datetime import datetime
# from funcs import *
#
# hp = HEALPix(nside=4, order='nested')
# dt = datetime.now()
# lat, long = 40.177200, 44.503490
# utc_dt = convert_time_to_utc(dt, long, lat)
# t = define_observe_time_from_utc(utc_dt)
# ra, dec = f(long,lat,t)
# # print(type(ra),type(dec))
# # print(ra,dec)
# # # glat = SkyCoord(ra=ra, dec=ra, unit=(u.degree, u.degree)).galactic
# # print(glat.l)
#
















def run():
    hp = HEALPix(nside=64, order='nested', frame=Galactic())
    dt = datetime.now()
    lat, long = 40.177200, 44.503490  # Yerevan coords
    # lat, long = clc.input_lonlat()
    utc_dt = convert_time_to_utc(dt, long, lat)
    t = define_observe_time_from_utc(utc_dt)
    my_ra, my_dec = get_radec_from_my_loc(long, lat, t)

    visible_pixels = hp.cone_search_lonlat(
        my_ra * u.deg,
        my_dec * u.deg,
        radius=30 * u.deg
    )
    lon, lat = hp.healpix_to_lonlat(visible_pixels) * u.deg  # long[]  lat[]
    ra_lst = get_values_from_Quantity_obj(lon)
    dec_lst = get_values_from_Quantity_obj(lat)
    # my_ra = format_ra(my_ra)
    draw_sphere(ra_lst, dec_lst,40.177200, 44.503490)
    return visible_pixels



