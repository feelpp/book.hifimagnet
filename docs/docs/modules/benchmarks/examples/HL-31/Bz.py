#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt


fig = plt.figure()
ax = plt.axes()

ax.set_xlabel('$z\,[mm]$')
ax.set_ylabel('$B_z\,[T]$')
# ax.set_title(r'balal')

file = open("HL-31_Field_Map.dat", "r" )
data = np.genfromtxt(file )
z =  data[:,1]
bz = data[:,3]

print "bz size: %d" % bz.size, np.argmax(bz)
bmax = np.amax(bz)
imax = np.argmax(bz)

every = bz.size/10
ax.plot(z, bz, c='b', marker='o', markevery=every, ls='-', label=r'Ana')
ax.grid(True)
leg = ax.legend()
plt.xlim(z[0],z[-1])

# # make a zoom:
# # http://akuederle.com/matplotlib-zoomed-up-inset
# # https://stackoverflow.com/questions/13583153/how-to-zoomed-a-portion-of-image-and-insert-in-the-same-plot-in-matplotlib

# from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
# axins = zoomed_inset_axes(ax, 6, loc=2) # zoom-factor: 2.5, location: upper-left
# axins.plot(z,bz)
# shift = 20
# z0 = z[imax-shift]
# z0 = z[imax-shift]
# axins.set_xlim(z[imax-shift], z[imax+shift]) # apply the x-limits
# axins.set_ylim(0.98*bmax, 1.02*bmax) # apply the y-limits

# plt.yticks(visible=False)
# plt.xticks(visible=False)

# from mpl_toolkits.axes_grid1.inset_locator import mark_inset
# mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")

# plt.show()
plt.savefig("Bz.png", format='png')
plt.close(fig)
