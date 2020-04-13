class Source(object):
    def __init__(self, source_id=''):
        self.source_id = None
        self.area = None
        self.start_date = None
        self.t = None
        self.deaths = None
        self.confirmed = None

    def set_dates(self, start_date, t):
        raise ValueError('Not implemented')

    def set_area(self, area):
        raise ValueError('Not implemented')

    def get_deaths(self):
        raise ValueError('Not implemented')

    def get_n_days(self):
        raise ValueError('Not implemented')

    def get_infected(self):
        raise ValueError('Not implemented')

    def get_population(self):
        raise ValueError('Not implemented')

    def update(self):
        raise ValueError('Not implemented')

    def get_date_range(self):
        raise ValueError('Not implemented')
