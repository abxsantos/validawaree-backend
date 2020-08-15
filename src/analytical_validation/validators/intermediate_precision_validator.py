import numpy
import pandas
from statsmodels.formula.api import ols
import statsmodels.api as statsmodels


class IntermediatePrecision(object):
    """
    Example:
        >>> analytical_data = {"day1": [[0.1,0.2,0.1],[0.3,0.3,0.32],[0.41,0.43,0.45],[0.51,0.53,0.55]], "day2": [[0.1,0.2,0.1],[0.3,0.3,0.32],[0.41,0.43,0.45],[0.51,0.53,0.55]], "analyst_a": [[0.1,0.2,0.1],[0.3,0.3,0.32],[0.41,0.43,0.45],[0.51,0.53,0.55]], "analyst_b": [[0.1,0.2,0.1],[0.3,0.3,0.32],[0.41,0.43,0.45],[0.51,0.53,0.55]],}
        >>> concentration_data = {"day1":[[0.01,0.02,0.01],[0.03,0.03,0.032],[0.041,0.043,0.045],[0.051,0.053,0.055]], "day2":[[0.01,0.02,0.01],[0.03,0.03,0.032],[0.041,0.043,0.045],[0.051,0.053,0.055]], "analyst_a":[[0.01,0.02,0.01],[0.03,0.03,0.032],[0.041,0.043,0.045],[0.051,0.053,0.055]], "analyst_b":[[0.01,0.02,0.01],[0.03,0.03,0.032],[0.041,0.043,0.045],[0.051,0.053,0.055]]}
        >>> intermediate_precision = IntermediatePrecision(analytical_data, concentration_data)
        >>> intermediate_precision_is_valid = intermediate_precision.validate_intermediate_precision
    """

    def __init__(self, analytical_data, concentration_data, intercept, slope, alpha=0.05):
        """
        The intermediate precision is the proximity between the results obtained in an analysis of the same sample, in
        the same laboratory, in at least two different days and between two different analysts.

        This class is used to validate the precision of an analytical method given the analytical and concentration data
        of different days and analysts ordered inside a dictionary containing the data inside a list of lists.
        :param analytical_data:
        :type analytical_data: dict
        :param concentration_data:
        :type concentration_data: dict
        :param alpha:
        :type alpha: float
        """
        self.original_analytical_data = analytical_data
        self.original_concentration_data = concentration_data
        self.intercept = intercept
        self.slope = slope
        self.alpha = alpha

        self.obtained_concentration = []
        self.two_way_anova_result = None

    def calculate_obtained_concentrations(self):
        """
        Calculate the concentration given a validated linear regression slope, intercept and intermediate precision
        analytical data.
        :return: Concentration data calculated with the regression coefficients.
        """
        pass

    def two_way_anova(self):
        """
        Creates the two-way ANOVA object containing statistical
        properties of the intermediate precision given data a set.
        """
        pass
