import rte
from rte.detectors import DetectorSpherical
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
    def _angular_efficiency(cosTheta):
        eff = np.sum([a*cosTheta**n for n,a in enumerate(OpticalModule.angular_parameters)], axis=0)
        # eff *= (cosTheta>0) #keep only upward going tracks
        return eff.squeeze()

    def efficiency(self, p:rte.Point):
        #convert to local RF
        R_local = p.R-self['center'].sample()
        N_local = R_local/R_local.mag()
        #calculate angular efficiency
        eff_angular = self._angular_efficiency(cosTheta = N_local.z)
        return super().efficiency(p) * eff_angular