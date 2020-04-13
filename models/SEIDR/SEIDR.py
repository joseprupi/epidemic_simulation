from ..Model import Model

import numpy as np
from scipy.integrate import solve_ivp


class SEIDR(Model):

    def __init__(self):
        self.S = 999
        self.E = 0
        self.I_0 = 1
        self.I_icu = 0
        self.I_in = 0
        self.I_out = 0
        self.D = 0
        self.R = 0

        self.mu = 0.0
        self.beta = 1/1.5
        self.nu = 0.0
        self.sigma = 1/3
        self.omega_icu = (1/7) * 0.12
        self.omega_in = (1/3) * 0.63
        self.omega_out = (1/2) * 0.25
        self.gamma_icu = (1/7) * (1 - 0.5)
        self.gamma_in = 1/11
        self.gamma_out = 1/12
        self.lambda_icu = (1/7) * 0.5

        self.days = 90

        self.sol = None

    def init_model(self, **kwargs):
        self.days = kwargs['t']
        self.S = kwargs['S']
        self.I_0 = kwargs['I_0']
        self.D = kwargs['D']

    def set_params(self, params):
        self.mu = params[0]
        self.beta = params[1]
        self.nu = params[2]
        self.sigma = params[3]
        self.omega_icu = params[4]
        self.omega_in = params[5]
        self.omega_out = params[6]
        self.gamma_icu = params[7]
        self.gamma_in = params[8]
        self.gamma_out = params[9]
        self.lambda_icu = params[10]

    def dS_dt(self, S, E, I_0, I_icu, I_in, I_out, R, mu, beta, nu):
        I = I_0 + I_icu + I_in + I_out
        return mu * (E + I_0 + + I_icu + I_in+ I_out + R) - beta * (I / (I + S)) * S - nu * S

    def dE_dt(self, S, E, I_0, I_icu, I_in, I_out, mu, beta, sigma):
        I = I_0 + I_icu + I_in + I_out
        return beta * (I / (I + S)) * S - (mu + sigma) * E

    def dI_0_dt(self, E, I_0, I_icu, I_in, I_out, sigma, mu, omega_icu, omega_in, omega_out):
        return sigma * E - mu * (I_0 + I_icu + I_in + I_out) - omega_icu * I_0 - omega_in * I_0 - omega_out * I_0

    def dI_icu_dt(self, I_0, I_icu, omega_icu, gamma_icu):
        return omega_icu * I_0 - gamma_icu * I_icu

    def d_I_in_dt(self, I_0, I_in, omega_in, gamma_in):
        return omega_in * I_0 - gamma_in * I_in

    def d_I_out_dt(self, I_0, I_out, omega_out, gamma_out):
        return omega_out * I_0 - gamma_out * I_out

    def dD_dt(self, I_icu, lambda_icu):
        return lambda_icu * I_icu

    def dR_dt(self, S, I_icu, I_in, I_out, R, gamma_icu, lambda_icu, gamma_in, gamma_out, mu, nu):
        return (gamma_icu - lambda_icu) * I_icu + gamma_in * I_in + gamma_out * I_out - mu * R + nu * S

    def SEIDR_model(self, t, y, mu, beta, nu, sigma, omega_icu, omega_in, omega_out, gamma_icu, gamma_in, gamma_out,
                    lambda_icu):
        S, E, I_0, I_icu, I_in, I_out, D, R = y

        S_out = self.dS_dt(S, E, I_0, I_icu, I_in, I_out, R, mu, beta, nu)
        E_out = self.dE_dt(S, E, I_0, I_icu, I_in, I_out, mu, beta, sigma)
        I_0_out = self.dI_0_dt(E, I_0, I_icu, I_in, I_out, sigma, mu, omega_icu, omega_in, omega_out)
        I_icu_out = self.dI_icu_dt(I_0, I_icu, omega_icu, gamma_icu)
        I_in_out = self.d_I_in_dt(I_0, I_in, omega_in, gamma_in)
        I_out_out = self.d_I_out_dt(I_0, I_out, omega_out, gamma_out)
        D_out = self.dD_dt(I_icu, lambda_icu)
        R_out = self.dR_dt(S, I_icu, I_in, I_out, R, gamma_icu, lambda_icu, gamma_in, gamma_out, mu, nu)

        return [S_out, E_out, I_0_out, I_icu_out, I_in_out, I_out_out, D_out, R_out]

    def solve(self):
        sol = solve_ivp(self.SEIDR_model, [0, self.days],
                        [self.S, self.E, self.I_0, self.I_icu, self.I_in, self.I_out,
                         self.D, self.R],
                        args=(self.mu, self.beta, self.nu, self.sigma, self.omega_icu, self.omega_in, self.omega_out,
                              self.gamma_icu, self.gamma_in, self.gamma_out,
                              self.lambda_icu),
                        t_eval=np.arange(self.days))

        self.sol = sol

    def get_infected(self):
        I_0 = self.sol.y[2]
        I_icu = self.sol.y[3]
        I_in = self.sol.y[4]
        I_out = self.sol.y[5]
        return I_0 + I_icu + I_in + I_out

    def get_deaths(self):
        return self.sol.y[6]

    def get_results(self):
        sol = {
            'S': self.sol.y[0],
            'E': self.sol.y[1],
            'I': self.sol.y[2] + self.sol.y[3] + self.sol.y[4] + self.sol.y[5],
            'D': self.sol.y[6],
            'R': self.sol.y[7],
        }
        return sol
