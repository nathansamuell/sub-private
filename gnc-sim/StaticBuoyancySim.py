# Nathan Samuell
# Aug 8 2026

# standard controls lib header
import numpy as np
import matplotlib.pyplot as plt

IN_TO_CM = 2.54
GRAV_CONST = 9.81 * 100
DENSITY_WATER = 1

# calculate volume displaced as volume of cylinder - water in syringe

# 3" OD, 15.5" len
vCylinder: np.float = np.square((3 * IN_TO_CM) / 2) * np.pi * (12 * IN_TO_CM)

# halfway full (15ml) of water
vSyringeWater: np.float = 0

mSub: float = vCylinder - 30;
vDisplacedBySub: np.float = (vCylinder - vSyringeWater)

print(str(vDisplacedBySub) + " cm^3");

print("Density compared to water: " + str(mSub / vDisplacedBySub))


newDepth: float = 12 * IN_TO_CM;       # cm
newBuoyantVel: float = 0;   # cm/s
newBuoyantAccel: float = 0; # cm^2/s

# start lists with ICs
depthList: list[np.float] = [newDepth]
buoyantVelList: list[np.float] = [newBuoyantVel]
buoyantAccelList: list[np.float] = [newBuoyantAccel]

# run sim in ms, 20 ms step size
stepSize = 20           # ms
dt = stepSize / 1000    # s
tListMs = np.arange(0, 10000, stepSize)
for t in tListMs:
    if t == 0:
        continue

    newBuoyantAccel = np.divide(
        np.subtract(np.multiply(mSub, GRAV_CONST), np.multiply(np.multiply(vDisplacedBySub, DENSITY_WATER), GRAV_CONST)),
        mSub
    )

    newBuoyantVel = np.multiply(newBuoyantAccel, dt) + newBuoyantVel
    newDepth = np.multiply(newBuoyantVel, dt) + newDepth
    # print(newDepth)

    depthList.append(newDepth)
    buoyantVelList.append(newBuoyantVel)
    buoyantAccelList.append(newBuoyantAccel)

plt.plot(np.array(tListMs) / 1000, buoyantVelList)
plt.title("StaticBuoyancySim")
plt.xlabel("Timestep")
plt.ylabel("Depth (cm)")
plt.gca().invert_yaxis()
plt.grid(True)
plt.show()
