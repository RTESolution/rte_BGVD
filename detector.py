import rte
from bgvd_model import OpticalModule
import vegas_params as vp
import numpy as np

class BGVD_Module(rte.detectors.DetectorSpherical):
    def __init__(self, center=[0,0,0], T=vp.Uniform([0,1])):
        super().__init__(center=center, 
                         T=T,
                         radius=OpticalModule.radius
                        )
    @staticmethod
    def efficiency(p:rte.Point):
        cosTheta = p.s.z
        eff = np.sum([a*cosTheta**n for n,a in enumerate(OpticalModule.angular_parameters)], axis=0)
        eff *= (cosTheta>0) #keep only upward going tracks
        return eff.squeeze()