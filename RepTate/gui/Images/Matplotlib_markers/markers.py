"""Generate plenty of Matplotlib markers to later use as icons"""

import matplotlib.pyplot as plt
# To make a figure without the frame :
markers=['.',',','o','v','^','<','>','1','2','3','4','8','s','p','P','*','h','H','+','x','X','D','d','|','_']
descriptions=['point', 'pixel', 'circle', 'triangle_down', 'triangle_up','triangle_left', 'triangle_right', 'tri_down', 'tri_up', 'tri_left','tri_right', 'octagon', 'square', 'pentagon', 'plus (filled)','star', 'hexagon1', 'hexagon2', 'plus', 'x', 'x (filled)','diamond', 'thin_diamond', 'vline', 'hline']
dic = {}
for m,d in zip(markers,descriptions):
    dic[d]=m
    markersize=8
    if d == "diamond":
        markersize=5
    if d == "thin_diamond":
        markersize=5
    fig = plt.figure(frameon=False)
    fig.set_size_inches(0.52,0.52)
    ax = plt.Axes(fig, [0, 0, .24, .24])
    ax.set_axis_off()
    fig.add_axes(ax) 
    plt.plot([0], [0],color='black', marker=m, markersize=markersize, markerfacecolor='none')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # lim = 0.05
    # ax.set_xlim([-lim,lim])
    # ax.set_ylim([-lim,lim])
    plt.savefig("marker_%s.png"%d, dpi=1000, pad_inches = 0, bbox_inches='tight', transparent=True)

print(dic)