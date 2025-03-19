import vegas_params as vp
import numpy as np
import rte

class cosTheta_DiffusorExp(vp.Uniform):
    def __init__(self, sigma=1):
        self.sigma = sigma
        super().__init__()
    def __construct__(self, x):
        return self.sigma*np.log(np.exp(-1./self.sigma) + x*(np.exp(1/self.sigma) - np.exp(-1/self.sigma)) )


@vp.expression
def diffused_light(ray:vp.Direction, diffusor:vp.Direction):
    return vp.Vector.__call__(rte.utils.combine_rotations(ray, diffusor))

def DiffusorExp(light, sigma=0):
    if(sigma==0):
        return light
    else:
        return diffused_light(light, diffusor=vp.Direction(cos_theta=cosTheta_DiffusorExp(sigma)))


def Laser(position, direction, time=0, *, diffuser_sigma=0, total_photons=1e15):
    src = rte.Source(R=vp.Vector(position),
                      T=time,
                      s=DiffusorExp(light=direction, sigma=diffuser_sigma)
                 )
    #normalize the laser integral to be 1e15 photons
    src = vp.utils.normalize_integral(total_photons, nitn=10)(src)
    return src