import pytest

from analytical_validation.exceptions import AnalyticalValueNotNumber, AverageValueNegative, AverageValueNotNumber, \
    AnalyticalValueNegative
from analytical_validation.statistical_tests.anova_analysis import AnovaValidator


@pytest.fixture(scope='function')
def anova_validator_obj():
    averages_data = [0.15, 0.2767]
    analytical_data = [[0.100, 0.200, 0.150, 0.100, 0.200, 0.150], [0.250, 0.280, 0.300, 0.250, 0.280, 0.300]]
    return AnovaValidator(averages_data, analytical_data)

class TestAnovaValidator(object):

    def test_constructor_must_raise_exception_when_average_is_not_float(self):
        """Given non float average
        When anova_analysis is called
        Then must raise exception"""
        # Arrange
        averages_data = ["0.175", 0.270]
        analytical_data = [[0.100, 0.200, 0.150], [0.250, 0.280, 0.300]]
        # Act & Assert
        with pytest.raises(AverageValueNotNumber):
            AnovaValidator(analytical_data, averages_data)

    def test_constructor_must_raise_exception_when_average_is_negative(self):
        """Given negative float average
        When anova_analysis is called
        Then must raise exception"""
        # Arrange
        averages_data = [-0.175, 0.270]
        analytical_data = [[0.100, 0.200, 0.150], [0.250, 0.280, 0.300]]
        # Act & Assert
        with pytest.raises(AverageValueNegative):
            AnovaValidator(analytical_data, averages_data)

    def test_constructor_must_raise_exception_when_analytical_data_is_not_float(self):
        """When given non float analytical data parameters
        The anova analysis
        should raise exception."""
        # Arrange
        averages_data = [0.175, 0.270]
        analytical_data = [["0.100", 0.200, 0.150], [0.250, 0.280, 0.300]]
        # Act & Aseert
        with pytest.raises(AnalyticalValueNotNumber):
            AnovaValidator(analytical_data, averages_data)

    def test_constructor_must_raise_exception_when_negative_analytical_values(self):
        """Given negative values
        When I call ordinary_least_squares_linear_regression
        Then it must raise exception"""
        # Arrange
        averages_data = [0.175, 0.270]
        analytical_data = [[-0.100, 0.200, 0.150], [0.250, -0.280, 0.300]]
        # Act & Assert
        with pytest.raises(AnalyticalValueNegative):
            AnovaValidator(analytical_data, averages_data)

    # TODO: make a mock test for flat_analytical_data = numpy.hstack(self.analytical_data)
    def test_anova_analysis_must_pass_float_when_given_float_data(self):
        # TODO: make a mock test for flat_analytical_data = numpy.hstack(self.analytical_data)
        pass

    def test_anova_analysis_must_return_int_degrees_of_freedom_btwn_treatments(self, anova_validator_obj):
        """Given data, averages
        When anova_analysis is called
        Then must pass"""
        # Arrange
        anova_validation = anova_validator_obj
        anova_validation.anova_degrees_of_freedom()
        # Assert
        assert anova_validation.degrees_of_freedom_btwn_treatments == 1

    def test_anova_analysis_must_return_int_error_degrees_of_freedom(self, anova_validator_obj):
        """Given data, averages
        When anova_analysis is called
        Then must pass"""
        # Arrange
        anova_validation = anova_validator_obj
        anova_validation.anova_degrees_of_freedom()
        # Assert
        assert anova_validation.residual_degrees_of_freedom == 10

    def test_anova_analysis_must_return_int_total_degrees_of_freedom(self, anova_validator_obj):
        """Given data, averages
        When anova_analysis is called
        Then must pass"""
        # Arrange
        anova_validation = anova_validator_obj
        anova_validation.anova_degrees_of_freedom()
        # Assert
        assert anova_validation.total_degrees_of_freedom == 11

    def test_anova_analysis_must_return_float_squares_btwn_treatments(self, anova_validator_obj):
        """Given data, averages
        When anova_analysis is called
        Then must pass"""
        # Arrange
        anova_validation = anova_validator_obj
        anova_validation.anova_sum_of_squares()
        # Assert
        assert anova_validation.sum_of_squares_btwn_treatments == 0.04815867333333334

    def test_anova_analysis_must_return_float_sum_of_squares_residual(self, anova_validator_obj):
        """Given data, averages
        When anova_analysis is called
        Then must pass"""
        # Arrange
        anova_validation = anova_validator_obj
        anova_validation.anova_sum_of_squares()
        # Assert
        assert anova_validation.sum_of_squares_residual == 0.01253334

    def test_anova_analysis_must_return_float_sum_of_squares_total(self, anova_validator_obj):
        """Given data, averages
        When anova_analysis is called
        Then must pass"""
        # Arrange
        anova_validation = anova_validator_obj
        anova_validation.anova_sum_of_squares()
        # Assert
        assert anova_validation.sum_of_squares_total == 0.060692013333333336

    def test_anova_analysis_must_return_float_mean_squares_btwn_treatments(self, anova_validator_obj):
        """Given data, averages
        When anova_analysis is called
        Then must pass"""
        # Arrange
        anova_validation = anova_validator_obj
        anova_validation.anova_degrees_of_freedom()
        anova_validation.anova_sum_of_squares()
        # Act
        anova_validation.anova_mean_squares()
        # Assert
        assert anova_validation.mean_squares_btwn_treatments == 0.04815867333333334

    def test_anova_analysis_must_return_float_mean_squares_of_residues(self, anova_validator_obj):
        """Given data, averages
        When anova_analysis is called
        Then must pass"""
        # Arrange
        anova_validation = anova_validator_obj
        anova_validation.anova_degrees_of_freedom()
        anova_validation.anova_sum_of_squares()
        # Act
        anova_validation.anova_mean_squares()
        # Assert
        assert anova_validation.mean_squares_of_residues == 0.001253334

    def test_anova_f_ratio_must_return_f_anova_as_float(self, anova_validator_obj):
        """Give data, averages
        when anova_f_ratio is called
        Then must return a tuple of float"""
        anova_validation = anova_validator_obj
        anova_validation.anova_f_ratio()
        assert anova_validation.f_anova == 38.40425531914891

    def test_anova_f_ratio_must_return_p_anova_as_float(self, anova_validator_obj):
        """Give data, averages
        when anova_f_ratio is called
        Then must return a tuple of float"""
        anova_validation = anova_validator_obj
        anova_validation.anova_f_ratio()
        assert anova_validation.p_anova == 0.00010183683714905551
