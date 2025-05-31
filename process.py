import rte
import vegas_params as vp

class Process0(rte.process.CalculatorBase):
    def __init__(self, src, tgt, medium):
        #store the expressions for later use
        self.src = src
        self.det = tgt
        self.medium = medium
        super().__init__(src=src, tgt=tgt)
        
    def __call__(self, src, tgt):
        p_src, p_det = src, tgt
        dR = p_det.R-p_src.R
        L = dR.mag()
        s = dR/L
        #update the points
        p_src.s = p_det.s = s
        #calculate the factors
        F_src = self.src.luminosity(p_src).squeeze()
        F_det = self.det.efficiency(p_det).squeeze()
        F_medium = self.medium.attenuation(L, n_scattering=0).squeeze()
        F_distance = 1/L.squeeze()**2
        # print(f"{F_src=},\n{F_det=},\n{F_medium=}\n")
        #resulting value        
        F_result = F_det * F_src * F_medium * F_distance
        # print(f"{F_result=}")
        return F_result