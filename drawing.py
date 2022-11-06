import numpy as np
import matplotlib.pyplot as plt


def draw_sphere(ras: list, decs: list, la, lo):

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111, projection='mollweide')
    # ax.scatter(np.radians(ras), np.radians(decs),c='#000080')
    ax.scatter(np.radians(la), np.radians(lo), c='#000080')
    ax.text(np.radians(la), np.radians(lo),s='*',c='red')
    xtick_labels = ["$-150^{\circ}$", "$-120^{\circ}$", "$-90^{\circ}$",
                    "$-60^{\circ}$", "$-30^{\circ}$", "$-0^{\circ}$",
                    "$30^{\circ}$", "$60^{\circ}$", "$90^{\circ}$",
                    "$120^{\circ}$", "$150^{\circ}$"]
    ytick_labels = ["$-75^{\circ}$", "$-60^{\circ}$", "$-45^{\circ}$",
                    "$-30^{\circ}$", "$-15^{\circ}$",
                    "$0^{\circ}$", "$15^{\circ}$", "$30^{\circ}$",
                    "$45^{\circ}$", "$60^{\circ}$",
                    "$75^{\circ}$"]
    ax.set_yticklabels(ytick_labels, fontsize=12)
    ax.set_xticklabels(xtick_labels, fontsize=15)
    ax.set_xlabel("RA")
    ax.xaxis.label.set_fontsize(20)
    ax.set_ylabel("Dec")
    ax.yaxis.label.set_fontsize(20)
    ax.grid(True)
    plt.axis('on')
    plt.show()