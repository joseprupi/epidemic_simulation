from ..Fit import Fit

from sklearn.metrics import mean_squared_error, mean_squared_log_error
from scipy.optimize import minimize
import numpy as np


class Basic(Fit):

    def __init__(self, data, model):
        self.data = data
        self.model = model
        self.params = None

    def eval(self, params, mean, estimator, days):

        self.model.set_params(params)
        self.model.solve(self.data.t)

        I_pred = np.clip(self.model.get_infected(), 0, np.inf)
        I_true = self.data.get_infected().to_numpy()[0]

        D_pred = np.clip(self.model.get_deaths(), 0, np.inf)
        D_true = self.data.get_deaths().to_numpy()[0]

        if estimator is 'MSE':
            error_infected = mean_squared_error(I_true, I_pred)
            error_deaths = mean_squared_error(D_true, D_pred)
        elif estimator is 'MSLE':
            error_infected = mean_squared_log_error(I_true[-days:], I_pred[-days:])
            error_deaths = mean_squared_log_error(D_true[-days:], D_pred[-days:])
        else:
            raise ValueError('Estimator not valid')

        if mean:
            error = np.mean([error_infected, error_deaths])
        else:
            error = error_infected + error_deaths

        print('Error: {}'.format(error))
        return error

    def fit_model(self, init_params, mean, estimator, days, bounds):
        self.params = init_params
        bounds = bounds
        self.sol = minimize(self.eval, self.params, args=(mean, estimator, days), bounds=bounds, method='L-BFGS-B', tol=0.0001)
        print(self.sol)

    def get_solution_parms(self):
        return self.sol['x']

