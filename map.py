from sys import getsizeof

from opensimplex import OpenSimplex


class map():

    def __init__(self):
        self.noiseElevation = OpenSimplex(1818811)
        self.noiseMoisture = OpenSimplex(987654)
        self.generateMap = {}

    def NoiseCalculation(self, nx, ny):
        e = (1.00 * self.noiseElevation.noise2d(1 * nx, 1 * ny)
             + 0.50 * self.noiseElevation.noise2d(2 * nx, 2 * ny)
             + 0.25 * self.noiseElevation.noise2d(4 * nx, 4 * ny)
             + 0.13 * self.noiseElevation.noise2d(8 * nx, 8 * ny)
             + 0.06 * self.noiseElevation.noise2d(16 * nx, 16 * ny)
             + 0.03 * self.noiseElevation.noise2d(32 * nx, 32 * ny))
        e = ((e / (
                1.00 + 0.50 + 0.25 + 0.13 + 0.06 + 0.03)) / 2.0 + 0.5) ** 2.7  ## change 2.7 to increase or decrese the globql elevation
        m = (1.00 * self.noiseMoisture.noise2d(1 * nx, 1 * ny)
             + 0.50 * self.noiseMoisture.noise2d(2 * nx, 2 * ny)
             + 0.25 * self.noiseMoisture.noise2d(4 * nx, 4 * ny)
             + 0.13 * self.noiseMoisture.noise2d(8 * nx, 8 * ny)
             + 0.06 * self.noiseMoisture.noise2d(16 * nx, 16 * ny)
             + 0.03 * self.noiseMoisture.noise2d(32 * nx, 32 * ny))
        m = ((m / (1.00 + 0.50 + 0.25 + 0.13 + 0.06 + 0.03)) / 2.0 + 0.5)
        self.generateMap[(nx, ny)] = (e, m)
        return e, m

    def BiomeCalculation(self, e, m):
        if (e < 0.1 and m > 0.3):
            return "OCEAN"
        if (e < 0.12 and m > 0.5):
            return "BEACH"

        if (e > 0.75):
            if (m < 0.1):
                return "SCORCHED"
            if (m < 0.2):
                return "BARE"
            if (m < 0.5):
                return "TUNDRA"
            return "SNOW"

        if (e > 0.6):
            if (m < 0.33):
                return "TEMPERATE_DESERT"
            if (m < 0.66):
                return "SHRUBLAND"
            return "TAIGA"

        if (e > 0.3):
            if (m < 0.16):
                return "TEMPERATE_DESERT"
            if (m < 0.5):
                return "GRASSLAND"
            if (m < 0.83):
                return "TEMPERATE_DECIDUOUS_FOREST"
            return "TEMPERATE_RAIN_FOREST"

        if (m < 0.16):
            return "SUBTROPICAL_DESERT"
        if (m < 0.33):
            return "GRASSLAND"
        if (m < 0.66):
            return "TROPICAL_SEASONAL_FOREST"
        return "TROPICAL_RAIN_FOREST"

    def mapreturn(self, x, y):

        if (getsizeof(self.generateMap) > 7200006):
            self.generateMap.clear()

        if ((x, y) in self.generateMap):
            e, m = self.generateMap[(x, y)]
        else:
            e, m = self.NoiseCalculation(x, y)
        return self.BiomeCalculation(e, m)
