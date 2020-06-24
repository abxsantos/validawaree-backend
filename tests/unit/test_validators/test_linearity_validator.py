import numpy
import pytest

from analytical_validation.exceptions import AnalyticalValueNotNumber, ConcentrationValueNotNumber, \
    AnalyticalValueNegative, ConcentrationValueNegative, DataNotList, AlreadyCleanedOutliers, DataNotConsistent, \
    ResiduesNone, DataWasNotFitted
from src.analytical_validation.validators.linearity_validator import LinearityValidator


class TestLinearityValidator(object):
    def test_constructor_must_return_true_when_float_analytical_data_values(self):
        """Given analytical data
        The LinearityValidator
        Should create a list of floats
        """
        # Arrange
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = [0.1, 0.2, 0.3]
        # Act
        constructor = LinearityValidator(analytical_data, concentration_data)
        assert all(isinstance(value, float) for value in constructor.analytical_data)

    def test_constructor_must_return_true_when_float_concentration_values(self):
        """Given concentration data
        The LinearityValidator
        Should create a list of floats
        """
        # Arrange
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = [0.1, 0.2, 0.3]
        # Act
        constructor = LinearityValidator(analytical_data, concentration_data)
        assert all(isinstance(value, float) for value in constructor.concentration_data)

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

    def test_ordinary_least_squares_linear_regression_must_return_float_when_concentration_float(self):
        """Given concentration values = float
        The ordinary_least_squares_linear_regression
        Should pass"""
        # Arrange
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = [0.1, 0.2, 0.3]
        # Act
        model = LinearityValidator(analytical_data, concentration_data)
        model.ordinary_least_squares_linear_regression()
        # Assert
        assert isinstance(model.intercept_pvalue, numpy.float64)
        assert isinstance(model.slope_pvalue, numpy.float64)
        assert isinstance(model.r_squared, numpy.float64)
        assert isinstance(model.intercept, numpy.float64)
        assert isinstance(model.slope, numpy.float64)
        assert isinstance(model.stderr, numpy.float64)

    def test_ordinary_least_squares_linear_regression_must_raise_exception_when_concentration_not_float(self):
        """Given concentration values != float
        The ordinary_least_squares_linear_regression
        Should raise exception"""
        # Arrange
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = ["STRING", 0.2, 0.3]
        # Act
        with pytest.raises(ConcentrationValueNotNumber) as excinfo:
            LinearityValidator(analytical_data, concentration_data).ordinary_least_squares_linear_regression()
        # Assert
        assert "One of the concentration values is not a number!" in str(excinfo.value)

    def test_ordinary_least_squares_linear_regression_must_raise_exception_when_analytical_values_not_float(self):
        """Given analytical values != float
        The ordinary_least_squares_linear_regression
        Should raise exception"""

        # Arrange
        analytical_data = ["STRING", 0.200, 0.150]
        concentration_data = [0.2, 0.2, 0.3]
        # Act
        with pytest.raises(AnalyticalValueNotNumber) as excinfo:
            LinearityValidator(analytical_data, concentration_data).ordinary_least_squares_linear_regression()
        # Assert
        assert "One of the analytical values is not a number!" in str(excinfo.value)

    def test_ordinary_least_squares_linear_regression_must_raise_exception_when_negative_concentration(self):
        """Given negative concentration values
        The ordinary_least_squares_linear_regression
        Should raise exception"""

        # Arrange
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = [-0.2, 0.2, 0.3]
        # Act
        with pytest.raises(ConcentrationValueNegative) as excinfo:
            LinearityValidator(analytical_data, concentration_data).ordinary_least_squares_linear_regression()
        # Assert
        assert "Negative value for concentration value is not valid!" in str(excinfo.value)

    def test_ordinary_least_squares_linear_regression_must_raise_exception_when_negative_analytical_values(self):
        """Given negative values
        When I call ordinary_least_squares_linear_regression
        Then it must raise exception"""

        # Arrange
        analytical_data = [-0.100, 0.200, 0.150]
        concentration_data = [0.2, 0.2, 0.3]
        # Act
        with pytest.raises(AnalyticalValueNegative) as excinfo:
            LinearityValidator(analytical_data, concentration_data).ordinary_least_squares_linear_regression()
        # Assert
        assert "Negative value for analytical signal is not valid!" in str(excinfo.value)

    def test_check_homokedasticity_must_raise_exeption_when_model_is_none(self):
        """Not given a model parameter
        The check_homokedasticity
        Should raise exception"""

        # Arrange
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = [0.2, 0.2, 0.3]
        # Act
        with pytest.raises(Exception) as excinfo:
            LinearityValidator(analytical_data, concentration_data).check_homokedasticity()
        # Assert
        assert "There is not a regression model to check the homokedasticity." in str(excinfo.value)

    def test_check_homokedasticity_must_return_false_when_data_is_heterokedastic(self):
        """Given heterokedastic data
        When check_homokedasticity is called
        Then must return false"""
        # Arrange
        analytical_data = [1.0, 1.0, 1.0, 6.0, 2.0, 4.0, 12.0, 6.0, 8.0, 30.0, 20.0, 10.0]
        concentration_data = [1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 4.0, 4.0]
        model = LinearityValidator(analytical_data, concentration_data)
        model.ordinary_least_squares_linear_regression()
        # Act
        model.check_homokedasticity()
        # Assert
        assert model.is_homokedastic == False

    def test_check_homokedasticity_must_return_true_when_data_is_homokedastic(self):
        """Given homokedastic data
        When check_homokedasticity is called
        Then must return true"""
        # Arrange
        analytical_data = [0.188, 0.192, 0.203, 0.349, 0.346, 0.348, 0.489, 0.482, 0.492, 0.637, 0.641, 0.641, 0.762,
                           0.768, 0.786, 0.931, 0.924,
                           0.925]
        concentration_data = [0.008, 0.008016, 0.008128, 0.016, 0.016032, 0.016256, 0.02, 0.02004, 0.02032,
                              0.027999996640000406, 0.028055996633280407, 0.02844799658624041, 0.032, 0.032064,
                              0.032512, 0.04, 0.04008, 0.04064]

        model = LinearityValidator(analytical_data, concentration_data)
        model.ordinary_least_squares_linear_regression()
        # Act
        model.check_homokedasticity()
        # Assert
        assert model.is_homokedastic is True


    def test_check_homokedasticity_must_raise_exception_when_analytical_data_is_negative(self):
        # Arrange
        analytical_data = [-0.188, 0.192, 0.203]
        concentration_data = [0.008, 0.008016, 0.008128]
        with pytest.raises(AnalyticalValueNegative) as excinfo:
            model = LinearityValidator(analytical_data, concentration_data)
            model.ordinary_least_squares_linear_regression()
        # Act
            model.check_homokedasticity()
        # Assert
        assert "Negative value for analytical signal is not valid!" in str(excinfo.value)

    def test_check_homokedasticity_must_raise_exception_when_analytical_values_not_float(self):
        """Given analytical values != float
        The ordinary_least_squares_linear_regression
        Should raise exception"""
        # Arrange
        analytical_data = ["STRING", 0.200, 0.150]
        concentration_data = [0.2, 0.2, 0.3]
        with pytest.raises(AnalyticalValueNotNumber) as excinfo:
            model = LinearityValidator(analytical_data, concentration_data)
            model.ordinary_least_squares_linear_regression()
        # Act
            model.check_homokedasticity()
        # Assert
        assert "One of the analytical values is not a number!" in str(excinfo.value)

    def test_check_homokedasticity_must_raise_exception_when_concentration_data_is_negative(self):
        # Arrange
        analytical_data = [0.188, 0.192, 0.203]
        concentration_data = [-0.008, 0.008016, 0.008128]
        with pytest.raises(ConcentrationValueNegative) as excinfo:
            model = LinearityValidator(analytical_data, concentration_data)
            model.ordinary_least_squares_linear_regression()
        # Act
            model.check_homokedasticity()
        # Assert
        assert "Negative value for concentration value is not valid!" in str(excinfo.value)

    def test_check_homokedasticity_must_raise_exception_when_concentration_values_not_float(self):
        """Given analytical values != float
        The ordinary_least_squares_linear_regression
        Should raise exception"""
        # Arrange
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = ["STR", 0.2, 0.3]
        with pytest.raises(ConcentrationValueNotNumber) as excinfo:
            model = LinearityValidator(analytical_data, concentration_data)
            model.ordinary_least_squares_linear_regression()
        # Act
            model.check_homokedasticity()
        # Assert
        assert "One of the concentration values is not a number!" in str(excinfo.value)

    def test_check_homokedasticity_must_raise_exception_when_analytical_data_is_not_list(self):
        """Given analytical data not as lis
        When check homokedassticity is called
        Then must raise an exception"""
        # Arrange
        analytical_data = "STRING"
        concentration_data = [0.1, 0.2, 0.3]
        with pytest.raises(DataNotList) as excinfo:
            model = LinearityValidator(analytical_data, concentration_data)
            model.ordinary_least_squares_linear_regression()
        # Act
            model.check_homokedasticity()
        # Assert
        assert "One of the input datas is not a list." in str(excinfo.value)

    def test_check_homokedasticity_must_raise_exception_when_concentration_data_is_not_list(self):
        """Given concentration data not as list
        When check homokedassticity is called
        Then must raise an exception"""
        # Arrange
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = "STRING"
        with pytest.raises(DataNotList) as excinfo:
            model = LinearityValidator(analytical_data, concentration_data)
            model.ordinary_least_squares_linear_regression()
        # Act
            model.check_homokedasticity()
        # Assert
        assert "One of the input datas is not a list." in str(excinfo.value)

    def test_check_hypothesis_must_call_ordinary_least_squares_linear_regression_when_parameters_are_none(self):
        """Given data, but not method parameters
        When check_hypothesis is called
        Then must call ordinary_least_squares_linear_regression for parameters"""
        # Arrange
        analytical_data = [0.188, 0.192, 0.203, 0.288, 0.292, 0.303, 0.388, 0.392, 0.403]
        concentration_data = [0.008, 0.008016, 0.008128, 0.009, 0.009016, 0.009128, 0.010, 0.010016, 0.010128]
        # Act
        model = LinearityValidator(analytical_data, concentration_data)
        model.check_hypothesis()
        # Assert
        assert model.has_required_parameters

    def test_check_hypothesis_must_return_true_when_slope_pvalue_is_smaller_than_alpha(self):
        """Given homokedastic data
        When check_hypothesis is called
        Then slope_is_significant must assert true"""
        # Arrange
        analytical_data = [0.188, 0.192, 0.203, 0.288, 0.292, 0.303, 0.388, 0.392, 0.403]
        concentration_data = [0.008, 0.008016, 0.008128, 0.009, 0.009016, 0.009128, 0.010, 0.010016, 0.010128]
        # Act
        model = LinearityValidator(analytical_data, concentration_data)
        model.check_hypothesis()
        # Assert
        assert model.significant_slope

    def test_check_hypothesis_must_return_true_when_intercept_pvalue_is_greater_than_alpha(self):
        """Given homokedastic data
        When check_hypothesis is called
        Then intercept_not_significant must assert true"""
        # Arrange
        analytical_data = [0.188, 0.192, 0.203, 0.349, 0.346, 0.348, 0.489, 0.482, 0.492, 0.637, 0.641, 0.641, 0.762,
                           0.768, 0.786, 0.931, 0.924,
                           0.925]  # [0.188, 0.192, 0.203, 0.288, 0.292, 0.303, 0.388, 0.392, 0.403]
        concentration_data = [0.008, 0.008016, 0.008128, 0.016, 0.016032, 0.016256, 0.02, 0.02004, 0.02032,
                              0.027999996640000406, 0.028055996633280407, 0.02844799658624041, 0.032, 0.032064,
                              0.032512, 0.04, 0.04008, 0.04064]

        # Act
        model = LinearityValidator(analytical_data, concentration_data)
        model.check_hypothesis()
        # Assert
        assert model.insignificant_intercept

    def test_check_hypothesis_must_return_true_when_r_squared_is_greater_than_0990(self):
        """Given homokedastic data
        When check_hypothesis is called
        Then r_squared > 0.990 must assert true"""
        # Arrange
        analytical_data = [0.188, 0.192, 0.203, 0.288, 0.292, 0.303, 0.388, 0.392, 0.403]
        concentration_data = [0.008, 0.008016, 0.008128, 0.009, 0.009016, 0.009128, 0.010, 0.010016, 0.010128]
        # Act
        model = LinearityValidator(analytical_data, concentration_data)
        model.check_hypothesis()
        # Assert
        assert model.valid_r_squared



    def test_check_outliers_must_pass_when_removed_outliers_is_true(self):
        """Given data,
        when check_outliers is called a second time
        should pass
        """
        # Arrange
        analytical_data = [0.100, 0.200, 0.300]
        concentration_data = [1, 2, 3]
        with pytest.raises(AlreadyCleanedOutliers):
            model = LinearityValidator(analytical_data, concentration_data)
            model.check_outliers()
            # Act
            model.check_outliers()
        # Assert
        assert AlreadyCleanedOutliers()

    def test_check_outliers_must_pass_when_given_a_list_without_outliers(self):
        """Given data with no outliers
        when check_outliers is called
        should pass
        """
        # Arrange
        analytical_data = [0.100, 0.100, 0.100]
        concentration_data = [1, 2, 3]
        model = LinearityValidator(analytical_data, concentration_data)
        # Act
        model.check_outliers()
        # Assert
        assert model.has_outliers is False

    def test_check_outliers_must_create_an_empty_list_of_outliers_when_no_outliers_found(self):
        """Given data with no outliers
        when check_outlier is called
        Should create a empty list"""
        # Arrange
        analytical_data = [0.100, 0.200, 0.150, 0.200, 0.150]
        concentration_data = [1, 2, 3, 4, 5]
        model = LinearityValidator(analytical_data, concentration_data)
        model.check_outliers()
        # Act
        model.check_outliers()
        # Assert
        assert model.outliers == []

    def test_check_outliers_must_create_a_list_of_outliers_when_outliers_found(self):
        """Given data with no outliers
        when check_outlier is called
        Should create a empty list"""
        # Arrange
        analytical_data = [0.100, 2.0, 0.150, 0.200, 0.150]
        concentration_data = [1, 2, 3, 4, 5]
        model = LinearityValidator(analytical_data, concentration_data)
        # Act
        model.check_outliers()
        # Assert
        assert model.outliers == [2.0]

    def test_check_outliers_must_create_a_list_of_cleaned_data_when_given_data_with_outliers(self):
        # Arrange
        analytical_data = [0.100, 2.0, 0.150, 0.100, 0.150]
        concentration_data = [1, 2, 3, 4, 5]
        model = LinearityValidator(analytical_data, concentration_data)
        # Act
        model.check_outliers()
        # Assert
        assert model.cleaned_data == [0.100, 0.150, 0.100, 0.150]
    # TODO check how many times you can check for outliers inside data set

    def test_check_outliers_must_create_a_list_of_cleaned_concentration_when_given_data_with_outliers(self):
        """Given a data with outliers
        When check_outliers is called
        Should also remove the corresponding
        concentration point"""
        # Arrange
        analytical_data = [0.100, 2.0, 0.150, 0.100, 0.150]
        concentration_data = [1, 2, 3, 4, 5]
        model = LinearityValidator(analytical_data, concentration_data)
        # Act
        model.check_outliers()
        # Assert
        assert model.cleaned_concentration == [1, 3, 4, 5]

    def test_check_outliers_must_raise_exception_when_more_than_nminus1_point_removed_from_set(self):
        """Given data with outliers n-2 outliers
    '   where n is the number of points in a set
        When check_outliers is called
        Should raise a execption"""
        # Arrange
        analytical_data = [0.100, 2.0, 0.100, 50.0, 20.0]
        concentration_data = [1, 2, 3, 4, 5]
        with pytest.raises(DataNotConsistent):
            model = LinearityValidator(analytical_data, concentration_data)
        # Act
            model.check_outliers()
        # Assert
        assert DataNotConsistent()

    def test_check_residual_autocorrelation_must_raise_exception_when_data_not_fitted(self):
        """Given data,
        if no regression was calculated
        Should raise an exception"""
        analytical_data = [0.100, 0.150, 0.100]
        concentration_data = [0.01, 0.01, 0.01]
        with pytest.raises(DataWasNotFitted):
            model = LinearityValidator(analytical_data, concentration_data)
        # Act
            model.check_residual_autocorrelation()
        # Assert
        assert DataWasNotFitted()

    def test_check_residual_autocorrelation_must_raise_exception_when_residues_None(self):
        """Given data,
        if the residues is none
        When check_residual_autocorrelation is called
        Should raise an exception"""
        # Arrange
        analytical_data = [0.100, 0.150, 0.100]
        concentration_data = [0.01, 0.01, 0.01]
        with pytest.raises(DataWasNotFitted):
            model = LinearityValidator(analytical_data, concentration_data)
        # Act
            model.check_residual_autocorrelation()
        # Assert
        assert DataWasNotFitted()

    def test_check_residual_autocorrelation_must_pass_when_durbin_watson_value_is_between_0_and_4(self):
        """Given data,
        When check_residual is called
        after fitting the model
        Should pass creating
        0 < durbin_watson_value < 4"""
        # Arrange
        analytical_data = [0.188, 0.192, 0.203, 0.288, 0.292, 0.303, 0.388, 0.392, 0.403]
        concentration_data = [0.008, 0.008016, 0.008128, 0.009, 0.009016, 0.009128, 0.010, 0.010016, 0.010128]
        model = LinearityValidator(analytical_data, concentration_data)
        model.ordinary_least_squares_linear_regression()
        # Act
        model.check_residual_autocorrelation()
        # Assert
        assert model.durbin_watson_value # TODO insert value
