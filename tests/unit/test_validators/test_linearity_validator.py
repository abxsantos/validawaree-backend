from unittest.mock import call

import pytest

from analytical_validation.exceptions import AnalyticalValueNotNumber, ConcentrationValueNotNumber, \
    AnalyticalValueNegative, ConcentrationValueNegative, DataNotList, DataWasNotFitted
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


# @pytest.fixture(scope='function')
# def fitted_result_obj(mocker):
#     mock = mocker.Mock()
#     mock.return_value = "Something"
#     return mock


@pytest.fixture(scope='function')
def linearity_validator_obj():
    analytical_data = [0.100, 0.200, 0.150]
    concentration_data = [0.1, 0.2, 0.3]
    return LinearityValidator(analytical_data, concentration_data)


@pytest.fixture(scope='function')
def het_breuschpagan_mock(mocker):
    het_breuschpagan_mock = mocker.patch('analytical_validation.validators.linearity_validator.'
                                         'statsmodelsapi.het_breuschpagan')
    het_breuschpagan_mock.return_value = (33, 42)
    return het_breuschpagan_mock


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

    def test_slope_property_exists_when_fitted_result_not_none(self, linearity_validator_obj):
        # Arrange
        linearity_validator_obj.fitted_result = FittedResult()
        # Act & assert
        assert linearity_validator_obj.slope is not None

    def test_intercept_property_exists_when_fitted_result_not_none(self, linearity_validator_obj):
        # Arrange
        linearity_validator_obj.fitted_result = FittedResult()
        # Act & assert
        assert linearity_validator_obj.intercept is not None

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
    def test_significant_slope_must_return_true_when_slope_pvalue_is_smaller_than_alpha(self,
                                                                                        param_significant_slope,
                                                                                        param_alpha, expected_result):
        """Given homokedastic data
        When check_hypothesis is called
        Then slope_is_significant must assert true"""
        linearity_validator_obj.fitted_result = FittedResult()
        linearity_validator_obj.fitted_result.pvalues = ("mock value", param_significant_slope)
        # Act & Assert
        assert (linearity_validator_obj.fitted_result.pvalues[1] < param_alpha) is expected_result

    @pytest.mark.parametrize('param_insignificant_intercept, param_alpha, expected_result', [
        (0.051, 0.05, True), (10, 0.1, True), (0.049, 0.05, False), (0.001, 0.10, False)
    ])
    def test_insignificant_intercept_must_return_true_when_intercept_pvalue_is_greater_than_alpha(self,
                                                                                                  param_alpha,
                                                                                                  param_insignificant_intercept,
                                                                                                  expected_result):
        """Given homokedastic data
        When check_hypothesis is called
        Then intercept_not_significant must assert true"""
        # Arrange
        linearity_validator_obj.fitted_result = FittedResult()
        linearity_validator_obj.fitted_result.pvalues = (param_insignificant_intercept, "mock value")
        # Act & Assert
        assert (linearity_validator_obj.fitted_result.pvalues[0] > param_alpha) is expected_result

    @pytest.mark.parametrize('r_squared, expected_result', [
        (1, True), (0.99, True), (0.98, False)
    ])
    def test_valid_r_squared_must_return_true_when_r_squared_is_greater_than_0990(self,
                                                                                  linearity_validator_obj,
                                                                                  r_squared, expected_result):
        """Given homokedastic data
        When check_hypothesis is called
        Then r_squared > 0.990 must assert true"""
        # Arrange
        linearity_validator_obj.fitted_result = FittedResult()
        linearity_validator_obj.fitted_result.rsquared = r_squared
        # Act & Assert
        assert linearity_validator_obj.valid_r_squared is expected_result

    # TODO: create tests for property valid_regression_model
    @pytest.mark.parametrize(
        'param_significant_slope, param_insignificant_intercept, param_valid_r_squared, expected_result', [
            (True, True, True, True), (True, False, False, False), (True, True, False, False),
            (False, False, False, False)
        ])
    def test_valid_regression_model(self, linearity_validator_obj, param_significant_slope,
                                    param_insignificant_intercept, param_valid_r_squared, expected_result):
        # Arrange
        linearity_validator_obj.fitted_result = FittedResult()
        # Act & assert
        linearity_validator_obj.significant_slope = param_significant_slope
        linearity_validator_obj.insignificant_intercept = param_insignificant_intercept
        linearity_validator_obj.valid_r_squared = param_valid_r_squared
        # Act & Assert
        assert linearity_validator_obj.valid_regression_model is expected_result

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
        # Arrange
        linearity_validator_obj.fitted_result = FittedResult()
        # Act
        linearity_validator_obj.run_breusch_pagan_test()
        # Assert
        assert linearity_validator_obj.breusch_pagan_pvalue == 42
        assert het_breuschpagan_mock.called
        assert het_breuschpagan_mock.call_args_list == [
            call(linearity_validator_obj.fitted_result.resid, linearity_validator_obj.fitted_result.model.exog)
        ]

    # def test_check_outliers_must_pass_when_removed_outliers_is_true(self):
    #     """Given data,
    #     when check_outliers is called a second time
    #     should pass
    #     """
    #     # Arrange
    #     analytical_data = [0.100, 0.200, 0.300]
    #     concentration_data = [1, 2, 3]
    #     with pytest.raises(AlreadyCleanedOutliers):
    #         model = LinearityValidator(analytical_data, concentration_data)
    #         model.check_outliers()
    #         # Act
    #         model.check_outliers()
    #     # Assert
    #     assert AlreadyCleanedOutliers()
    #
    # def test_check_outliers_must_pass_when_given_a_list_without_outliers(self):
    #     """Given data with no outliers
    #     when check_outliers is called
    #     should pass
    #     """
    #     # Arrange
    #     analytical_data = [0.100, 0.100, 0.100]
    #     concentration_data = [1, 2, 3]
    #     model = LinearityValidator(analytical_data, concentration_data)
    #     # Act
    #     model.check_outliers()
    #     # Assert
    #     assert model.has_outliers is False
    #
    # def test_check_outliers_must_create_an_empty_list_of_outliers_when_no_outliers_found(self):
    #     """Given data with no outliers
    #     when check_outlier is called
    #     Should create a empty list"""
    #     # Arrange
    #     analytical_data = [0.100, 0.200, 0.150, 0.200, 0.150]
    #     concentration_data = [1, 2, 3, 4, 5]
    #     model = LinearityValidator(analytical_data, concentration_data)
    #     model.check_outliers()
    #     # Act
    #     model.check_outliers()
    #     # Assert
    #     assert model.outliers == []
    #
    # def test_check_outliers_must_create_a_list_of_outliers_when_outliers_found(self):
    #     """Given data with no outliers
    #     when check_outlier is called
    #     Should create a empty list"""
    #     # Arrange
    #     analytical_data = [0.100, 2.0, 0.150, 0.200, 0.150]
    #     concentration_data = [1, 2, 3, 4, 5]
    #     model = LinearityValidator(analytical_data, concentration_data)
    #     # Act
    #     model.check_outliers()
    #     # Assert
    #     assert model.outliers == [2.0]
    #
    # def test_check_outliers_must_create_a_list_of_cleaned_data_when_given_data_with_outliers(self):
    #     # Arrange
    #     analytical_data = [0.100, 2.0, 0.150, 0.100, 0.150]
    #     concentration_data = [1, 2, 3, 4, 5]
    #     model = LinearityValidator(analytical_data, concentration_data)
    #     # Act
    #     model.check_outliers()
    #     # Assert
    #     assert model.cleaned_data == [0.100, 0.150, 0.100, 0.150]
    #
    # def test_check_outliers_must_create_a_list_of_cleaned_concentration_when_given_data_with_outliers(self):
    #     """Given a data with outliers
    #     When check_outliers is called
    #     Should also remove the corresponding
    #     concentration point"""
    #     # Arrange
    #     analytical_data = [0.100, 2.0, 0.150, 0.100, 0.150]
    #     concentration_data = [1, 2, 3, 4, 5]
    #     model = LinearityValidator(analytical_data, concentration_data)
    #     # Act
    #     model.check_outliers()
    #     # Assert
    #     assert model.cleaned_concentration == [1, 3, 4, 5]
    #
    # def test_check_outliers_must_raise_exception_when_more_than_nminus1_point_removed_from_set(self):
    #     """Given data with outliers n-2 outliers
    # '   where n is the number of points in a set
    #     When check_outliers is called
    #     Should raise a execption"""
    #     # Arrange
    #     analytical_data = [0.100, 2.0, 0.100, 50.0, 20.0]
    #     concentration_data = [1, 2, 3, 4, 5]
    #     with pytest.raises(DataNotConsistent):
    #         model = LinearityValidator(analytical_data, concentration_data)
    #     # Act
    #         model.check_outliers()
    #     # Assert
    #     assert DataNotConsistent()

    @pytest.mark.parametrize('durbin_watson_pvalue', [
        0, 1, 2, 2.5, 3, 4
    ])
    def test_check_residual_autocorrelation(self, linearity_validator_obj, durbin_watson_mock,
                                            durbin_watson_pvalue):
        """Given data
        When residual_autocorrelation is called
        Then must create durbin_watson_value"""
        # Arrange
        durbin_watson_mock.return_value = durbin_watson_pvalue
        linearity_validator_obj.fitted_result = FittedResult()
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
        -1, 'str', 10, 4.1
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
        linearity_validator_obj.fitted_result = FittedResult()
        with pytest.raises(Exception):
            # Act
            linearity_validator_obj.check_residual_autocorrelation()
        # Assert
        assert linearity_validator_obj.durbin_watson_value is None
