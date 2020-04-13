# Epidemic simulation module

Epidemic simulation module to fit and forecast epidemics dynamics. 

The three main parts of the module are:
* Data sources: Data sources to fit the models. Currently John Hopkins data available
* Fit classes: Classes where the minimization is defined
* Models: Any model to fit and used to forecast

## Extend the module

To extend the module override the correspondant base classes for:
* Data sources
* Fit classes
* Models

## Example
See below a sample code and the outputs

```python
from data_sources.jh import JH
from models.SEIDR import SEIDR
from fit.basic import Basic
from plot.plot_model import plot_model_results, plot_model_prediction, plot_model_prediction_all

import numpy as np

# Initialize John Hopkins data
jh_data = JH.JH()
# Uncoment below line to download last John Hopkins data
#jh_data.update()
jh_data.process_data()

# Set the area to be used to fit the model
area = {
    'Country_Region': 'US'
}

# Set the initial date and area
start_date = '1/22/20'

jh_data.set_area(area)
jh_data.set_dates(start_date)

# Get the infected and death number from first day
infected_0 = jh_data.get_infected()[start_date].iloc[0]
deaths_0 = jh_data.get_deaths().iloc[0][start_date]

# Get the length of the data
t = len(jh_data.get_infected().columns)

# Get the population
population = jh_data.get_population()

# Initialize the model
SEIDR_model = SEIDR.SEIDR()
SEIDR_model.init_model(t=t, S=population, I_0=infected_0, D=deaths_0)

# Initialize the basic fit class with the data and the model
basic_fit = Basic.Basic(jh_data, SEIDR_model)

# Set the initial params to start minimization and execute it
mu = 0.0
beta = 1 / 1.5
nu = 0.0
sigma = 1 / 3
omega_icu = (1 / 7) * 0.12
omega_in = (1 / 3) * 0.63
omega_out = (1 / 2) * 0.25
gamma_icu = (1 / 7) * (1 - 0.5)
gamma_in = 1 / 11
gamma_out = 1 / 12
lambda_icu = (1 / 7) * 0.5

params = [mu, beta, nu, sigma, omega_icu, omega_in, omega_out, gamma_icu, gamma_in, gamma_out, lambda_icu]

# Set the bounds
bounds = ((0.1, 0.5), (0, np.inf), (0, np.inf), (0, np.inf), (0, np.inf), (0, np.inf), (0.1, np.inf), (0.1, np.inf),
                  (0, np.inf), (0, np.inf), (0, np.inf))

# Fit the model with the init params, bounds
basic_fit.fit_model(params, True, 'MSLE', 21, bounds)

sol_params = basic_fit.get_solution_parms()

SEIDR_model.set_params(sol_params)
SEIDR_model.solve()
plot_model_results(SEIDR_model.get_infected(), jh_data.get_infected(), SEIDR_model.get_deaths(), jh_data.get_deaths())

SEIDR_model.init_model(t=200, S=population, I_0=infected_0, D=deaths_0)
SEIDR_model.set_params(sol_params)
SEIDR_model.solve()
plot_model_prediction(SEIDR_model.get_infected(), SEIDR_model.get_deaths())

plot_model_prediction_all(SEIDR_model.get_results())

```
![Model results](/plot/model_results.png)
Format: ![Alt Text](url)
