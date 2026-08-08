# Nathan Samuell
# Following https://python-control.readthedocs.io/en/0.10.2/examples/python-control_tutorial.html#Initialization

import numpy as np
import matplotlib.pyplot as plt

# try to import control systems library
try:
    import control as ct
    print("python-control", ct.__version__)
except ImportError as e:
    print(e)
