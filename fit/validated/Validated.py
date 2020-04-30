from ..Fit import Fit
from ..basic import Basic
from plot.plot_model import plot_model_results

from sklearn.metrics import mean_squared_error, mean_squared_log_error
import numpy as np


class Validated(Fit):

    def __init__(self, data, model):
        self.data = data
        self.model = model
        self.params = None
        self.sol = None

    def eval(self, params, mean, estimator, days):
        pass

    def fit_model(self, init_params, mean, estimator, days, val_days, bounds):
        self.params = init_params
        bounds = bounds
        all_days = self.data.t
        train_days = self.data.t - val_days

        basic_fit = Basic.Basic(self.data, self.model)
        self.data.t = train_days
        train_error = basic_fit.fit_model(init_params, True, 'MSLE', days, bounds)
        self.sol = basic_fit.get_solution_parms()

        self.model.set_params(self.get_solution_parms())
        self.model.solve(all_days)

        # plot_model_results(self.model.get_infected(), self.data.get_infected(), self.model.get_deaths(),
        #                    self.data.get_deaths())

        I_pred = np.clip(self.model.get_infected()[-val_days:], 0, np.inf)
        I_true = self.data.get_infected().to_numpy()[0][-val_days:]

        D_pred = np.clip(self.model.get_deaths()[-val_days:], 0, np.inf)
        D_true = self.data.get_deaths().to_numpy()[0][-val_days:]

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
        return train_error, error

    def get_solution_parms(self):
        return self.sol
