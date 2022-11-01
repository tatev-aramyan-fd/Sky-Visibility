import matplotlib.pyplot as plt


def draw_planets_sun_moon(obj_name, ax, t, projection, eph):
    earth = eph['earth']
    celestial_obj = eph[obj_name]
    obj_position = earth.at(t).observe(celestial_obj)
    x, y = projection(obj_position)

    if obj_name == "sun":
        color = "yellow"
        st = '☀'
        obj_name = ''
    elif obj_name == 'moon':
        color = 'grey'
        st = "☾"
        obj_name = ''
    else:
        color = "green"
        st = '•'
    ax.text(x, y, s=st, fontsize=30, c=color)
    ax.text(x+0.05, y+0.02, s=obj_name, fontsize=10, c="grey")


def draw(ax, stars):
    max_star_size = 100
    limiting_magnitude = 4
    bright_stars = (stars.magnitude <= limiting_magnitude)
    magnitude = stars['magnitude'][bright_stars]
    border = plt.Rectangle((-100, -100), 200, 200, color='black', fill=True)
    ax.add_patch(border)
    marker_size = max_star_size * 10 ** (magnitude / -2.5)
    ax.scatter(stars['x'][bright_stars], stars['y'][bright_stars],
               s=marker_size, color='blue', marker='*', linewidths=0,
               zorder=2)



