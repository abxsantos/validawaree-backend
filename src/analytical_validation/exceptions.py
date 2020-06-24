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


class AverageValueNotNumber(Exception):
    def __init__(self):
        super().__init__("One of the average values is not a number!")


class AverageValueNegative(Exception):
    def __init__(self):
        super().__init__("Negative value for average value is not valid!")


class DataNotList(Exception):
    def __init__(self):
        super().__init__("One of the input datas is not a list.")


class AlreadyCleanedOutliers(Exception):
    def __init__(self):
        super().__init__("Already removed the outliers from data set.")


class DataNotConsistent(Exception):
    def __init__(self):
        super().__init__("Data is not consistent.")


class DataNotListOfLists(Exception):
    def __init__(self):
        super().__init__("The given data is not a list of lists.")


class DataNotNumber(Exception):
    def __init__(self):
        super().__init__("The data contains a value that isn't a number.")


class DataIsEmpty(Exception):
    def __init__(self):
        super().__init__("The data is empty!")


class DataTooSmall(Exception):
    def __init__(self):
        super().__init__("At least 3 data points are required")


class DataTooBig(Exception):
    def __init__(self):
        super().__init__("Dixon outlier Q test can't be used with more than 28 values in a data set.")


class AlphaNotValid(Exception):
    def __init__(self):
        super().__init__("The alpha value is not valid. Only 0.01, 0.05, 0.10 are accepted values.")


class DirectionNotBoolean(Exception):
    def __init__(self):
        super().__init__("The left and right input values should be booleans (True or False).")