import statsmodels.api as statsmodels
import statsmodels.stats.api as stats
import numpy

from analytical_validation.exceptions import AnalyticalValueNotNumber, ConcentrationValueNotNumber, \
    AnalyticalValueNegative, ConcentrationValueNegative


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
    def __init__(self, analytical_data, concentration_data, alpha=0.5):
        """
        Validate the linearity of the method.
        :param analytical_data: List containing all measured analytical signal.
        :type analytical_data: list
        :param concentration_data: List containing the concentration for each analytical signal
        :type concentration_data: list
        :param alpha: Significance (default value = 0.5)
        :type alpha: float
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

    def validate(self):
        """Validate the given data.

        :return: True if data is valid; otherwise, False.
        :rtype: bool
        """
        pass

    def ordinary_least_squares_linear_regression(self):
        """Fit the data using the ordinary least squares method of Linear Regression.

        :raises ValueNotNumber: When a value in analytical data isn't a float.
        """
        # Check for values != float
        if not all(isinstance(value, float) for value in self.analytical_data):
            raise AnalyticalValueNotNumber()
        if not all(isinstance(value, float) for value in self.concentration_data):
            raise ConcentrationValueNotNumber()
        if not all(value > 0 for value in self.analytical_data):
            raise  ()
        if not all(value > 0 for value in self.concentration_data):
            raise ConcentrationValueNegative()
        # Create the model and fit the result
        concentration_data = statsmodels.add_constant(self.concentration_data)
        model = statsmodels.OLS(self.analytical_data, concentration_data)
        fitted_result = model.fit()
        # Retrieve hypothesis parameters
        self.intercept_pvalue ,self.slope_pvalue  = fitted_result.pvalues
        self.r_squared = fitted_result.rsquared
        self.fitted_result = fitted_result
        # Retrieve coefficients
        self.intercept, self.slope = fitted_result.params
        self.stderr = fitted_result.bse[1]

    def check_homokedasticity(self):
        """Check if the given data is homokedastic (the variance is constant) or
        heterokedastic (the variance is not constant), using the Breusch-Pagan test.

        In the Breusch-Pagan test to check homoskedasticity the p value of fitted results basaed on regression model
        is needed. If the (p-value) > 0.05, the method is homoskedastic, else is heteroskedastic
        """
        if self.fitted_result is None:
            raise Exception("There is not a regression model to check the homokedasticity.")
        try:
            # Calculate the residues based on fitted model of linear regression
            breusch_pagan_test = stats.het_breuschpagan(self.fitted_result.resid, self.fitted_result.model.exog)

            # labels = ["LM Statistic", "LM-Test p-value", "F-Statistic", "F-Test p-value"]
            self.breusch_pagan_pvalue = float(breusch_pagan_test[3])

            # TODO: Deal with heteroskedastic, removing outliers or using Weighted Least Squares Regression
            # Run the Breusch-Pagan test to check homoskedasticity
            # If the (p-value) > 0.05, the method is homoskedastic, else is heteroskedastic
            # Check Heteroskedasticity
            if self.breusch_pagan_pvalue < self.alpha:
                self.is_homokedastic = True
        except:
            raise Exception("Something went wrong.")

    def anova_analysis(self):
        """Determine the influence of independent variables (concentration) have on the dependant variables
        (analytical signal) in a regression study.

       The results of anova analysis consists of:
       Sum of squares between groups (SSB) which is the sum of the squared differences between each
                                treatment (or group) mean and the overall mean.
       Sum of squares within groups (SSE) which is the sum of the squared differences between each individual
                                value and its group mean.
       Total sum of squared errors (SST) which is is the variability of the data

       Treatment degrees of freedom (dfb) number of samples (k) - 1

       Error degrees of freedom (dfe) n (number of data points) - k

       Total degrees of freedom (dft) n -1

        Mean squares between treatments (MSB) which is the SSB / dfb

        Mean squares of residues (MSE) which is the SSE / dfe

        F-ratio which is the statistic which measures if the means of
        different samples are significantly different or not.
        If F-ratio > Fcrit, the null hyphothesis is rejected and the assumption
        of one of samples has statistically different mean can be accepted.
        """
        # X
        concentration_data = numpy.array(self.concentration_data)[:, numpy.newaxis]
        # y
        analytical_data = numpy.array(self.analytical_data)[:, numpy.newaxis]

    def check_outliers(self):
        """Check for outliers in the data set using the Dixon Q value test."""
        pass

    def check_residual_autocorrelation(self):
        """Check the residual autocorrelation in a regression analysis using the Durbin-Watson test.
        """
        pass