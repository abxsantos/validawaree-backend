import statsmodels.api as statsmodels
import statsmodels.stats.api as statsmodelsapi

from analytical_validation.exceptions import AnalyticalValueNotNumber, ConcentrationValueNotNumber, \
    AnalyticalValueNegative, ConcentrationValueNegative, AverageValueNotNumber, AverageValueNegative, DataNotList


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
        :param averages_data: List containing the average for each set of analytical signal with the same concentration
        :type averages_data: list
        :param std_dev_data: List containing the standard deviation for each set of analytical signal with the same concentration
        :type std_dev_data: list
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
        self.slope_pvalue = None
        self.intercept_pvalue = None
        self.r_squared = None
        self.fitted_result = None
        self.slope = None
        self.intercept = None
        self.stderr = None

        self.is_homokedastic = False

        self.has_required_parameters = False
        self.significant_slope = False
        self.insignificant_intercept = False
        self.valid_r_squared = False

        self.valid_regression_model = False
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
        """Validate the given data.

        :return: True if data is valid; otherwise, False.
        :rtype: bool
        """
        pass

    def ordinary_least_squares_linear_regression(self):
        """Fit the data using the ordinary least squares method of Linear Regression.

        :raises AnalyticalValueNotNumber: When a value in analytical data isn't a float.
        :raises ConcentrationNotNumber: When a value in concentration data isn't a float.
        :raises AnalyticalValueNegative: When a value in analytical data is negative.
        :raises ConcentrationValueNegative: When a value in concentration data is negative.
        """
        try:
            # Check for values != float
            if not all(isinstance(value, float) for value in self.analytical_data):
                raise AnalyticalValueNotNumber()
            if not all(isinstance(value, float) for value in self.concentration_data):
                raise ConcentrationValueNotNumber()
            if not all(value > 0 for value in self.analytical_data):
                raise AnalyticalValueNegative()
            if not all(value > 0 for value in self.concentration_data):
                raise ConcentrationValueNegative()
            # Create the model and fit the result
            concentration_data = statsmodels.add_constant(self.concentration_data)
            model = statsmodels.OLS(self.analytical_data, concentration_data)
            fitted_result = model.fit()
            # Retrieve hypothesis parameters
            self.intercept_pvalue, self.slope_pvalue = fitted_result.pvalues
            self.r_squared = fitted_result.rsquared
            self.fitted_result = fitted_result
            # Retrieve coefficients
            self.intercept, self.slope = fitted_result.params
            self.stderr = fitted_result.bse[1]
            self.summary = self.fitted_result.summary(alpha=self.alpha, title="Ordinary Least Square Results")
        except:
            raise Exception("Something went wrong.")

    def check_homokedasticity(self):
        """Check if the given data is homokedastic
        (the variance is constant) or heterokedastic
        (the variance is not constant), using the
        Breusch-Pagan test. In the Breusch-Pagan test
        to check homoskedasticity the p value of fitted
        results basaed on regression model is needed.
        If the (p-value) > 0.05, the method is homoskedastic,
        else is heteroskedastic
        """
        if self.fitted_result is None:
            raise Exception("There is not a regression model to check the homokedasticity.")
        try:
            # Calculate the residues based on fitted model of linear regression
            breusch_pagan_test = statsmodelsapi.het_breuschpagan(self.fitted_result.resid,
                                                                 self.fitted_result.model.exog)

            # labels = ["LM Statistic", "LM-Test p-value", "F-Statistic", "F-Test p-value"]
            self.breusch_pagan_pvalue = float(breusch_pagan_test[1])



            # TODO: Deal with heteroskedastic, removing outliers or using Weighted Least Squares Regression
            # Run the Breusch-Pagan test to check homoskedasticity
            # If the (p-value) > 0.05, the method is homoskedastic, else is heteroskedastic
            # Check Heteroskedasticity
            if self.breusch_pagan_pvalue > self.alpha:
                self.is_homokedastic = True
        except:
            raise Exception("Something went wrong.")

    def check_hypothesis(self):
        """Check the null hypothesis for significance of intercept, slope and r²\n
        # H0: a = 0\n
        # H1: a != 0\n
        # Slope p-value < alpha the slope is != 0\n
        # Intercept p-value > alpha the intercept = 0\n
        # R² >= 0.990
        """
        try:
            if self.slope_pvalue or self.intercept_pvalue or self.r_squared is None:
                self.ordinary_least_squares_linear_regression()
                self.has_required_parameters = True
            self.has_required_parameters = True
            #p-value < 0.05 the slope is != 0
            if self.slope_pvalue < self.alpha:
                self.significant_slope = True
            if self.intercept_pvalue > self.alpha:
                self.insignificant_intercept = True
            if self.r_squared >= 0.990:
                self.valid_r_squared = True
            if self.significant_slope and self.insignificant_intercept and self.valid_r_squared:
                self.valid_regression_model = True
        except:
            raise Exception("Something went worng.")

    def check_outliers(self):
        """Check for outliers in the data set
        using the Dixon Q value test."""

        pass

    def check_residual_autocorrelation(self):
        """Check the residual autocorrelation in a
        regression analysis using the Durbin-Watson test.
        """
        pass