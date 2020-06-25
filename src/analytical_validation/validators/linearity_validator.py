import statsmodels.api as statsmodels
import statsmodels.stats.api as statsmodelsapi
import statsmodels.stats.stattools as stattools

from analytical_validation.exceptions import AnalyticalValueNotNumber, ConcentrationValueNotNumber, \
    AnalyticalValueNegative, ConcentrationValueNegative, DataNotList, \
    ResiduesNone, DataWasNotFitted


class LinearityValidator(object):
    """

    Example:
        >>> l = LinearityValidator(samples=[])
        >>> l.validate()
        False

        >>> l = LinearityValidator(samples=[1, 2, 3])
        >>> l.validate()
        True
    """

    def __init__(self, analytical_data, concentration_data, alpha=0.05):
        """
        Validate the linearity of the method.
        :param analytical_data: List containing all measured analytical signal.
        :type analytical_data: list
        :param concentration_data: List containing the concentration for each analytical signal
        :type concentration_data: list
        :param alpha: Significance (default value = 0.05)
        :type alpha: float
        :raises AnalyticalValueNotNumber: When a value in analytical data isn't a float.
        :raises ConcentrationNotNumber: When a value in concentration data isn't a float.
        :raises AnalyticalValueNegative: When a value in analytical data is negative.
        :raises ConcentrationValueNegative: When a value in concentration data is negative.
        """
        self.analytical_data = analytical_data
        self.concentration_data = concentration_data
        self.alpha = alpha
        # Ordinary least squares linear regression coefficients
        self.fitted_result = None
        # Anova parameters
        self.has_required_parameters = False
        # Durbin Watson parameters
        self.durbin_watson_value = None
        if isinstance(analytical_data, list) is False:
            raise DataNotList()
        if isinstance(concentration_data, list) is False:
            raise DataNotList()
        if not all(isinstance(value, float) for value in self.analytical_data):
            raise AnalyticalValueNotNumber()
        if not all(isinstance(value, float) for value in self.concentration_data):
            raise ConcentrationValueNotNumber()
        if not all(value > 0 for value in self.analytical_data):
            raise AnalyticalValueNegative()
        if not all(value > 0 for value in self.concentration_data):
            raise ConcentrationValueNegative()

    def validate(self):
        """Validate the linearity of given data.
        :return: True if data is linear; otherwise, False.
        :rtype: bool
        """
        pass

    def ordinary_least_squares_linear_regression(self):
        """Fit the data using the ordinary least squares method of Linear Regression."""
        concentration_data = statsmodels.add_constant(self.concentration_data)
        model = statsmodels.OLS(self.analytical_data, concentration_data)
        self.fitted_result = model.fit()

    @property
    def intercept(self):
        """The intercept value.

        :return: The intercept value.
        :rtype: numpy.float64
        """
        # TODO: create tests
        return self.fitted_result.params[0]

    @property
    def slope(self):
        """The slope value.

        :return: The slope value.
        :rtype: numpy.float64
        """
        # TODO: create tests
        return self.fitted_result.params[1]

    @property
    def is_homokedastic(self):
        """The homokedastic data information.

        The data is homokedastic when the variance is constant; otherwise it is heterokedastic.
        Uses the Breusch-Pagan test. In the Breusch-Pagan test to check homoskedasticity the p value of fitted
        results basaed on regression model is needed.
        If the (p-value) > 0.05, the method is homoskedastic, else is heteroskedastic

        :return: The homokedastic data information.
        :rtype: bool
        """
        # TODO: improve testes - see valid_r_squared
        return self.breusch_pagan_pvalue > self.alpha

    @property
    def significant_slope(self):
        """The slope significance avaliation.

        If the (p-value) < alpha, the slope is significant.

        :return: The avaliation of slope siginificance.
        :rtype: bool
        """
        # TODO: improve testes - see valid_r_squared
        return self.fitted_result.pvalues[1] < self.alpha

    @property
    def insignificant_intercept(self):
        """The slope significance avaliation.

        If the (p-value) > alpha, the intercept is insignificant.

        :return: The avaliation of intercept insiginificance.
        :rtype: bool
        """
        # TODO: improve testes - see valid_r_squared
        return self.fitted_result.pvalues[0] > self.alpha

    @property
    def valid_r_squared(self):
        """The slope significance avaliation.

        If the r squared > 0.990, the correlation coefficient is valid.

        :return: The avaliation of correlation coefficient.
        :rtype: bool
        """
        return self.fitted_result.rsquared >= 0.990

    @property
    def valid_regression_model(self):
        """The slope significance avaliation.

        If the r squared > 0.990, slope is significant and intercept is
        insignificant,regression model is valid.

        :return: The validity of regression model.
        :rtype: bool
        """
        # TODO: create test
        return self.significant_slope and self.insignificant_intercept and self.valid_r_squared

    def run_breusch_pagan_test(self):
        """Run the Breusch-Pagan test."""
        if self.fitted_result is None:
            # TODO: create specific exception
            raise Exception("There is not a regression model to check the homokedasticity.")
        # Calculate the residues based on fitted model of linear regression
        breusch_pagan_test = statsmodelsapi.het_breuschpagan(self.fitted_result.resid,
                                                             self.fitted_result.model.exog)
        # labels = ["LM Statistic", "LM-Test p-value", "F-Statistic", "F-Test p-value"]
        self.breusch_pagan_pvalue = float(breusch_pagan_test[1])
        # TODO: Deal with heteroskedastic, removing outliers or using Weighted Least Squares Regression

    def check_outliers(self):
        """Check for outliers in the data set
        using the Dixon Q value test."""
        pass

    def check_residual_autocorrelation(self):
        """Check the residual autocorrelation in a
        regression analysis using the Durbin-Watson test.

        The closer the Durbin-Watson value is to 0, the
        more evidence for positive serial correlation.
        The closer to 4, the more evidence for negative
        serial correlation.
        """
        if self.fitted_result is None:
            raise DataWasNotFitted()
        # TODO: check if property is needed
        value = stattools.durbin_watson(self.fitted_result.resid)
        if 0 <= value <=4:
            self.durbin_watson_value = value
        else:
            # TODO: Create specific exception
            raise Exception()
