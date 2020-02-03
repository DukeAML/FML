from algDev.models.indicators import Indicators


class Index(Indicators):

    def __init__(self, data_file):
        super().__init__(data_file)
