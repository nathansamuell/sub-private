# Nathan Samuell
# Aug 8 2026

import numpy as np

class SimDepthMotor:
    # define constants
    rotationsToVolume: float = 3  # 3 ml of volume for one motor rotation
    maxVolume: int = 30           # 30 ml/30cm^3 of water
    maxSpeed: int = 300           # rpm

    def __init__(self, vol):
        self.currVolume: float = vol
        self.saturated: bool = False
        return

    def setRotToVol(self, ratio: float):
        rotationsToVolume = ratio
        return

    def setMaxVol(self, maxVol: int):
        maxVolume = 30
        return

    def getCurrentVolume(self) -> float:
        return self.currVolume
    
    def propagate(self, dt_ms: int, speed: int):
        # if we've saturated, set global flag and clamp
        if abs(speed) > self.maxSpeed:
            self.saturated = True
            speed = maxSpeed
        else:
            self.saturated = False

        # calculate new volume
        # figure how many rotations made, map to volume
        deltaVolume = np.multiply(np.multiply(np.divide(speed, 60000), dt_ms), self.rotationsToVolume)
        if np.add(self.currVolume, deltaVolume) > np.float64(self.maxVolume):
            self.currVolume = self.maxVolume
        elif np.add(self.currVolume, deltaVolume) < np.float64(0):
            self.currVolume = 0
        else:
            self.currVolume = np.add(self.currVolume, deltaVolume)

        return;



# class SimSimpleCylinderSub:
    
