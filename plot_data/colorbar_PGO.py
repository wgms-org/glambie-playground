#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 09:29:06 2026

@author: guyez
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os
import matplotlib


# COLORMAPcomme dans PGO

def colorFader(c1, c2, t):
    c1 = np.array(mcolors.hex2color(c1))
    c2 = np.array(mcolors.hex2color(c2))
    return mcolors.rgb2hex((1 - t) * c1 + t * c2)

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = mcolors.LinearSegmentedColormap.from_list(
        cmap.name + "_trunc", cmap(np.linspace(minval, maxval, n)))
    return new_cmap

top = matplotlib.colormaps['gist_heat']
bottom = matplotlib.colormaps['Blues']
mid = plt.get_cmap('Spectral')

top = truncate_colormap(top, 0, 0.92)
bottom = truncate_colormap(bottom, 0.1, 0.92)

rgba_1 = mcolors.rgb2hex(top(0.99))
rgba_2 = mcolors.rgb2hex(bottom(0.90))
rgba = mcolors.rgb2hex(mid(0.5))

n = 256
c1 = [mcolors.to_rgba(colorFader(rgba_1, rgba, x/n)) for x in range(n+1)]
top_mid = mcolors.ListedColormap(c1)

top_mid_newcolors = np.vstack((top(np.linspace(0, 1, 250)),
                               top_mid(np.linspace(0, 1, 25))))
top_mid_newcmp = mcolors.ListedColormap(top_mid_newcolors)

c2 = [mcolors.to_rgba(colorFader(rgba, rgba_2, x/n)) for x in range(n+1)]
bottom_mid = mcolors.ListedColormap(c2)

top_mid_bottom_newcolors = np.vstack((top_mid_newcmp(np.linspace(0, 1, 200)),
                                      bottom_mid(np.linspace(0, 1, 100))))
newcmp = mcolors.ListedColormap(top_mid_bottom_newcolors, name='OrangeYellowBlue')

cmap = newcmp.copy()
cmap.set_bad(color="white") # put no data in white 
