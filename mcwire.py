#!/usr/bin/python3

import math
import numpy as np
from random import random

# resistivity ρ = R * A / L [ohm m]
# resistance  R = ρ * L / A [ohm]

class NotRand(object):
    def __init__(self):
        self.i:int = -1
    def __call__(self) -> int:
        self.i = self.i + 1
        return self.i % 2

class MCwire(object):
    def __init__(self, f1:float=0.5, f2:float=0.5):
        if(f1+f2 != 1.0):
            raise ValueError("The material fractions have to add to 1.0, ", f1, f2)
        self.L:float    = 100.       # 100m long wire [m]
        self.A:float    = 1e-4      # 1cm x 1cm cross-section [m^2]
        self.divL:int   = 40     # divisions along L
        self.divA:int   = 40       # divisions along A
        self.rho1:float = 1e-9      # restivity [ohm m] mat 1
        self.rho2:float = 1e-6      # mat 2
        self.f1:float   = f1        # fraction of mat1
        self.f2:float   = f2        # fraction of mat2
                                    # wire represented as 2D array (L,A)
        self.nr = NotRand()
        self.wire = np.zeros(self.divL*self.divA).reshape(self.divL,self.divA)

        self._build_wire()
        self.Rwavr:float    = self._calc_R_waverage()
        self.Rstream:float  = self._calc_R_streams()
        self.Rpancake:float = self._calc_R_pancakes()


    def results(self):
        'Print results'
        print(self.wire)
        print(f'average: \t{self.Rwavr}\nstreams: \t{self.Rstream}\npancakes: \t{self.Rpancake}')

    def _build_wire(self):
        'Fill the wire array with resistivities'
        for i in np.arange(self.divL):
            for j in np.arange(self.divA):
                if(random() < self.f1):
                #if(self.nr() < self.f1):
                    self.wire[i,j] = self.rho1
                else:
                    self.wire[i,j] = self.rho2
        # Resistance of each segment
        self.wire *= (self.L / self.divL) / (self.A / self.divA)

    def _calc_R_streams(self) -> float:
        'Calculate resistance of the wire, streams first'
        streams = self.wire.sum(axis=0) 
        invR:float = 0.0
        for Rstream in streams:
            invR += 1.0 / Rstream
        return 1.0 / invR

    def _calc_R_pancakes(self) -> float:
        'Calculate resistance of the wire, pancakes first'
        pancakes = np.zeros(self.divL)
        for i in np.arange(self.divL):
            for j in np.arange(self.divA):
                pancakes[i] += 1.0 / self.wire[i,j]
        pancakes = 1.0 / pancakes
#        print (pancakes)
        return pancakes.sum()

    def _calc_R_waverage(self) -> float:
        'Calculate resistance of the wire, weighted average'
        # R = rho * l / A
        rho = self.rho1 * self.f1 + self.rho2 * self.f2
        return rho * self.L / self.A


# ------------------------------------------------------------
if __name__ == '__main__':
    print("This is a random wire with two components.")
    input("Press Ctrl+C to quit, or enter else to test it.")
    a = MCwire()
    a.results()

'''
import numpy as np
import mcwire
a = mcwire.MCwire()
a.results()
'''
    
