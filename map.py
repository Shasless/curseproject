from opensimplex import OpenSimplex


class map():

    def __init__(self):
        self.noiseElevation = OpenSimplex(1818811)
        self.noiseMoisture = OpenSimplex(987654)

    def NoiseCalculation(self, nx, ny):
        e = (1.00 * self.noiseElevation.noise2d(1 * nx, 1 * ny)
             + 0.50 * self.noiseElevation.noise2d(2 * nx, 2 * ny)
             + 0.25 * self.noiseElevation.noise2d(4 * nx, 4 * ny)
             + 0.13 * self.noiseElevation.noise2d(8 * nx, 8 * ny)
             + 0.06 * self.noiseElevation.noise2d(16 * nx, 16 * ny)
             + 0.03 * self.noiseElevation.noise2d(32 * nx, 32 * ny))
        e = e / (1.00 + 0.50 + 0.25 + 0.13 + 0.06 + 0.03)
        m = (1.00 * self.noiseMoisture.noise2d(1 * nx, 1 * ny)
             + 0.50 * self.noiseMoisture.noise2d(2 * nx, 2 * ny)
             + 0.25 * self.noiseMoisture.noise2d(4 * nx, 4 * ny)
             + 0.13 * self.noiseMoisture.noise2d(8 * nx, 8 * ny)
             + 0.06 * self.noiseMoisture.noise2d(16 * nx, 16 * ny)
             + 0.03 * self.noiseMoisture.noise2d(32 * nx, 32 * ny))
        m = (1.00 + 0.50 + 0.25 + 0.13 + 0.06 + 0.03)
        return e, m

    ## REDO BUNDARY
    def BiomeCalculation(self, e, m):
        if (e < -0.8):
            return "OCEAN"
        if (e < -0.75):
            return "BEACH"

        if (e > 0.6):
            if (m < -0.6):
                return "SCORCHED"
            if (m < -0.4):
                return "BARE"
            if (m <  -0.3):
                return "TUNDRA"
            return "SNOW"

        if (e > 0.2):
            if (m < -0.66):
                return "TEMPERATE_DESERT"
            if (m < 0.33):
                return "SHRUBLAND"
            return "TAIGA"

        if (e > -0.6):
            if (m < -0.68):
                return "TEMPERATE_DESERT"
            if (m < 0):
                return "GRASSLAND"
            if (m < 0.66):
                return "TEMPERATE_DECIDUOUS_FOREST"
            return "TEMPERATE_RAIN_FOREST"

        if (m <  -0.68):
            return "SUBTROPICAL_DESERT"
        if (m < -0.33):
            return "GRASSLAND"
        if (m < 0.33):
            return "TROPICAL_SEASONAL_FOREST"
        return "TROPICAL_RAIN_FOREST"

    def mapreturn(self,x,y):
        e,m = self.NoiseCalculation(x,y)
        return self.BiomeCalculation(e,m)
