class AnalyticalValueNotNumber(Exception):
    def __init__(self):
        super().__init__("One of the analytical values is not a number!")


class ConcentrationValueNotNumber(Exception):
    def __init__(self):
        super().__init__("One of the concentration values is not a number!")


class AnalyticalValueNegative(Exception):
    def __init__(self):
        super().__init__("Negative value for analytical signal is not valid!")


class ConcentrationValueNegative(Exception):
    def __init__(self):
        super().__init__("Negative value for concentration value is not valid!")
