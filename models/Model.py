class Model(object):
    def init_model(self, **kwargs):
        raise ValueError('Not implemented')

    def set_params(self, **kwargs):
        raise ValueError('Not implemented')

    def get_infectred(self):
        raise ValueError('Not implemented')

    def get_deaths(self):
        raise ValueError('Not implemented')

    def solve(self):
        raise ValueError('Not implemented')

    def get_results(self):
        raise ValueError('Not implemented')