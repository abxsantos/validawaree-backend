from unittest.mock import call, PropertyMock, MagicMock

import pytest

from analytical_validation.exceptions import AnalyticalValueNotNumber, ConcentrationValueNotNumber, \
    AnalyticalValueNegative, ConcentrationValueNegative, DataNotList, DataWasNotFitted, DurbinWatsonValueError
from src.analytical_validation.validators.linearity_validator import LinearityValidator


# TODO: use mocker.Mock instead
class FittedResultModel(object):
    def __init__(self):
        self.exog = 10.0


# TODO: use mocker.Mock instead
class FittedResult(object):
    def __init__(self):
        self.params = (1.0, 2.0)
        self.pvalues = (4.0, 5.0)
        self.rsquared = 6.0
        self.resid = 7.0
        # self.significant_slope = True
        # self.insignificant_intercept = True
        # self.valid_r_squared = True
        # self.valid_regression_model = True
        self.model = FittedResultModel()


@pytest.fixture(scope='function')
def fitted_result_obj(mocker):
    mock = mocker.Mock(create=True)
    mock.params = (mocker.Mock(), mocker.Mock())
    mock.pvalues = (mocker.Mock(), mocker.Mock())
    mock.ess = MagicMock()
    mock.ssr = MagicMock()
    mock.df_model = MagicMock()
    mock.df_resid = MagicMock()
    return mock


@pytest.fixture(scope='function')
def linearity_validator_obj(fitted_result_obj):
    analytical_data = [0.100, 0.200, 0.150]
    concentration_data = [0.1, 0.2, 0.3]
    linearity_validator = LinearityValidator(analytical_data, concentration_data)
    linearity_validator.fitted_result = fitted_result_obj
    return linearity_validator


@pytest.fixture(scope='function')
def het_breuschpagan_mock(mocker):
    het_breuschpagan_mock = mocker.patch('analytical_validation.validators.linearity_validator.'
                                         'statsmodelsapi.het_breuschpagan')
    het_breuschpagan_mock.return_value = (33, 42)
    return het_breuschpagan_mock


@pytest.fixture(scope='function')
def shapiro_mock(mocker, linearity_validator_obj):
    shapiro_mock = mocker.patch('analytical_validation.validators.linearity_validator.scipy.stats')
    shapiro_mock.shapiro(linearity_validator_obj.analytical_data).return_value = (0, 1)
    return shapiro_mock


@pytest.fixture(scope='function')
def durbin_watson_mock(mocker):
    durbin_watson_mock = mocker.patch('analytical_validation.validators.linearity_validator.stattools.durbin_watson')
    durbin_watson_mock.return_value = 1
    return durbin_watson_mock


@pytest.fixture(scope='function')
def add_constant_mock(mocker):
    add_constant_mock = mocker.patch(
        'analytical_validation.validators.linearity_validator.statsmodels.add_constant')  # Quando chamar, este modulo sera usado ao inves do original
    return add_constant_mock


@pytest.fixture(scope='function')
def ordinary_least_squares_regression_mock(mocker):
    ordinary_least_squares_regression_mock = mocker.patch(
        'analytical_validation.validators.linearity_validator.statsmodels.OLS')  # Quando chamar, este modulo sera usado ao inves do original
    return ordinary_least_squares_regression_mock


class TestLinearityValidator(object):

    def test_constructor_raise_exception_when_analytical_data_is_not_list(self):
        """Given analytical data that is not a list
        When LinearityValidator constructor is called
        Then must raise exception
        """
        # Arrange
        analytical_data = {0.100: 'abc', 0.200: 'def', 0.150: 'fgh'}
        concentration_data = [0.1, 0.2, 0.3]
        # Act & Assert
        with pytest.raises(DataNotList):
            LinearityValidator(analytical_data, concentration_data)

    def test_constructor_raise_exception_when_concentration_data_is_not_list(self):
        """Given concentration data that is not a list
        When LinearityValidator constructor is called
        Then must raise exception
        """
        # Arrange
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = {0.1: 'abc', 0.2: 'def', 0.3: 'fgh'}
        # Act & Assert
        with pytest.raises(DataNotList):
            LinearityValidator(analytical_data, concentration_data)

    def test_constructor_must_create_object_when_analytical_data_has_float_values(self, linearity_validator_obj):
        """Given analytical data
        The LinearityValidator
        Should create a list of floats
        """
        # Assert
        assert linearity_validator_obj.analytical_data == [0.100, 0.200, 0.150]
        assert linearity_validator_obj.concentration_data == [0.1, 0.2, 0.3]

    def test_constructor_must_raise_exception_when_concentration_not_float(self):
        """Given concentration values != float
        The ordinary_least_squares_linear_regression
        Should raise exception"""
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = ["STRING", 0.2, 0.3]
        # Act
        with pytest.raises(ConcentrationValueNotNumber) as excinfo:
            LinearityValidator(analytical_data, concentration_data)
        # Assert
        assert "One of the concentration values is not a number!" in str(excinfo.value)

    def test_constructor_must_raise_exception_when_concentration_negative(self):
        """Given negative concentration values
        The ordinary_least_squares_linear_regression
        Should raise exception"""

        # Arrange
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = [-0.2, 0.2, 0.3]
        # Act
        with pytest.raises(ConcentrationValueNegative) as excinfo:
            LinearityValidator(analytical_data, concentration_data)
        # Assert
        assert "Negative value for concentration value is not valid!" in str(excinfo.value)

    def test_constructor_must_raise_exception_when_analytical_data_not_float(self):
        """Given analytical values != float
        The ordinary_least_squares_linear_regression
        Should raise exception"""

        # Arrange
        analytical_data = ["STRING", 0.200, 0.150]
        concentration_data = [0.2, 0.2, 0.3]
        # Act
        with pytest.raises(AnalyticalValueNotNumber) as excinfo:
            LinearityValidator(analytical_data, concentration_data)
        # Assert
        assert "One of the analytical values is not a number!" in str(excinfo.value)

    def test_constructor_must_raise_exception_when_analytical_data_negative(self):
        """Given negative values
        When I call ordinary_least_squares_linear_regression
        Then it must raise exception"""

        # Arrange
        analytical_data = [-0.100, 0.200, 0.150]
        concentration_data = [0.2, 0.2, 0.3]
        # Act
        with pytest.raises(AnalyticalValueNegative) as excinfo:
            LinearityValidator(analytical_data, concentration_data)
        # Assert
        assert "Negative value for analytical signal is not valid!" in str(excinfo.value)

    def test_ordinary_least_squares_linear_regression_must_pass_float_when_given_correct_data(self,
                                                                                              ordinary_least_squares_regression_mock,
                                                                                              add_constant_mock,
                                                                                              linearity_validator_obj):
        """Given concentration values = float
        The ordinary_least_squares_linear_regression
        Then must set properties"""
        # Act
        linearity_validator_obj.ordinary_least_squares_linear_regression()
        # Assert
        assert linearity_validator_obj.fitted_result == ordinary_least_squares_regression_mock.return_value.fit.return_value  # Garante que a regressao e resultado do resultado do metodo statsmodels.OLS(), aplicado .fit().
        assert ordinary_least_squares_regression_mock.called  # Garante que o metodo ols esta sendo chamado
        assert ordinary_least_squares_regression_mock.call_args_list == [
            call(linearity_validator_obj.analytical_data, add_constant_mock.return_value)
            # Garante que os arquivos de entrada definidos no call foram utilizados
        ]
        assert add_constant_mock.called
        assert add_constant_mock.call_args_list == [
            call(linearity_validator_obj.concentration_data)
        ]

    def test_slope_property_exists_when_fitted_result_not_none(self, linearity_validator_obj, fitted_result_obj):
        # Act & assert
        assert linearity_validator_obj.slope is not None
        assert linearity_validator_obj.slope == fitted_result_obj.params[1]

    def test_intercept_property_exists_when_fitted_result_not_none(self, linearity_validator_obj, fitted_result_obj):
        # Act & assert
        assert linearity_validator_obj.intercept is not None
        assert linearity_validator_obj.intercept == fitted_result_obj.params[0]

    def test_r_squared_adjusted_property_exists_when_fitted_result_not_none(self, linearity_validator_obj,
                                                                            fitted_result_obj):
        # Act & assert
        assert linearity_validator_obj.r_squared_adj is not None
        assert linearity_validator_obj.r_squared_adj == fitted_result_obj.rsquared_adj

    def test_r_squared_property_exists_when_fitted_result_not_none(self, linearity_validator_obj, fitted_result_obj):
        # Act & assert
        assert linearity_validator_obj.r_squared is not None
        assert linearity_validator_obj.r_squared == fitted_result_obj.rsquared

    def test_sum_of_squares_model_property_exists_when_fitted_result_not_none(self, linearity_validator_obj,
                                                                              fitted_result_obj):
        # Act & assert
        assert linearity_validator_obj.sum_of_squares_model is not None
        assert linearity_validator_obj.sum_of_squares_model == fitted_result_obj.ess

    def test_sum_of_squares_total_property_exists_when_fitted_result_not_none(self, linearity_validator_obj,
                                                                              fitted_result_obj):
        # Act & assert
        assert linearity_validator_obj.sum_of_squares_total is not None
        assert linearity_validator_obj.sum_of_squares_total == fitted_result_obj.ess + fitted_result_obj.ssr

    def test_sum_of_squares_resid_property_exists_when_fitted_result_not_none(self, linearity_validator_obj,
                                                                              fitted_result_obj):
        # Act & assert
        assert linearity_validator_obj.sum_of_squares_resid is not None
        assert linearity_validator_obj.sum_of_squares_resid == fitted_result_obj.ssr

    def test_degrees_of_freedom_model_property_exists_when_fitted_result_not_none(self, linearity_validator_obj,
                                                                                  fitted_result_obj):
        # Act & assert
        assert linearity_validator_obj.degrees_of_freedom_model is not None
        assert linearity_validator_obj.degrees_of_freedom_model == fitted_result_obj.df_model

    def test_degrees_of_freedom_residues_property_exists_when_fitted_result_not_none(self, linearity_validator_obj,
                                                                                     fitted_result_obj):
        # Act & assert
        assert linearity_validator_obj.degrees_of_freedom_residues is not None
        assert linearity_validator_obj.degrees_of_freedom_residues == fitted_result_obj.df_resid

    def test_degrees_of_freedom_total_property_exists_when_fitted_result_not_none(self, linearity_validator_obj,
                                                                                  fitted_result_obj):
        # Act & assert
        assert linearity_validator_obj.degrees_of_freedom_total is not None
        assert linearity_validator_obj.degrees_of_freedom_total == fitted_result_obj.df_model + fitted_result_obj.df_resid

    def test_mean_squared_error_model_property_exists_when_fitted_result_not_none(self, linearity_validator_obj,
                                                                                  fitted_result_obj):
        # Act & assert
        assert linearity_validator_obj.mean_squared_error_model is not None
        assert linearity_validator_obj.mean_squared_error_model == fitted_result_obj.mse_model

    def test_mean_squared_error_residues_property_exists_when_fitted_result_not_none(self, linearity_validator_obj,
                                                                                     fitted_result_obj):
        # Act & assert
        assert linearity_validator_obj.mean_squared_error_residues is not None
        assert linearity_validator_obj.mean_squared_error_residues == fitted_result_obj.mse_resid

    def test_anova_f_value_property_exists_when_fitted_result_not_none(self, linearity_validator_obj,
                                                                       fitted_result_obj):
        # Act & assert
        assert linearity_validator_obj.anova_f_value is not None
        assert linearity_validator_obj.anova_f_value == fitted_result_obj.fvalue

    def test_anova_f_pvalue_property_exists_when_fitted_result_not_none(self, linearity_validator_obj,
                                                                        fitted_result_obj):
        # Act & assert
        assert linearity_validator_obj.anova_f_pvalue is not None
        assert linearity_validator_obj.anova_f_pvalue == fitted_result_obj.f_pvalue

    @pytest.mark.parametrize('param_anova_f_pvalue, param_alpha, expected_result', [
        (0.051, 0.05, False), (10, 0.1, False), (0.049, 0.05, True), (0.001, 0.10, True)
    ])
    def test_valid_anova_f_pvalue_must_return_true_when_r_squared_is_greater_than_0990(self, param_alpha,
                                                                                       linearity_validator_obj,
                                                                                       param_anova_f_pvalue,
                                                                                       expected_result):
        """Given data with an aceptable regression model
        When valid_anova_f_pvalue is called
        Then anova_f_pvalue < alpha must assert true"""
        # Arrange
        linearity_validator_obj.alpha = param_alpha
        linearity_validator_obj.fitted_result.f_pvalue = param_anova_f_pvalue
        # Act & Assert
        assert linearity_validator_obj.valid_anova_f_pvalue is expected_result

    @pytest.mark.parametrize('param_alpha, param_breusch_pagan_pvalue, expected_result', [
        (1, -10, False), (0.05, 0.049, False), (0.10, 0.11, True), (0.05, 10, True)
    ])
    def test_is_homokedastic_must_return_false_when_breusch_pagan_pvalue_is_smaller_than_alpha_otherwise_true(self,
                                                                                                              param_alpha,
                                                                                                              param_breusch_pagan_pvalue,
                                                                                                              expected_result):
        # Arrange
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = [0.1, 0.2, 0.3]
        linearity_validator = LinearityValidator(analytical_data, concentration_data, param_alpha)
        linearity_validator.breusch_pagan_pvalue = param_breusch_pagan_pvalue
        # Act & Assert
        assert linearity_validator.is_homokedastic is expected_result

    @pytest.mark.parametrize('param_significant_slope, param_alpha, expected_result', [
        (0.051, 0.05, False), (10, 0.1, False), (0.049, 0.05, True), (0.001, 0.10, True)
    ])
    def test_significant_slope_must_return_true_when_slope_pvalue_is_smaller_than_alpha(self, linearity_validator_obj,
                                                                                        param_significant_slope,
                                                                                        param_alpha, expected_result):
        """Given homokedastic data
        When check_hypothesis is called
        Then slope_is_significant must assert true"""
        # Arrange
        linearity_validator_obj.alpha = param_alpha
        linearity_validator_obj.fitted_result.pvalues = ("mock value", param_significant_slope)
        # Act & Assert
        assert linearity_validator_obj.significant_slope is expected_result

    @pytest.mark.parametrize('param_insignificant_intercept, param_alpha, expected_result', [
        (0.051, 0.05, True), (10, 0.1, True), (0.049, 0.05, False), (0.001, 0.10, False)
    ])
    def test_insignificant_intercept_must_return_true_when_intercept_pvalue_is_greater_than_alpha(self,
                                                                                                  linearity_validator_obj,
                                                                                                  param_alpha,
                                                                                                  param_insignificant_intercept,
                                                                                                  expected_result):
        """Given homokedastic data
        When check_hypothesis is called
        Then intercept_not_significant must assert true"""
        # Arrange
        linearity_validator_obj.alpha = param_alpha
        linearity_validator_obj.fitted_result.pvalues = (param_insignificant_intercept, "mock value")
        # Act & Assert
        assert linearity_validator_obj.insignificant_intercept is expected_result

    @pytest.mark.parametrize('param_r_squared, expected_result', [
        (1, True), (0.99, True), (0.98, False)
    ])
    def test_valid_r_squared_must_return_true_when_r_squared_is_greater_than_0990(self,
                                                                                  linearity_validator_obj,
                                                                                  param_r_squared, expected_result):
        """Given homokedastic data
        When check_hypothesis is called
        Then r_squared > 0.990 must assert true"""
        # Arrange
        linearity_validator_obj.fitted_result.rsquared = param_r_squared
        # Act & Assert
        assert linearity_validator_obj.valid_r_squared is expected_result

    @pytest.mark.parametrize(
        'param_significant_slope, param_insignificant_intercept, param_valid_r_squared, expected_result', [
            (True, True, True, True), (True, False, False, False), (True, True, False, False),
            (False, False, False, False)
        ])
    def test_valid_regression_model(self, mocker, param_significant_slope, param_insignificant_intercept,
                                    param_valid_r_squared, expected_result):
        # Arrange
        mocker.patch('unit.test_validators.test_linearity_validator.LinearityValidator.significant_slope',
                     new_callable=PropertyMock, return_value=param_significant_slope)
        mocker.patch('unit.test_validators.test_linearity_validator.LinearityValidator.insignificant_intercept',
                     new_callable=PropertyMock, return_value=param_insignificant_intercept)
        mocker.patch('unit.test_validators.test_linearity_validator.LinearityValidator.valid_r_squared',
                     new_callable=PropertyMock, return_value=param_valid_r_squared)
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = [0.2, 0.2, 0.3]
        linearity_validator = LinearityValidator(analytical_data, concentration_data)
        # Act & Assert
        assert linearity_validator.valid_regression_model is expected_result

    def test_check_outliers_when_given_list_of_list_data(self):
        outliers, cleaned_data, cleaned_concentration_data = LinearityValidator.check_outliers(self)
        assert outliers == [101]
        assert cleaned_data == [1,1,2,3,2,4]
        assert cleaned_concentration_data == [1,2,4,5,6,7]

    @pytest.mark.parametrize('param_shapiro_pvalue, param_alpha, expected_result', [
        (10, 0.05, True), (0.01, 0.1, False), (0.0501, 0.05, True), (0.099, 0.1, False)
    ])
    def test_is_normal_distribution(self, param_shapiro_pvalue, param_alpha, expected_result):
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = [0.2, 0.2, 0.3]
        validator = LinearityValidator(analytical_data, concentration_data, param_alpha)
        validator.shapiro_pvalue = param_shapiro_pvalue
        # Assert
        assert validator.is_normal_distribution is expected_result

    def test_run_breusch_pagan_test_must_raise_exception_when_model_is_none(self):
        """Not given a model parameter
        The check_homokedasticity
        Should raise exception"""
        # Arrange
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = [0.2, 0.2, 0.3]
        # Act & Assert
        with pytest.raises(DataWasNotFitted):
            LinearityValidator(analytical_data, concentration_data).run_breusch_pagan_test()

    def test_run_breusch_pagan_test(self, linearity_validator_obj, het_breuschpagan_mock):
        """Given heterokedastic data
        When check_homokedasticity is called
        Then must return false"""
        # Act
        linearity_validator_obj.run_breusch_pagan_test()
        # Assert
        assert linearity_validator_obj.breusch_pagan_pvalue == 42
        assert het_breuschpagan_mock.called
        assert het_breuschpagan_mock.call_args_list == [
            call(linearity_validator_obj.fitted_result.resid, linearity_validator_obj.fitted_result.model.exog)
        ]

    @pytest.mark.parametrize('durbin_watson_pvalue', [
        0.1, 1, 2, 2.5, 3, 3.9
    ])
    def test_check_residual_autocorrelation(self, linearity_validator_obj, durbin_watson_mock,
                                            durbin_watson_pvalue):
        """Given data
        When residual_autocorrelation is called
        Then must create durbin_watson_value"""
        # Arrange
        durbin_watson_mock.return_value = durbin_watson_pvalue
        # Act
        linearity_validator_obj.check_residual_autocorrelation()
        # Assert
        assert linearity_validator_obj.durbin_watson_value == durbin_watson_mock.return_value
        assert durbin_watson_mock.called
        assert durbin_watson_mock.call_args_list == [
            call(linearity_validator_obj.fitted_result.resid)
        ]

    def test_check_residual_autocorrelation_must_raise_exception_when_data_not_fitted(self, linearity_validator_obj):
        """Given data,
        if no regression was calculated
        Should raise an exception"""
        linearity_validator_obj.fitted_result = None
        with pytest.raises(DataWasNotFitted):
            # Act
            linearity_validator_obj.check_residual_autocorrelation()

    @pytest.mark.parametrize('durbin_watson_pvalue', [
        -1, 10, 4.1
    ])
    def test_check_residual_autocorrelation_must_pass_when_durbin_watson_value_is_between_0_and_4(self,
                                                                                                  linearity_validator_obj,
                                                                                                  durbin_watson_mock,
                                                                                                  durbin_watson_pvalue):
        """Given data,
        When check_residual is called
        after fitting the model
        Should pass creating
        0 < durbin_watson_value < 4"""
        # Arrange
        durbin_watson_mock.return_value = durbin_watson_pvalue
        with pytest.raises(DurbinWatsonValueError):
            # Act
            linearity_validator_obj.check_residual_autocorrelation()
        # Assert
        assert linearity_validator_obj.durbin_watson_value is None
