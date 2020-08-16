import pytest

from analytical_validation.validators.intermediate_precision_validator import IntermediatePrecision


@pytest.fixture(scope="function")
def intermediate_precision_object():
    intermediate_precision = IntermediatePrecision(alpha=0.05,
                                                   analytical_data=[0.1, 0.11, 0.12,   # Day 1, analyst A
                                                                    0.1, 0.11, 0.12,   # Day 1, analyst B
                                                                    0.1, 0.11, 0.12,   # Day 2, analyst A
                                                                    0.1, 0.11, 0.12],  # Day 2, analyst B
                                                   intercept=0.0001,
                                                   slope=20.2,
                                                   )
    return intermediate_precision


@pytest.fixture(scope="function")
def two_way_anova_mocked_object(mocker):
    mock = mocker.Mock(create=True)
    return mock


class TestIntermediatePrecisionValidator:

    def test_calculate_obtained_concentrations(self):
        """
        Given a slope, intercept and analytical data,
        when calculate_obtained_concentrations is called,
        must create a list containing the calculated concentrations
        """

    def test_calculate_obtained_concentrations_must_raise_a_warning_given_incorrect_data(self):
        """
        Given an incorrect slope, intercept or analytical data,
        when calculate_obtained_concentrations is called,
        must raise an warning
        """

    def test_calculate_obtained_concentrations_must_keep_none_type_concentration_values_without_raising_error(self):
        """
        Given None type concentration values with correct data,
        when calculate_obtained_concentrations is called,
        must calculate the data and keep the None values in the set
        """

    def test_two_way_anova(self):
        """
        Given a concentration data set,
        when two_way ANOVA is called,
        must return an object containing the ANOVA properties
        """

    def test_two_way_anova_must_not_raise_warning_when_given_none_type_values(self):
        """
        Given a concentration data set with None type values,
        when two_way_anova is called,
        must return the correct object containing ANOVA properties
        """

    def test_two_way_anova_must_raise_warning_when_given_invalid_data(self):
        """
        Given incorrect data type,
        when two_way_anova is called,
        should raise a warning.
        """

    def test_validate_intermediate_precision_must_return_true_if_data_is_validated(self):
        """
        Given the correct data that meets the specifications,
        when validate_intermediate_precision is called,
        must return True
        """

    def test_validate_intermediate_precision_must_return_false_if_data_is_not_validated(self):
        """
        Given the correct data that doesn't meet the intermediate precision specifications,
        when validate_intermediate_precision is called,
        must return False
        """
