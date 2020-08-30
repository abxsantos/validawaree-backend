import numpy
import pandas
from statsmodels.formula.api import ols
import statsmodels.api as statsmodels
from analytical_validation.exceptions import IncorrectIntermediatePrecisionData


class IntermediatePrecision(object):
    """
    Example:
        >>> analytical_data = [0.1, 0.11, 0.12, 0.1, 0.11, 0.12, 0.1, 0.11, 0.12, 0.1, 0.11, 0.12,]
        >>> intercept = 0.0001
        >>> slope = 20.2
        >>> alpha = 0.05
        >>> intermediate_precision = IntermediatePrecision(analytical_data, intercept, slope, alpha)
        >>> intermediate_precision_is_valid = intermediate_precision.validate_intermediate_precision
    """

    def __init__(self, analytical_data, intercept, slope, alpha=0.05):
        """
        The intermediate precision is the proximity between the results obtained in an analysis of the same sample, in
        the same laboratory, in at least two different days and between two different analysts.

        This class is used to validate the precision of an analytical method given the analytical and concentration data
        of different days and analysts ordered inside a dictionary containing the data inside a list of lists.
        :param analytical_data:
        :type analytical_data: list
        :param intercept:
        :type intercept: float
        :param slope:
        :type slope: float
        :param alpha:
        :type alpha: float
        """
        self.original_analytical_data = analytical_data
        self.intercept = intercept
        self.slope = slope
        self.alpha = alpha

        self.calculated_concentration = []
        self.two_way_anova_result = None
        self.is_intermediate_precise = False

    def calculate_obtained_concentrations(self):
        """
        Calculate the concentration given a validated linear regression slope, intercept and intermediate precision
        analytical data.
        :return: Concentration data calculated with the regression coefficients.
        """
        self.calculated_concentration = []
        if isinstance(self.original_analytical_data, list) is False:
            raise IncorrectIntermediatePrecisionData()
        for value in self.original_analytical_data:
            if value is None:
                self.calculated_concentration.append(value)
            elif isinstance(value, float) or isinstance(value, int):
                self.calculated_concentration.append(value * self.slope + self.intercept)
            else:
                raise IncorrectIntermediatePrecisionData()

    def two_way_anova(self):
        """
        Creates the two-way ANOVA object containing statistical
        properties of the intermediate precision given data a set.
        """
        data_set_length = len(self.calculated_concentration)
        data_frame = pandas.DataFrame({"days": numpy.repeat(["day 1", "day 2"], data_set_length // 2),
                                       "analyst": numpy.tile(
                                           numpy.repeat(["analyst a", "analyst b"], data_set_length // 4), 2),
                                       "concentration": self.calculated_concentration})
        model = ols('concentration ~ C(days) + C(analyst) + C(days):C(analyst)', data=data_frame).fit()
        self.two_way_anova_result = statsmodels.stats.anova_lm(model, typ=2)

    def validate_intermediate_precision(self):
        """
        Validates the intermediate precision of given data.
        :return: True if the given data is valid. False otherwise.
        :rtype: bool
        """
        self.calculate_obtained_concentrations()
        self.two_way_anova()
        # TODO: Check conditionals for intermediate precision acceptance
        self.is_intermediate_precise = True

