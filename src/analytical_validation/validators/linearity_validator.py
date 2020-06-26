import scipy.stats
import statsmodels.api as statsmodels
import statsmodels.stats.api as statsmodelsapi
import statsmodels.stats.stattools as stattools

from analytical_validation.exceptions import AnalyticalValueNotNumber, ConcentrationValueNotNumber, \
    AnalyticalValueNegative, ConcentrationValueNegative, DataNotList, \
    DataWasNotFitted, DurbinWatsonValueError
from analytical_validation.statistical_tests.dixon_qtest import dixon_qtest


class LinearityValidator(object):
    """

    Example:
        >>> l = LinearityValidator(samples=[])
        >>> l.validate()
        False
        >>> l.plot_values()
        [(1, 20), (4, 44)]

        >>> l = LinearityValidator(samples=[1, 2, 3])
        >>> l.validate()
        True
        >>> l.plot_values()
        [(1, 20), (4, 44)]
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
        self.original_analytical_data = analytical_data
        self.original_concentration_data = concentration_data
        self.alpha = alpha
        # Ordinary least squares linear regression coefficients
        self.fitted_result = None
        # Anova parameters
        self.has_required_parameters = False
        # Outliers
        self.outliers = None
        self.cleaned_data = None
        self.cleaned_concentration_data = None
        # Durbin Watson parameters
        self.durbin_watson_value = None
        self.shapiro_pvalue = None

        if isinstance(analytical_data, list) is False:
            raise DataNotList()
        if isinstance(concentration_data, list) is False:
            raise DataNotList()
        self.analytical_data = [x for y in analytical_data for x in y]
        self.concentration_data = [x for y in concentration_data for x in y]
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
        self.ordinary_least_squares_linear_regression()
        return self.intercept

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
        return self.fitted_result.params[0]

    @property
    def slope(self):
        """The slope value.

        :return: The slope value.
        :rtype: numpy.float64
        """
        return self.fitted_result.params[1]

    @property
    def r_squared(self):
        """The correlation coefficient value.

        :return: Correlation coefficient value.
        :rtype: numpy.float64
        """
        return self.fitted_result.rsquared

    @property
    def r_squared_adj(self):
        """The adjusted correlation coefficient.

        :return: Adjusted correlation coefficient value.
        :rtype: numpy.float64
        """
        return self.fitted_result.rsquared_adj

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
        return self.breusch_pagan_pvalue > self.alpha

    @property
    def significant_slope(self):
        """The slope significance avaliation.

        If the (p-value) < alpha, the slope is significant.

        :return: The avaliation of slope siginificance.
        :rtype: bool
        """
        return self.fitted_result.pvalues[1] < self.alpha

    @property
    def insignificant_intercept(self):
        """The slope significance avaliation.

        If the (p-value) > alpha, the intercept is insignificant.

        :return: The avaliation of intercept insiginificance.
        :rtype: bool
        """
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
        return self.significant_slope and self.insignificant_intercept and self.valid_r_squared

    # ANOVA table values
    @property
    def sum_of_squares_model(self):
        """Sum of squares of model
        :return: The sum of squares of each observed value and the predicted result
        :rtype: numpy.float64
        """
        return self.fitted_result.ess

    @property
    def sum_of_squares_resid(self):
        """Sum of squares of residues
        :return: The sum of squares of predicted result and the mean
        :rtype: numpy.float64
        """
        return self.fitted_result.ssr

    @property
    def sum_of_squares_total(self):
        """Total sum of squares
        :return: The total sum of squares
        :rtype: numpy.float64
        """
        return self.fitted_result.ess + self.fitted_result.ssr

    @property
    def degrees_of_freedom_model(self):
        """Degrees of freedom of the model
        :return: The Degrees of freedom of the model
        :rtype: numpy.float64
        """
        return self.fitted_result.df_model

    @property
    def degrees_of_freedom_residues(self):
        """Degrees of freedom of the residues
        :return: The Degrees of freedom of the residues
        :rtype: numpy.float64
        """
        return self.fitted_result.df_resid

    @property
    def degrees_of_freedom_total(self):
        """Total degrees of freedom
        :return: Total Degrees of freedom.
        :rtype: numpy.float64
        """
        return self.fitted_result.df_model + self.fitted_result.df_resid

    @property
    def mean_squared_error_model(self):
        """Mean squared error of the model
        :return: Mean squared error of the model
        :rtype: numpy.float64
        """
        return self.fitted_result.mse_model

    @property
    def mean_squared_error_residues(self):
        """Mean squared error of the residues
        :return: Mean squared error of residues
        :rtype: numpy.float64
        """
        return self.fitted_result.mse_resid

    @property
    def anova_f_value(self):
        """F value of model and residual means
        :return: F value
        :rtype: numpy.float64
        """
        return self.fitted_result.fvalue

    @property
    def anova_f_pvalue(self):
        """F value of model and residual means
        :return: F value
        :rtype: numpy.float64
        """
        return self.fitted_result.f_pvalue

    @property
    def valid_anova_f_pvalue(self):
        """ Validate the F p-value of regression
        :return: Regression validity based on anova
        :rtype: numpy.float64
        """
        return self.fitted_result.f_pvalue < self.alpha

    def check_outliers(self):
        """Check for outliers in the data set
        using the Dixon Q value test.
        :return: The data set list without outliers and a list of outliers.
        :rtype: list"""
        # TODO: Implement dixon qtest outlier
        """para cada lista dentro da parent list,
        rodar o teste de ouliers.
        cada teste de outliers retornará uma lista contendo os dados limpos.
        agrupar estas listas em uma lista flat."""

        data = self.original_analytical_data
        concentration = self.original_concentration_data
        self.outliers = []
        self.cleaned_data = []
        self.cleaned_concentration_data = []

        for data_set in data:
            outliers_set, cleaned_data_set = dixon_qtest(data_set)
            self.outliers.append(outliers_set)
            self.cleaned_data.append(cleaned_data_set)
        try:
            set_index = 0
            while set_index < len(data):
                outlier_index = self.original_analytical_data[set_index].index(self.outliers[set_index][0])
                concentration[set_index].pop(outlier_index)
                set_index = set_index + 1
                self.cleaned_concentration_data = concentration
        except:
            pass

        return self.outliers, self.cleaned_data, self.cleaned_concentration_data

    # TODO: create test
    @property
    def is_normal_distribution(self):
        """check for normality in data set using the Shapiro-Wilk test.
        :return: True if data has a normal distribution, False otherwise.
        :rtype: bool"""
        # TODO: check if property is needed
        return self.shapiro_pvalue > self.alpha

    def run_shapiro_wilk_test(self):
        self.shapiro_pvalue = scipy.stats.shapiro(self.analytical_data)

    def run_breusch_pagan_test(self):
        """Run the Breusch-Pagan test."""
        if self.fitted_result is None:
            raise DataWasNotFitted()
        # Calculate the residues based on fitted model of linear regression
        breusch_pagan_test = statsmodelsapi.het_breuschpagan(self.fitted_result.resid,
                                                             self.fitted_result.model.exog)
        # labels = ["LM Statistic", "LM-Test p-value", "F-Statistic", "F-Test p-value"]
        self.breusch_pagan_pvalue = float(breusch_pagan_test[1])
        # TODO: Deal with heteroskedastic, removing outliers or using Weighted Least Squares Regression

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
        if 0 < value < 4:
            self.durbin_watson_value = value
        else:
            raise DurbinWatsonValueError()
