from algDev.models.equity import Equity


class SNP(Equity):
    """Special class for S&P 500."""

    def __init__(self, data_file):
        super().__init__(data_file)
