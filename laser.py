import vegas_params as vp
import numpy as np
import rte

class cosTheta_DiffusorExp(vp.Uniform):
    def __init__(self, sigma=1):
        self.sigma = sigma
        super().__init__()
    def __construct__(self, x):
        return self.sigma*np.log(np.exp(-1./self.sigma) 
                                 + x*(np.exp(1/self.sigma) - np.exp(-1/self.sigma)) 
                                )


@vp.expression
def diffused_light(ray:vp.Direction, diffusor:vp.Direction):
    return vp.Vector.__call__(rte.utils.combine_rotations(ray, diffusor))

def DiffusorExp(light, sigma=0):
    if(sigma==0):
        return light
    else:
        return diffused_light(light, diffusor=vp.Direction(cos_theta=cosTheta_DiffusorExp(sigma)))


class Laser(rte.Source):
    def __init__(self,
                 position,
                 direction=vp.Vector([0,0,1]),
                 time=0,
                 *,
                 diffuser_sigma=1e-5,
                 total_photons=1e15
                ):
        super().__init__(R=vp.Vector(position),
                         T=time,
                         s=vp.Vector(direction),
                )
        #normalize the laser integral to be 1e15 photons
        self.diffuser_sigma = diffuser_sigma
        self.total_photons = total_photons
        self.diff_norm = (np.exp(1/diffuser_sigma)-np.exp(-1/diffuser_sigma))*diffuser_sigma
        

    def luminosity(self, p:rte.Point)->float:
        s0 = self['s'].sample()
        cosTheta = p.s.dot(s0)
        pdf = np.exp(cosTheta/self.diffuser_sigma)/self.diff_norm
        pdf *= 1/(2*np.pi)
        return pdf * self.total_photons