# from controls lib example 2

# standard controls lib header
import numpy as np
import matplotlib.pyplot as plt

# test import, exit if fails
try:
    import control as ct
    print("python-control", ct.__version__)
except ImportError as e:
    print(e)
    exit(1)

# define a bicycle navigating (simple kinematics)
# write in terms of contact point (x, y) and angle theta
#
# x' = cos(Theta) * v
# y' = sin(Theta) * v
# Theta' = (v/l) * tan(Delta)

# System Defintion:
# x' = f(x, u)
# y = h(x, u)

# Define the update rule for the system, f(x, u)
# States: x, y, theta (postion and angle of the center of mass)
# Inputs: v (forward velocity), delta (steering angle)
def vehicle_update(t, x, u, params):
    # Get the parameters for the model
    a = params.get('refoffset', 1.5)        # offset to vehicle reference point
    b = params.get('wheelbase', 3.)         # vehicle wheelbase
    maxsteer = params.get('maxsteer', 0.5)  # max steering angle (rad)

    # Saturate the steering input
    delta = np.clip(u[1], -maxsteer, maxsteer)
    alpha = np.arctan2(a * np.tan(delta), b)

    # Return the derivative of the state
    return np.array([
        u[0] * np.cos(x[2] + alpha),    # xdot = cos(theta + alpha) v
        u[0] * np.sin(x[2] + alpha),    # ydot = sin(theta + alpha) v
        (u[0] / a) * np.sin(alpha)      # thdot = v sin(alpha) / a
    ])

# Define the readout map for the system, h(x, u)
# Outputs: x, y (planar position of the center of mass)
def vehicle_output(t, x, u, params):
    return x

# Default vehicle parameters (including nominal velocity)
vehicle_params={'refoffset': 1.5, 'wheelbase': 3, 'velocity': 15,
                'maxsteer': 0.5}

# Define the vehicle steering dynamics as an input/output system
vehicle = ct.nlsys(
    vehicle_update, vehicle_output, states=3, name='vehicle',
    inputs=['v', 'delta'], outputs=['x', 'y', 'theta'], params=vehicle_params)

# now, vehicle object is the nonlinear system model. Next, let's compute a trajectory for the system!

# Define the time interval that we want to use for the simulation
timepts = np.linspace(0, 10, 1000) # presumably 0-10s, sampled every 10 ms

# Define the inputs
U = [
    10 * np.ones_like(timepts),          # velocity
    0.1 * np.sin(timepts * 2*np.pi)      # steering angle - this is angular freq one second * 0.1
]

# Simulate the system dynamics, starting from the origin
response = ct.input_output_response(vehicle, timepts, U, 0)
time, outputs, inputs = response.time, response.outputs, response.inputs

# Create a figure to plot the results
fig, ax = plt.subplots(2, 1)

# Plot the results in the xy plane
ax[0].plot(outputs[0], outputs[1])
ax[0].set_xlabel("$x$ [m]")
ax[0].set_ylabel("$y$ [m]")

# Plot the inputs
ax[1].plot(timepts, U[0])
ax[1].set_ylim(0, 12)
ax[1].set_xlabel("Time $t$ [s]")
ax[1].set_ylabel("Velocity $v$ [m/s]")
ax[1].yaxis.label.set_color('blue')

rightax = ax[1].twinx()       # Create an axis in the right
rightax.plot(timepts, U[1], color='red')
rightax.set_ylim(None, 0.5)
rightax.set_ylabel(r"Steering angle $\phi$ [rad]")
rightax.yaxis.label.set_color('red')

fig.tight_layout()
plt.show()
