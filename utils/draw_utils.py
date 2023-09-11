import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import SubplotZero

def make_arrows(axs):
    axs.xaxis.set_ticks_position('bottom')
    axs.yaxis.set_ticks_position('left')

    # make arrows
    axs.spines['left'].set_position('zero')
    axs.spines['right'].set_visible(False)
    axs.spines['bottom'].set_position('zero')
    axs.spines['top'].set_visible(False)
    axs.xaxis.set_ticks_position('bottom')
    axs.yaxis.set_ticks_position('left')
    axs.plot((1), (0), ls="", marker=">", ms=10, color="k",
             transform=axs.get_yaxis_transform(), clip_on=False)
    axs.plot((0), (1), ls="", marker="^", ms=10, color="k",
             transform=axs.get_xaxis_transform(), clip_on=False)



def draw_ECG(ax, signal):
    ax.plot(signal, color='black', alpha=0.2, label="ECG")
    make_arrows(ax)
    ax.set_xticks(range(0, len(signal),5))
    ax.grid(which='major', axis='both', linestyle='--', alpha=0.75)
    ax.plot(signal, 'o', label='vals', color="black",  markersize=2)


def draw_vertical_line(ax, x, y, color=None, label=None):
    if color is None:
        color = 'red'
    ax.vlines(x=x, ymin=0, ymax=y, colors=color, lw=2, alpha=0.5, label=label)