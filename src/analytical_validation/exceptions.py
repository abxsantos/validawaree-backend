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
        super().__init__("One of the input data is not a list.")


class AlreadyCleanedOutliers(Exception):
    def __init__(self):
        super().__init__("Already removed the outliers from data set.")


class DataNotConsistent(Exception):
    def __init__(self):
        super().__init__("Data is not consistent.")


class DataNotListOfLists(Exception):
    def __init__(self):
        super().__init__("The given data is not a list of lists.")


class DataNotSymmetric(Exception):
    def __init__(self):
        super().__init__("The given data is not symmetric. Check if there's a value missing.")


class DataNotNumber(Exception):
    def __init__(self):
        super().__init__("The data contains a value that isn't a number.")


class DataIsEmpty(Exception):
    def __init__(self):
        super().__init__("The data is empty!")


class DataIsOutOfRange(Exception):
    def __init__(self):
        super().__init__("Dixon outlier Q test can't be used with less than 3 or more than 28 values in a data set.")


class AlphaNotValid(Exception):
    def __init__(self):
        super().__init__("The alpha value is not valid. Only 0.01, 0.05, 0.10 are accepted values.")


class DirectionNotBoolean(Exception):
    def __init__(self):
        super().__init__("The left and right input values should be booleans (True or False).")


class ResiduesNone(Exception):
    def __init__(self):
        super().__init__("There are no residues!")


class DataWasNotFitted(Exception):
    def __init__(self):
        super().__init__("There is no regression model!")


class DurbinWatsonValueError(Exception):
    def __init__(self):
        super().__init__("The Durbin Watson value is out of bounds. Should be less than 4 and more than 0.")


class OulierCheckError(Exception):
    def __init__(self):
        super().__init__("Something went wrong checking outliers. Check your input format, data must be symmetric.")


class ValueNotValid(Exception):
    def __init__(self):
        super().__init__("Non number values are not valid. Check and try again.")


class NegativeValue(Exception):
    def __init__(self):
        super().__init__("Negative values are not valid. Check and try again.")


custom_exceptions = {
    "DataNotListOfLists": {"message": "The given data is not a list of lists.", "status": 400},
    "DataNotList": {"message": "There is no regression model!", "status": 400},
    "ValueNotValid": {"message": "Non number values are not valid. Check and try again.",
                      "status": 400},
    "NegativeValue": {"message": "Negative values are not valid. Check and try again.",
                      "status": 400},
    "DataNotSymmetric": {"message": "The given data is not symmetric. Check if there's a value missing.",
                         "status": 400},
}
