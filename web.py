from mpl_toolkits.mplot3d import Axes3D

from os.path import expanduser#import the os
import tkinter
from pathlib import Path
import numbers    
import cif_extractor as cifEx
import cifToScad as cifScad
from tkinter.filedialog import askopenfilename
import getpass
import numpy as np

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt 


fig = plt.figure(1)
        #plt.ion()
ax = fig.add_subplot(projection='3d')
ax.set_aspect("equal")
        
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = np.cos(u)*np.sin(v)
y = np.sin(u)*np.sin(v)
z = np.cos(v)
ax.plot_wireframe(x, y, z, color="r")      
        
plt.show()