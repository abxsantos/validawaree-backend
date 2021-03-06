from copy import deepcopy

import scipy.stats
import statsmodels.api as statsmodels
import statsmodels.stats.api as statsmodelsapi
import statsmodels.stats.stattools as stattools

from analytical_validation.exceptions import DataWasNotFitted
from analytical_validation.statistical_tests.dixon_qtest import DixonQTest


class LinearityValidator(object):
    """

    Example:
        >>> analytical_data = [[0.1,0.2,0.1],[0.3,0.3,0.32],[0.41,0.43,0.45],[0.51,0.53,0.55]]
        >>> concentration_data = [[0.01,0.02,0.01],[0.03,0.03,0.032],[0.041,0.043,0.045],[0.051,0.053,0.055]]

        >>> linearity_validator = LinearityValidator(analytical_data, concentration_data)

        >>> outliers, cleaned_analytical_data, cleaned_concentration_data, linearity_is_valid = linearity_validator.validate_linearity
        >>> linearity_validator.durbin_watson_value
        >>> linearity_validator.anova_f_value
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
        """
        self.original_analytical_data = analytical_data
        self.original_concentration_data = concentration_data
        # Flattened data
        self.analytical_data = [x for y in analytical_data for x in y]
        self.concentration_data = [x for y in concentration_data for x in y]
        self.alpha = alpha
        # Ordinary least squares linear regression coefficients
        self.fitted_result = None
        # Anova parameters
        self.has_required_parameters = False
        # Durbin Watson parameters
        self.durbin_watson_value = None
        self.shapiro_pvalue = None
        self.breusch_pagan_pvalue = None
        self.linearity_is_valid = False
        self.outliers = []
        self.cleaned_analytical_data = []
        self.cleaned_concentration_data = []

    def ordinary_least_squares_linear_regression(self):
        """Fit the data using the Ordinary Least Squares method of Linear Regression."""
        concentration_data = statsmodels.add_constant(self.concentration_data)
        model = statsmodels.OLS(self.analytical_data, concentration_data)
        self.fitted_result = model.fit()

    # Regression coefficients
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
    def significant_slope(self):
        """The slope significance avaliation.

        If the (p-value) < alpha, the slope is significant.

        :return: The avaliation of slope siginificance.
        :rtype: bool
        """
        if self.fitted_result.pvalues[1] < self.alpha:
            return True
        else:
            return False

    @property
    def insignificant_intercept(self):
        """The slope significance avaliation.

        If the (p-value) > alpha, the intercept is insignificant.

        :return: The avaliation of intercept insiginificance.
        :rtype: bool
        """
        if self.fitted_result.pvalues[0] > self.alpha:
            return True
        else:
            return False

    @property
    def valid_r_squared(self):
        """The slope significance avaliation.

        If the r squared > 0.990, the correlation coefficient is valid.

        :return: The avaliation of correlation coefficient.
        :rtype: bool
        """
        if self.fitted_result.rsquared >= 0.990:
            return True
        else:
            return False

    @property
    def valid_regression_model(self):
        """The slope significance avaliation.

        If the r squared > 0.990, slope is significant and intercept is
        insignificant,regression model is valid.

        :return valid_regression_model: The validity of regression model.
        :rtype valid_regression_model: bool
        """
        if self.significant_slope and self.insignificant_intercept and self.valid_r_squared:
            return True
        else:
            return False

    @property
    def regression_residues(self):
        """Residues of the regression
        :return regression_residues: List containing the residues of the model
        :rtype regression_residues: list
        """
        return self.fitted_result.resid.tolist()

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

    # Outlier check
    def check_outliers(self):
        """Check for outliers in the data set
        using the Dixon Q value test.
        :return outliers: List containing all the outliers.
        :rtype outliers: list[list[float]]]
        :return cleaned_analytical_data: List containing the analytical data without outliers.
        :rtype outliers: list[list[float]]]
        :return cleaned_concentration_data: List containing the concentration data without
        corresponding analytical data outliers.
        :rtype outliers: list[list[float]]]
        """
        data = deepcopy(self.original_analytical_data)
        concentration = deepcopy(self.original_concentration_data)
        for data_set in data:
            outliers_set, cleaned_data_set = DixonQTest(data_set).check_data_for_outliers()
            self.outliers.append(outliers_set)
            self.cleaned_analytical_data.append(cleaned_data_set)

        for index in range(len(data)):
            try:
                concentration[index].pop(self.original_analytical_data[index].index(self.outliers[index][0]))
            except:
                pass
            index += 1
            self.cleaned_concentration_data = concentration

    def run_shapiro_wilk_test(self):
        self.shapiro_pvalue = (scipy.stats.shapiro(self.analytical_data))[1]

    @property
    def is_normal_distribution(self):
        """check for normality in data set using the Shapiro-Wilk test.
        :return: True if data has a normal distribution, False otherwise.
        :rtype: bool"""
        return self.shapiro_pvalue > self.alpha

    # Heterokedasticity test
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

    @property
    def is_homoscedastic(self):
        """The homokedastic data information.

        The data is homokedastic when the variance is constant; otherwise it is heterokedastic.
        Uses the Breusch-Pagan test. In the Breusch-Pagan test to check homoskedasticity the p value of fitted
        results basaed on regression model is needed.
        If the (p-value) > 0.05, the method is homoskedastic, else is heteroskedastic

        :return: The homokedastic data information.
        :rtype: bool
        """
        return self.breusch_pagan_pvalue > self.alpha

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
        self.durbin_watson_value = stattools.durbin_watson(self.fitted_result.resid)

    @property
    def positive_correlation(self):
        if 0 < self.durbin_watson_value < 4:
            return self.positive_correlation is True

    def validate_linearity(self):
        """Validate the linearity of given data.
        :return outliers: List containing all the outliers.
        :rtype outliers: list[list[float]]]
        :return cleaned_analytical_data: List containing the analytical data without outliers.
        :rtype outliers: list[list[float]]]
        :return cleaned_concentration_data: List containing the concentration data without
        corresponding analytical data outliers.
        :rtype outliers: list[list[float]]]
        :return linearity_is_valid: True if data is linear; otherwise, False.
        :rtype: bool
        :raises DataWasNotFitted():
        :raises DurbinWatsonValueError() :
        """
        try:
            self.ordinary_least_squares_linear_regression()
            self.run_shapiro_wilk_test()
            self.run_breusch_pagan_test()
            self.check_residual_autocorrelation()
            self.check_outliers()
            if self.valid_regression_model and self.is_homoscedastic and self.is_normal_distribution \
                    and self.positive_correlation:
                self.linearity_is_valid = True
        except:
            return self.linearity_is_valid
