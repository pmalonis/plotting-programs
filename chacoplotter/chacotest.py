import numpy as np
from chaco.shell import *

x = np.linspace(-2*np.pi, 200*np.pi, 1e5)
y = np.sin(x)
x = np.random.randn(len(x))
plot(x, "r-")
title("first plot")

show()