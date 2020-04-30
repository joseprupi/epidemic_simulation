from ..Source import Source

import git
from git import Repo
import pandas as pd

import os


class JH(Source):

    def __init__(self):

        self.data_path = os.path.dirname(os.path.abspath(__file__)) + '/git_data/COVID-19/'
        self.t = None

        self.confirmed_US = None
        self.deaths_US = None

        self.confirmed_global = None
        self.deaths_global = None

        self.areas_US = None
        self.areas_global = None

        self.population = None

    def set_dates(self, start_date, t=0):
        self.start_date = start_date
        if t is not 0:
            self.t = t
        else:
            start_date_pos = self.deaths_US.columns.get_loc(self.start_date)
            self.t = len(self.deaths_US.columns[start_date_pos:])

    def set_area(self, area):
        self.area = area

    def get_areas_list(self):
        return None

    def get_deaths(self):
        """
        :param area: a dictionary like
        {
        Province_State:'value',
        Country_Region:'value',
        Town_City:'value',
        }
        Town_City just applies to US.

        :param init_date: date with format MM/dd
        :param end_date: date with format MM/dd
        :return:
        """
        Province_State = ''
        Country_Region = ''
        Town_City = ''

        df = None

        if 'Province_State' in self.area:
            Province_State = self.area['Province_State']

        if 'Country_Region' in self.area:
            Country_Region = self.area['Country_Region']

        if 'Town_City' in self.area:
            Town_City = self.area['Town_City']

        if Country_Region is 'US':
            df = self.deaths_US[(self.deaths_US.Country_Region == 'US')]
            if Province_State is not '':
                df = df[(self.deaths_US.Province_State == Province_State)]
            if Town_City is not '':
                df = df[(self.deaths_US.Town_City == Town_City)]

        else:
            if Country_Region is not '':
                df = self.deaths_global[(self.deaths_global.Country_Region == Country_Region)]
            if Province_State is not '':
                df = df[(self.deaths_global.Province_State == Province_State)]

        start_date_col = df.columns.get_loc(self.start_date)
        df = df.iloc[:, start_date_col:start_date_col + self.t]

        return df.cumsum()[-1:]

    def get_infected(self):
        """
        :param area: a dictionary like
        {
        Province_State:'value',
        Country_Region:'value',
        Town_City:'value',
        }
        Town_City just applies to US.

        :param init_date: date with format MM/dd
        :param end_date: date with format MM/dd
        :return:
        """
        Province_State = ''
        Country_Region = ''
        Town_City = ''

        df = None

        if 'Province_State' in self.area:
            Province_State = self.area['Province_State']

        if 'Country_Region' in self.area:
            Country_Region = self.area['Country_Region']

        if 'Town_City' in self.area:
            Town_City = self.area['Town_City']

        if Country_Region is 'US':
            df = self.confirmed_US[(self.confirmed_US.Country_Region == 'US')]
            if Province_State is not '':
                df = df[(self.confirmed_US.Province_State == Province_State)]
            if Town_City is not '':
                df = df[(self.confirmed_US.Town_City == Town_City)]

        else:
            if Country_Region is not '':
                df = self.confirmed_global[(self.confirmed_global.Country_Region == Country_Region)]
            if Province_State is not '':
                df = df[(self.confirmed_global.Province_State == Province_State)]

        start_date_col = df.columns.get_loc(self.start_date)
        df = df.iloc[:, start_date_col:start_date_col + self.t]


        return df.cumsum()[-1:]

    def update(self):
        self.update_git()
        self.process_data()

    def update_git(self):

        print()
        if os.path.exists(self.data_path):
            repo = git.Repo(os.path.dirname(self.data_path))
            origin = repo.remotes.origin
            origin.pull()
        else:
            Repo.clone_from("https://github.com/CSSEGISandData/COVID-19", os.path.dirname(self.data_path))

    def process_data(self):

        # Read confirmed cases from US csv
        self.confirmed_US = pd.read_csv(
            self.data_path + 'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv', keep_default_na=False)

        self.confirmed_US = self.confirmed_US.rename(columns={'Admin2': 'Town_City'})

        # Read deaths from US csv
        self.deaths_US = pd.read_csv(
            self.data_path + 'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')

        self.deaths_US = self.deaths_US.rename(columns={'Admin2': 'Town_City'})

        # Read confirmed cases from US csv
        self.confirmed_global = pd.read_csv(
            self.data_path + 'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', keep_default_na=False)

        self.confirmed_global = self.confirmed_global.rename(columns={'Province/State': 'Province_State'})
        self.confirmed_global = self.confirmed_global.rename(columns={'Country/Region': 'Country_Region'})

        # Read deaths from US csv
        self.deaths_global = pd.read_csv(
            self.data_path + 'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv', keep_default_na=False)

        self.deaths_global = self.deaths_global.rename(columns={'Province/State': 'Province_State'})
        self.deaths_global = self.deaths_global.rename(columns={'Country/Region': 'Country_Region'})

        # Read the list of available areas
        self.areas_US = self.confirmed_US[['Town_City', 'Province_State', 'Country_Region']]
        self.areas_global = self.confirmed_global[['Province_State','Country_Region']]

        # Read the population of areas
        self.population = pd.read_csv(
            self.data_path + 'csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv', keep_default_na=False)

        self.population = self.population.rename(columns={'Admin2': 'Town_City'})

    def get_date_range(self):
        col = self.confirmed_US.columns.get_loc('Combined_Key')
        start_date = self.confirmed_US.columns[col + 1:]
        end_date = self.confirmed_US.columns[-1]
        return start_date, end_date

    def get_population(self):
        Province_State = ''
        Country_Region = ''
        Town_City = ''

        df = None

        if 'Province_State' in self.area:
            Province_State = self.area['Province_State']

        if 'Country_Region' in self.area:
            Country_Region = self.area['Country_Region']

        if 'Town_City' in self.area:
            Town_City = self.area['Town_City']

        df = self.population
        df = df[(df.Country_Region == Country_Region)]
        df = df[(df.Province_State == Province_State)]
        df = df[(df.Town_City == Town_City)]

        if len(df.index) > 1:
            raise ValueError('Invalid area')
        else:
            return int(df.iloc[0]['Population'])