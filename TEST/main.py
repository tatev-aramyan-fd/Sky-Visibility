from astropy.io import fits
# import astropy_healpix as hp
# import matplotlib.pyplot as plt
# import numpy as np
from astropy.coordinates import Galactic
# import healpy
# m42 = fits.open('frame-u-006073-4-0063new.fits')
# print(m42)

# sphere_pixel = hp.HEALPix(1024, 'ring')  # must be power of 2
#
# print(sphere_pixel.npix)   # 12*nside*nside  -> 16*16*12=3072
# lon, lat = hp.healpix_to_lonlat([1, 442, 2200], 32)
# print(lon.hourangle, '\n', lat.degree)
# from astropy_healpix import HEALPix
# from astropy.coordinates import Galactic
# hp = HEALPix(nside=16, order='nested', frame=Galactic())



# section of a sky map.....**************************************************************************-\
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
# Set up the HEALPix projection
from astropy_healpix import HEALPix
from astropy.coordinates import Galactic
from astropy import units as u
from astropy.coordinates import SkyCoord

# hdulist
fitss= fits.open('https://lambda.gsfc.nasa.gov/data/map/dr3/skymaps/5yr//wmap_band_imap_r9_5yr_K_v3.fits')
# fitss = fits.open("FITS/full_TQU.fits")
# nside = hdulist[1].header['NSIDE']
# order = hdulist[1].header['ORDERING']

# print(fitss[1].header)
# print('*****************')
# print(hdulist[1].header)
# nside = hdulist[1].header['NSIDE']
# order = hdulist[1].header['ORDERING']
# print(nside, order)
nside = fitss[1].header['NSIDE']
order = fitss[1].header['ORDERING'] #Ring 128
# print('*****************')
# print(nside,order, type(nside))
hp = HEALPix(nside=nside, order=order, frame=Galactic())

# Sample a 300x200 grid in RA/Dec

ra = np.linspace(-15., 15.,300 ) * u.deg
dec = np.linspace(-10., 10., 200) * u.deg

# print(ra, type(ra))
ra_grid, dec_grid = np.meshgrid(ra, dec)
# print( ra,'**********')
# Set up Astropy coordinate objects
coords = SkyCoord(ra_grid.ravel(), dec_grid.ravel(), frame='icrs')   #coordinat  (ra,dec), 200*300հատ
print(ra_grid.ravel(), type(ra_grid.ravel()))
temperature = fitss[1].data['temperature']


tmap = hp.interpolate_bilinear_skycoord(coords, temperature)
tmap = tmap.reshape(200, 300)

plt.figure(figsize=(9, 5))
im = plt.imshow(tmap, extent=[-10, 10, -10, 10], cmap=plt.cm.RdBu, origin='lower', aspect='auto')# tmap nd array, extent->box
plt.colorbar(im)
plt.xlabel('Right ascension (ICRS)')
plt.ylabel('Declination (ICRS)')
plt.show()

# # section of a sky map.....**************************************************************************-\






#
# """Routines to help draw star charts."""
#
# import numpy as np
# from IPython.display import HTML
# from matplotlib import rc_context, rcParams
# from matplotlib.animation import FuncAnimation, FFMpegWriter, writers
# from .starlib import Star
#
# def _plot_stars(catalog, observer, project, ax, mag1, mag2, margin=1.25):
#     """Experiment in progress, hence the underscore; expect changes."""
#
#     art = []
#
#     # from astropy import wcs
#     # w = wcs.WCS(naxis=2)
#     # w.wcs.crpix = [-234.75, 8.3393]
#     # w.wcs.cdelt = np.array([-0.066667, 0.066667])
#     # w.wcs.crval = [0, -90]
#     # w.wcs.ctype = ["RA---AIR", "DEC--AIR"]
#     # w.wcs.set_pv([(2, 1, 45.0)])
#
#     # import matplotlib.pyplot as plt
#
#     # plt.subplot(projection=wcs)
#     # #plt.imshow(hdu.data, vmin=-2.e-5, vmax=2.e-4, origin='lower')
#     # plt.grid(color='white', ls='solid')
#     # plt.xlabel('Galactic Longitude')
#     # plt.ylabel('Galactic Latitude')
#
#     xmin, xmax = ax.get_xlim()
#     ymin, ymax = ax.get_xlim()
#     lim = max(abs(xmin), abs(xmax), abs(ymin), abs(ymax)) * margin
#     lims = (-lim, lim)
#     ax.set_xlim(lims)
#     ax.set_ylim(lims)
#     ax.set_aspect('equal')
#
#     o = observer[0]
#
#     # Dim stars: points of with varying gray levels.
#
#     c = catalog
#     c = c[c['magnitude'] > mag1]
#     c = c[c['magnitude'] <= mag2]
#     #print('Second star group:', len(c))
#     c = c.sort_values('magnitude', ascending=False)
#     s = Star(ra_hours=c.ra_hours, dec_degrees=c.dec_degrees)
#     spos = o.observe(s)
#     x, y = project(spos)
#     m = (mag2 - c['magnitude']) / (mag2 - mag1)
#     # Note that "gray_r" is white for 0.0 and black for 1.0
#     art.append(ax.scatter(
#         x, y, s=1.0,
#         c=1 - 0.8 * m, cmap='gray_r', vmin=0.0, vmax=1.0,
#     ))
#
#     # Bright stars: black circles of varying radius, surrounded by a
#     # white gap in case stars are touching.  Draw the brightest stars
#     # first to stop them from completely occluding smaller companions.
#
#     def mag_to_radius(m):
#         return (mag1 - m) * scale + 1.0
#
#     c = catalog
#     c = c[c['magnitude'] <= mag1]
#     c = c.sort_values('magnitude', ascending=True)
#     #print('First star group:', len(c))
#     s = Star(ra_hours=c.ra_hours, dec_degrees=c.dec_degrees)
#     spos = o.observe(s)
#     x, y = project(spos)
#     scale = 1.5
#     radius = mag_to_radius(c['magnitude'])
#
#     x2 = np.repeat(x, 2)
#     y2 = np.repeat(y, 2)
#     radius2 = (radius[:,None] + (3.0,0.0)).flatten()
#     c2 = ('w', 'k')
#     c2 = ('k', 'w')
#
#     art.append(ax.scatter(x2, y2, s=radius2 ** 2.0, c=c2))
#
#     return art, mag_to_radius
#
# @writers.register('ffmpeg_small')
# class _FFMpegWriter(FFMpegWriter):
#     def _args(self):
#         args = super(_FFMpegWriter, self)._args()
#         i = args.index('h264') + 1
#         args[i:i] = ['-x264-params', 'keyint=99999999:scenecut=0']
#         #args.append('keyint=123:min-keyint=20')
#         return args
#
# X = []
#
# class _Animation(FuncAnimation):
#     patcher = None
#
#     def _draw_next_frame(self, framedata, blit):
#         blit = True    # override matplotlib's refusal to blit in save()
#         super(_Animation, self)._draw_next_frame(framedata, blit)
#
#         if self.patcher is None:
#             self.patcher = patch('matplotlib.backends.backend_agg'
#                             '.FigureCanvasAgg.draw', draw)
#             self.patcher.__enter__()
#
#     # Experiment to avoid drawing month names over each other when they
#     # are outside the axis borders and don't get blitted:
#
#     # def _pre_draw(self, framedata, blit):
#     #     artists = self._drawn_artists
#     #     for figure in set(a.axes.figure for a in artists):
#     #         from IPython.core.debugger import set_trace
#     #         #set_trace()
#     #         #figure.canvas.renderer.clear()
#     #     super(_Animation, self)._pre_draw(framedata, blit)
#
# def draw(self):
#     pass
#
# from unittest.mock import patch
#
# def _animate(projection, t, stars, observer, planet):
#     import matplotlib.pyplot as plt
#
#     # print(t)
#     # print(t[0].utc_strftime('%Y %B'))
#
#     o = observer.at(t)
#     p = o.observe(planet)
#
#     p0 = planet.at(t)
#     mag = -8.88 + 5.0 * np.log10(p.distance().au * p0.distance().au)
#
#     project = projection(p)
#     x, y = project(p)
#
#     fig, ax = plt.subplots()
#
#     plt.tick_params(axis='both', which='both',
#                     bottom=False, labelbottom=False,
#                     left=False, labelleft=False)
#
#     # Draw invisibly the entire path, so that the bounding boxes are
#     # known ahead of time.
#     ax.scatter(x, y, color='b', alpha=0.0)
#
#     art, mag_to_radius = _plot_stars(stars, o, project, ax, 6.0, 8.5, 0.8)
#
#     # http://aa.usno.navy.mil/software/mica/USNO-AA-TN-2003-04.pdf
#     # m - M = 5 (log10 d - 1)
#     # m = 5 (log10 d - 1) + M
#
#     x_left, x_right = ax.get_xlim()
#     y_bottom, y_top = ax.get_ylim()
#     text_x = x_left
#     text_y = y_bottom - (y_top - y_bottom) * 0.01
#
#     saturn_color = '#f7dfae'
#     #'#a69276'  # chroma('#d8c2a5').darken().hex()
#
#     # Somehow matplotlib is (a) drawing the date text twice which ruins
#     # the anti-aliasing and makes it look blocky, and (b) also never
#     # erasing that part of the figure so the month names all pile up on
#     # top of each other.  So let's manually paint a white rectangle
#     # behind the text each time to overwrite the previous text.
#     r = ax.add_patch(plt.Rectangle(
#         (x_left, y_bottom - 0.012), 0.08, 0.01,
#         clip_on=False, facecolor='white',
#     ))
#
#     items = []  # so update() can get the axes init() created
#
#     def init():
#         print('init()')
#         planet_art = ax.scatter(x[100], y[100], color=saturn_color)
#         #print(dir(planet_art))
#         date_text = ax.text(text_x, text_y, '', ha='left', va='top')
#         items[:] = [planet_art, date_text]
#         return planet_art, r, #date_text
#
#     def update(i):
#         #print('Frame {}'.format(i))
#
#         planet_art, date_text = items
#
#         # planet_art.set_xdata(x[i])
#         # planet_art.set_ydata(y[i])
#
#         planet_art.set_offsets(((x[i], y[i]),))
#         planet_art.set_sizes((mag_to_radius(mag[i]) ** 2.0,))
#
#         date_text.set_text(t[i].utc_strftime('%Y %B'))
#
#         ax.set_facecolor('black')
#         return planet_art, r, date_text
#
#     frames = len(x)
#     #frames = 90
#
#     ax.set_facecolor('black')
#
#     anim = _Animation(fig, update, frames=frames,
#                       blit=True, init_func=init,
#                       interval=16)
#     plt.close()
#     return anim
#     rcParams.validate['animation.writer'].valid['ffmpeg_small'] = 'ffmpeg_small'
#     with rc_context({'animation.writer': 'ffmpeg_small'}):
#         html = anim.to_html5_video()
#
#     anim.patcher.__exit__()
#     return HTML(html)
#
# def _save_and_display(anim, path):
#     Writer = _FFMpegWriter
#     writer = Writer(codec='h264',
#                     bitrate=rcParams['animation.bitrate'],
#                     fps=1000. / anim._interval)
#     anim.save(path, writer=writer)
#     anim.patcher.__exit__()
#     return HTML(r'''<video autoplay loop>
#   <source type="video/mp4" src="{}">
#   Alas! Your browser does not support the video tag.
# </video>'''.format(path)) #'file://' + path))
#
# class T(object):
#     from time import time
#     def __enter__(self):
#         self.t0 = self.time()
#     def __exit__(self, *args):
#         print('<<< %s >>>' % (self.time() - self.t0))
#
# def printout(thing):
#     print()
#     for line in debug(thing):
#         print(line)
#     print()
#
# def debug(thing, indent=0):
#     a = 'A' if thing.get_animated() else '-'
#     yield '{:<{}}{} {} {}'.format('', indent, hex(id(thing)), a, repr(thing))
#     indent += 2
#     for child in thing.get_children():
#         yield from debug(child, indent)








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

def print_on_plain(stars):
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
    horizon = Circle((0, 0), radius=1, transform=ax.transData)
    # horizon = Rectangle((-100, -100), 200, 200, transform=ax.transData)
    # for col in ax.collections:
    #     col.set_clip_path(horizon)

    # other settings
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    plt.axis('off')
    fig.savefig('sky.png')
    plt.show()
# def find_earth_sun_loc():
#     eph = load('de421.bsp')
#     # hipparcos dataset contains star location data
#     with load.open(hipparcos.URL) as f:
#         stars = hipparcos.load_dataframe(f)
#     sun = eph['sun']
#     earth = eph['earth']

def run():
    dt = get_current_time()
    # hour = dt.hour-4   # set utc time by current timezone(+4)
    # dt = dt.replace(hour= hour)
    lat, long = get_current_location(dt)
    utc_dt = convert_time_to_utc(dt)
    print('long, lat', get_current_location(dt))

    eph = load('de421.bsp')
    # hipparcos dataset contains star location data
    with load.open(hipparcos.URL) as f:
        stars = hipparcos.load_dataframe(f)
    sun = eph['sun']
    earth = eph['earth']
    t = define_observe_time_from_utc(utc_dt)
    center_object = define_sky_obsrve_point(long, lat,t)
    projection = get_projection_our_center(earth, t, center_object)
    stars = calc_star_projection(earth, stars, projection, t)
    print_on_plain(stars)


run()