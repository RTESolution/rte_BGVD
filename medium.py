import bgvd_model
import scipy
import rte
import numpy as np
#define the water medium
class BaikalWater(bgvd_model.BaikalWater):
    def mu_a(self, wavelength):
        return np.interp(wavelength,
                         self.wavelength,
                         self.absorption_inv_length)
    def mu_s(self, wavelength):
        return np.interp(wavelength,
                         self.wavelength, 
                         self.scattering_inv_length)
    def n_phase(self, wavelength):
        return np.interp(wavelength, 
                         water.wavelength,
                         water.phase_refraction_index
                        )
    def speed_of_light(self, wavelength):
        return scipy.constants.speed_of_light/self.n_phase(wavelength)

water = BaikalWater()

def get_properties(wavelength):
    return rte.Medium(
        mu_a = water.mu_a(wavelength),
        mu_s = water.mu_s(wavelength),
        c = water.speed_of_light(wavelength),
        g = 0.9
    )