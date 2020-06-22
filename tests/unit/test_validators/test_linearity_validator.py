from analytical_validation.exceptions import AnalyticalValueNotNumber, ConcentrationValueNotNumber, \
    AnalyticalValueNegative, ConcentrationValueNegative
from src.analytical_validation.validators.linearity_validator import LinearityValidator

import pytest


class TestLinearityValidator(object):
    def test_constructor(self):
        pass

    def test_validate(self):
        pass

    def test_ordinary_least_squares_linear_regression_must_return_float_when_concentration_float(self):
        """Given concentration values != float
        The ordinary_least_squares_linear_regression
        Should raise exception"""
        # Arrange

        # Act

        # Assert
        pass

    def test_ordinary_least_squares_linear_regression_must_return_float_when_analytical_values_float(self):
        """Given analytical values != float
        The ordinary_least_squares_linear_regression
        Should raise exception"""
        # Arrange
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = ["STRING", 0.2, 0.3]
        # Act
        # Assert
        pass

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
        analytical_data = [0.100, 0.600, 0.03, 0.300]
        concentration_data = [0.2, 0.8, 1.2, 0.3]
        model = LinearityValidator(analytical_data, concentration_data)
        model.ordinary_least_squares_linear_regression()
        # Act
        model.check_homokedasticity()
        # Assert
        assert model.is_homokedastic is False

    def test_check_homokedasticity_must_return_true_when_data_is_homokedastic(self):
        """Given homokedastic data
        When check_homokedasticity is called
        Then must return true"""

        # Arrange
        analytical_data = [0.188, 0.192, 0.203]
        concentration_data = [0.008, 0.008016, 0.008128]
        model = LinearityValidator(analytical_data, concentration_data)
        model.ordinary_least_squares_linear_regression()
        # Act
        model.check_homokedasticity()
        # Assert
        assert model.is_homokedastic is True

    def test_anova_analysis_must_raise_exception_when_analytical_data_is_not_float(self):
        """When given non float analytical data parameters
        The anova analysis
        should raise exception."""

        # Arrange
        analytical_data = ["STRING", 0.200, 0.150]
        concentration_data = [0.2, 0.2, 0.3]
        # Act
        # Assert
        pass

    def test_anova_analysis_must_raise_exception_when_concentration_is_not_float(self):
        """When given non float concentration parameters
        The anova analysis
        should raise exception."""
        # Arrange
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = ["STRING", 0.2, 0.3]
        # Act
        # Assert
        pass

    def test_anova_analysis_must_raise_exception_when_negative_concentration(self):
        """Given negative concentration values
        The ordinary_least_squares_linear_regression
        Should raise exception"""
        # Arrange
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = [-0.2, 0.2, 0.3]
        # Act
        # Assert
        pass

    def test_anova_analysis_must_raise_exception_when_negative_analytical_values(self):
        """Given negative values
        When I call ordinary_least_squares_linear_regression
        Then it must raise exception"""
        # Arrange
        analytical_data = [-0.100, 0.200, 0.150]
        concentration_data = [0.2, 0.2, 0.3]
        # Act
        # Assert
        pass