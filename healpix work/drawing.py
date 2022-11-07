import numpy as np
import matplotlib.pyplot as plt


def draw_sphere(ras: list, decs: list, ra: float, dec: float):

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111, projection='mollweide')
    ax.scatter(np.radians(ras), np.radians(decs), c='#000080')
    ax.text(np.radians(ra), np.radians(dec), s='*', c='red')

    xtick_labels = ["–150°", "–120°", "–90°", "–60°", "–30°",
                    "0°", "30°", "60°", "90°", "120°", "150°"
                    ]
    ytick_labels = ["–75°", "–60°", "–45°", "–30°", "–15°",
                    "0°", "15°", "30°", "45°", "60°", "75°"
                    ]
    ax.set_yticklabels(ytick_labels, fontsize=12)
    ax.set_xticklabels(xtick_labels, fontsize=15)
    ax.set_xlabel("RA")
    ax.xaxis.label.set_fontsize(20)
    ax.set_ylabel("Dec")
    ax.yaxis.label.set_fontsize(20)
    ax.grid(True)
    plt.axis('on')
    fig.savefig('sphere.png')
    plt.show()
