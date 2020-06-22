from analytical_validation.exceptions import AnalyticalValueNotNumber, ConcentrationValueNotNumber, \
    AnalyticalValueNegative, ConcentrationValueNegative, AverageValueNotNumber, AverageValueNegative
from src.analytical_validation.validators.linearity_validator import LinearityValidator, AnovaValidator

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
        averages_data = []
        std_dev_data = []
        # Act
        with pytest.raises(ConcentrationValueNotNumber) as excinfo:
            LinearityValidator(analytical_data, concentration_data, averages_data, std_dev_data).ordinary_least_squares_linear_regression()
        # Assert
        assert "One of the concentration values is not a number!" in str(excinfo.value)

    def test_ordinary_least_squares_linear_regression_must_raise_exception_when_analytical_values_not_float(self):
        """Given analytical values != float
        The ordinary_least_squares_linear_regression
        Should raise exception"""

        # Arrange
        analytical_data = ["STRING", 0.200, 0.150]
        concentration_data = [0.2, 0.2, 0.3]
        averages_data = []
        std_dev_data = []
        # Act
        with pytest.raises(AnalyticalValueNotNumber) as excinfo:
            LinearityValidator(analytical_data, concentration_data, averages_data, std_dev_data).ordinary_least_squares_linear_regression()
        # Assert
        assert "One of the analytical values is not a number!" in str(excinfo.value)

    def test_ordinary_least_squares_linear_regression_must_raise_exception_when_negative_concentration(self):
        """Given negative concentration values
        The ordinary_least_squares_linear_regression
        Should raise exception"""

        # Arrange
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = [-0.2, 0.2, 0.3]
        averages_data = []
        std_dev_data = []
        # Act
        with pytest.raises(ConcentrationValueNegative) as excinfo:
            LinearityValidator(analytical_data, concentration_data, averages_data, std_dev_data).ordinary_least_squares_linear_regression()
        # Assert
        assert "Negative value for concentration value is not valid!" in str(excinfo.value)

    def test_ordinary_least_squares_linear_regression_must_raise_exception_when_negative_analytical_values(self):
        """Given negative values
        When I call ordinary_least_squares_linear_regression
        Then it must raise exception"""

        # Arrange
        analytical_data = [-0.100, 0.200, 0.150]
        concentration_data = [0.2, 0.2, 0.3]
        averages_data = []
        std_dev_data = []
        # Act
        with pytest.raises(AnalyticalValueNegative) as excinfo:
            LinearityValidator(analytical_data, concentration_data, averages_data, std_dev_data).ordinary_least_squares_linear_regression()
        # Assert
        assert "Negative value for analytical signal is not valid!" in str(excinfo.value)

    def test_check_homokedasticity_must_raise_exeption_when_model_is_none(self):
        """Not given a model parameter
        The check_homokedasticity
        Should raise exception"""

        # Arrange
        analytical_data = [0.100, 0.200, 0.150]
        concentration_data = [0.2, 0.2, 0.3]
        averages_data = []
        std_dev_data = []
        # Act
        with pytest.raises(Exception) as excinfo:
            LinearityValidator(analytical_data, concentration_data, averages_data, std_dev_data).check_homokedasticity()
        # Assert
        assert "There is not a regression model to check the homokedasticity." in str(excinfo.value)

    def test_check_homokedasticity_must_return_false_when_data_is_heterokedastic(self):
        """Given heterokedastic data
        When check_homokedasticity is called
        Then must return false"""
        # Arrange
        averages_data = []
        std_dev_data = []
        analytical_data = [0.100, 0.600, 0.03, 0.300]
        concentration_data = [0.2, 0.8, 1.2, 0.3]
        model = LinearityValidator(analytical_data, concentration_data, averages_data, std_dev_data)
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
        averages_data = []
        std_dev_data = []
        analytical_data = [0.188, 0.192, 0.203]
        concentration_data = [0.008, 0.008016, 0.008128]
        model = LinearityValidator(analytical_data, concentration_data, averages_data, std_dev_data)
        model.ordinary_least_squares_linear_regression()
        # Act
        model.check_homokedasticity()
        # Assert
        assert model.is_homokedastic is True



class TestAnovaValidator(object):


    def test_constructor_must_raise_exception_when_average_is_not_float(self):
        """Given non float average
        When anova_analysis is called
        Then must raise exception"""
        # Arrange
        averages_data = ["0.175", 0.270]
        analytical_data = [[0.100, 0.200, 0.150], [0.250, 0.280, 0.300]]
        # Act
        with pytest.raises(AverageValueNotNumber) as excinfo:
            AnovaValidator(analytical_data, averages_data)
        # Assert
        assert "One of the average values is not a number!" in str(excinfo.value)

    def test_constructor_must_raise_exception_when_average_is_negative(self):
        """Given negative float average
        When anova_analysis is called
        Then must raise exception"""
        # Arrange
        averages_data = [-0.175, 0.270]
        analytical_data = [[0.100, 0.200, 0.150], [0.250, 0.280, 0.300]]
        # Act
        with pytest.raises(AverageValueNegative) as excinfo:
            AnovaValidator(analytical_data, averages_data)
        # Assert
        assert "Negative value for average value is not valid!" in str(excinfo.value)

    def test_constructor_must_raise_exception_when_analytical_data_is_not_float(self):
        """When given non float analytical data parameters
        The anova analysis
        should raise exception."""
        # Arrange
        averages_data = [0.175, 0.270]
        analytical_data = [["0.100", 0.200, 0.150], [0.250, 0.280, 0.300]]
        # Act
        with pytest.raises(AnalyticalValueNotNumber) as excinfo:
            AnovaValidator(analytical_data, averages_data)
        # Assert
        assert "One of the analytical values is not a number!" in str(excinfo.value)

    def test_constructor_must_raise_exception_when_negative_analytical_values(self):
        """Given negative values
        When I call ordinary_least_squares_linear_regression
        Then it must raise exception"""
        # Arrange
        averages_data = [0.175, 0.270]
        analytical_data = [[-0.100, 0.200, 0.150], [0.250, -0.280, 0.300]]
        # Act
        with pytest.raises(AnalyticalValueNegative) as excinfo:
            AnovaValidator(analytical_data, averages_data)
        # Assert
        assert "Negative value for analytical signal is not valid!" in str(excinfo.value)


    def test_anova_analysis_must_return_int_degrees_of_freedom_btwn_treatments(self):
        """Given data, averages
        When anova_analysis is called
        Then must pass"""
        # Arrange
        averages_data = [0.15, 0.2767]
        analytical_data = [[0.100, 0.200, 0.150, 0.100, 0.200, 0.150], [0.250, 0.280, 0.300, 0.250, 0.280, 0.300]]
        # Act
        anova_validation = AnovaValidator(analytical_data, averages_data)
        anova_validation.anova_degrees_of_freedom()
        # Assert
        assert anova_validation.degrees_of_freedom_btwn_treatments == 1

    def test_anova_analysis_must_return_int_error_degrees_of_freedom(self):
        """Given data, averages
        When anova_analysis is called
        Then must pass"""
        # Arrange
        averages_data = [0.15, 0.2767]
        analytical_data = [[0.100, 0.200, 0.150, 0.100, 0.200, 0.150], [0.250, 0.280, 0.300, 0.250, 0.280, 0.300]]
        # Act
        anova_validation = AnovaValidator(analytical_data, averages_data)
        anova_validation.anova_degrees_of_freedom()
        # Assert
        assert anova_validation.residual_degrees_of_freedom == 10

    def test_anova_analysis_must_return_int_total_degrees_of_freedom(self):
        """Given data, averages
        When anova_analysis is called
        Then must pass"""
        # Arrange
        averages_data = [0.15, 0.2767]
        analytical_data = [[0.100, 0.200, 0.150, 0.100, 0.200, 0.150], [0.250, 0.280, 0.300, 0.250, 0.280, 0.300]]
        # Act
        anova_validation = AnovaValidator(analytical_data, averages_data)
        anova_validation.anova_degrees_of_freedom()
        # Assert
        assert anova_validation.total_degrees_of_freedom == 11

    def test_anova_analysis_must_return_float_squares_btwn_treatments(self):
        """Given data, averages
        When anova_analysis is called
        Then must pass"""
        # Arrange
        averages_data = [0.15, 0.2767]
        analytical_data = [[0.100, 0.200, 0.150, 0.100, 0.200, 0.150], [0.250, 0.280, 0.300, 0.250, 0.280, 0.300]]
        # Act
        anova_validation = AnovaValidator(analytical_data, averages_data)
        anova_validation.anova_sum_of_squares()
        # Assert
        assert anova_validation.sum_of_squares_btwn_treatments == 0.04815867333333334

    def test_anova_analysis_must_return_float_sum_of_squares_residual(self):
        """Given data, averages
        When anova_analysis is called
        Then must pass"""
        # Arrange
        averages_data = [0.15, 0.2767]
        analytical_data = [[0.100, 0.200, 0.150, 0.100, 0.200, 0.150], [0.250, 0.280, 0.300, 0.250, 0.280, 0.300]]
        # Act
        anova_validation = AnovaValidator(analytical_data, averages_data)
        anova_validation.anova_sum_of_squares()
        # Assert
        assert anova_validation.sum_of_squares_residual == 0.01253334

    def test_anova_analysis_must_return_float_sum_of_squares_total(self):
        """Given data, averages
        When anova_analysis is called
        Then must pass"""
        # Arrange
        averages_data = [0.15, 0.2767]
        analytical_data = [[0.100, 0.200, 0.150, 0.100, 0.200, 0.150], [0.250, 0.280, 0.300, 0.250, 0.280, 0.300]]
        # Act
        anova_validation = AnovaValidator(analytical_data, averages_data)
        anova_validation.anova_sum_of_squares()
        # Assert
        assert anova_validation.sum_of_squares_total == 0.060692013333333336

    def test_anova_analysis_must_return_float_mean_squares_btwn_treatments(self):
        """Given data, averages
        When anova_analysis is called
        Then must pass"""
        # Arrange
        averages_data = [0.15, 0.2767]
        analytical_data = [[0.100, 0.200, 0.150, 0.100, 0.200, 0.150], [0.250, 0.280, 0.300, 0.250, 0.280, 0.300]]
        anova_validation = AnovaValidator(analytical_data, averages_data)
        anova_validation.anova_degrees_of_freedom()
        anova_validation.anova_sum_of_squares()
        # Act
        anova_validation.anova_mean_squares()
        # Assert
        assert anova_validation.mean_squares_btwn_treatments == 0.04815867333333334

    def test_anova_analysis_must_return_float_mean_squares_of_residues(self):
        """Given data, averages
        When anova_analysis is called
        Then must pass"""
        # Arrange
        averages_data = [0.15, 0.2767]
        analytical_data = [[0.100, 0.200, 0.150, 0.100, 0.200, 0.150], [0.250, 0.280, 0.300, 0.250, 0.280, 0.300]]
        anova_validation = AnovaValidator(analytical_data, averages_data)
        anova_validation.anova_degrees_of_freedom()
        anova_validation.anova_sum_of_squares()
        # Act
        anova_validation.anova_mean_squares()
        # Assert
        assert anova_validation.mean_squares_of_residues == 0.001253334

    def test_anova_f_ratio_must_return_f_anova_as_float(self):
        """Give data, averages
        when anova_f_ratio is called
        Then must return a tuple of float"""
        averages_data = [0.15, 0.2767]
        analytical_data = [[0.100, 0.200, 0.150, 0.100, 0.200, 0.150], [0.250, 0.280, 0.300, 0.250, 0.280, 0.300]]
        anova_validation = AnovaValidator(analytical_data, averages_data)
        anova_validation.anova_f_ratio()
        assert anova_validation.f_anova == 38.40425531914891

    def test_anova_f_ratio_must_return_p_anova_as_float(self):
        """Give data, averages
        when anova_f_ratio is called
        Then must return a tuple of float"""
        averages_data = [0.15, 0.2767]
        analytical_data = [[0.100, 0.200, 0.150, 0.100, 0.200, 0.150], [0.250, 0.280, 0.300, 0.250, 0.280, 0.300]]
        anova_validation = AnovaValidator(analytical_data, averages_data)
        anova_validation.anova_f_ratio()
        assert anova_validation.p_anova == 0.00010183683714905551

