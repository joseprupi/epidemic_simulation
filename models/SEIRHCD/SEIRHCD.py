from ..Model import Model

import numpy as np
from scipy.integrate import solve_ivp


class SEIRHCD(Model):

    def __init__(self, population):
        self.S = None
        self.E = None
        self.I = None
        self.R = None
        self.H = None
        self.C = None
        self.D = None

        self.R_0 = 0.0
        self.t_inc = 0.0
        self.t_inf = 0.0
        self.t_hosp = 0.0
        self.t_crit = 0.0
        self.m_a = 0.0
        self.c_a = 0.0
        self.f_a = 0.0

        self.days = 0

        self.population = population

        self.sol = None

    def init_model(self, params):
        self.days = params[0]
        self.S = params[1]
        self.E = params[2]
        self.I = params[3]
        self.R = params[4]
        self.H = params[5]
        self.C = params[6]
        self.D = params[7]

    # Susceptible equation
    def dS_dt(self, S, I, R_t, t_inf):
        return -(R_t / t_inf) * I * S

    # Exposed equation
    def dE_dt(self, S, E, I, R_t, t_inf, t_inc):
        return (R_t / t_inf) * I * S - (E / t_inc)

    # Infected equation
    def dI_dt(self, I, E, t_inc, t_inf):
        return (E / t_inc) - (I / t_inf)

    # Hospialized equation
    def dH_dt(self, I, C, H, t_inf, t_hosp, t_crit, m_a, f_a):
        return ((1 - m_a) * (I / t_inf)) + ((1 - f_a) * C / t_crit) - (H / t_hosp)

    # Critical equation
    def dC_dt(self, H, C, t_hosp, t_crit, c_a):
        return (c_a * H / t_hosp) - (C / t_crit)

    # Recovered equation
    def dR_dt(self, I, H, t_inf, t_hosp, m_a, c_a):
        return (m_a * I / t_inf) + (1 - c_a) * (H / t_hosp)

    # Deaths equation
    def dD_dt(self, C, t_crit, f_a):
        return f_a * C / t_crit

    def SEIDR_model(self, t, y, R_t, t_inc, t_inf, t_hosp, t_crit, m_a, c_a, f_a):
        """

        :param t: Time step for solve_ivp
        :param y: Previous solution or initial values
        :param R_t: Reproduction number
        :param t_inc: Average incubation period. Default 5.2 days
        :param t_inf: Average infectious period. Default 2.9 days
        :param t_hosp: Average time a patient is in hospital before either recovering or becoming critical. Default 4 days
        :param t_crit: Average time a patient is in a critical state (either recover or die). Default 14 days
        :param m_a: Fraction of infections that are asymptomatic or mild. Default 0.8
        :param c_a: Fraction of severe cases that turn critical. Default 0.1
        :param f_a: Fraction of critical cases that are fatal. Default 0.3
        :return:
        """

        if callable(R_t):
            reprod = R_t(t)
        else:
            reprod = R_t

        S, E, I, R, H, C, D = y

        S_out = self.dS_dt(S, I, reprod, t_inf)
        E_out = self.dE_dt(S, E, I, reprod, t_inf, t_inc)
        I_out = self.dI_dt(I, E, t_inc, t_inf)
        R_out = self.dR_dt(I, H, t_inf, t_hosp, m_a, c_a)
        H_out = self.dH_dt(I, C, H, t_inf, t_hosp, t_crit, m_a, f_a)
        C_out = self.dC_dt(H, C, t_hosp, t_crit, c_a)
        D_out = self.dD_dt(C, t_crit, f_a)
        return [S_out, E_out, I_out, R_out, H_out, C_out, D_out]

    def set_params(self, params):

        self.R_0 = params[0]
        self.t_inc = params[1]
        self.t_inf = params[2]
        self.t_hosp = params[3]
        self.t_crit = params[4]
        self.m_a = params[5]
        self.c_a = params[6]
        self.f_a = params[7]

    def solve(self):
        sol = solve_ivp(self.SEIDR_model, [0, self.days],
                        [self.S, self.E, self.I, self.R, self.H, self.C, self.D],
                        args=(self.R_0, self.t_inc, self.t_inf, self.t_hosp, self.t_crit, self.m_a, self.c_a, self.f_a),
                        t_eval=np.arange(self.days))

        self.sol = sol

    def get_infected(self):
        return self.sol.y[2] * self.population

    def get_deaths(self):
        return self.sol.y[6] * self.population

    def get_results(self):
        sol = {
            'S': self.sol.y[0],
            'E': self.sol.y[1],
            'I': self.sol.y[2],
            'R': self.sol.y[3],
            'H': self.sol.y[4],
            'C': self.sol.y[5],
            'D': self.sol.y[6],
        }
        return sol
