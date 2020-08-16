import pytest

from analytical_validation.exceptions import IncorrectIntermediatePrecisionData
from analytical_validation.validators.intermediate_precision_validator import IntermediatePrecision

_correct_data = [0.1, 0.11, 0.12,
                 0.1, 0.11, 0.12,
                 0.1, 0.11, 0.12,
                 0.1, 0.11, 0.12]

_data_with_none = [0.1, 0.11, 0.12,
                   0.1, None, 0.12,
                   0.1, 0.11, 0.12,
                   0.1, 0.11, None]


@pytest.fixture(scope="function")
def two_way_anova_mocked_object(mocker):
    mock = mocker.Mock(create=True)
    mock.sum_sq = mocker.Mock()
    mock.df = mocker.Mock()
    mock.F = mocker.Mock()
    mock.PR = mocker.Mock()
    return mock


@pytest.fixture(scope="function")
def intermediate_precision_object(two_way_anova_mocked_object, given_analytical_data=_correct_data):
    intermediate_precision = IntermediatePrecision(alpha=0.05,
                                                   analytical_data=given_analytical_data,
                                                   intercept=0.1,
                                                   slope=5,
                                                   )
    intermediate_precision.two_way_anova_result = two_way_anova_mocked_object
    return intermediate_precision


class TestIntermediatePrecisionValidator:

    def test_calculate_obtained_concentrations(self, intermediate_precision_object):
        """
        Given a slope, intercept and analytical data,
        when calculate_obtained_concentrations is called,
        must create a list containing the calculated concentrations
        """
        intermediate_precision = intermediate_precision_object
        expected_result = [
            0.6, 0.65, 0.7,
            0.6, 0.65, 0.7,
            0.6, 0.65, 0.7,
            0.6, 0.65, 0.7
        ]
        intermediate_precision.calculate_obtained_concentrations()
        assert intermediate_precision.calculated_concentration == expected_result

    @pytest.mark.parametrize("param_analytical_data", [
        "str", {"whaaat": 0.1}, 10, -1, None
    ])
    def test_calculate_obtained_concentrations_must_raise_a_warning_given_incorrect_data(self, param_analytical_data):
        """
        Given an incorrect slope, intercept or analytical data,
        when calculate_obtained_concentrations is called,
        must raise an warning
        """
        intermediate_precision = IntermediatePrecision(alpha=0.05,
                                                       analytical_data=param_analytical_data,
                                                       intercept=0.1,
                                                       slope=5,
                                                       )
        with pytest.raises(IncorrectIntermediatePrecisionData):
            intermediate_precision.calculate_obtained_concentrations()

    def test_calculate_obtained_concentrations_must_keep_none_type_concentration_values_without_raising_error(self,
                                                                                                              intermediate_precision_object):
        """
        Given None type concentration values with correct data,
        when calculate_obtained_concentrations is called,
        must calculate the data and keep the None values in the set
        """
        expected_result = [
            0.6, 0.65, 0.7,
            0.6, None, 0.7,
            0.6, 0.65, 0.7,
            0.6, 0.65, None
        ]
        intermediate_precision = IntermediatePrecision(alpha=0.05,
                                                       analytical_data=_data_with_none,
                                                       intercept=0.1,
                                                       slope=5,
                                                       )
        intermediate_precision.calculate_obtained_concentrations()
        assert intermediate_precision.calculated_concentration == expected_result

    def test_two_way_anova(self, intermediate_precision_object, two_way_anova_mocked_object):
        """
        Given a concentration data set,
        when two_way ANOVA is called,
        must return an object containing the ANOVA properties
        """
        assert intermediate_precision_object.two_way_anova_result == two_way_anova_mocked_object

    def test_two_way_anova_must_not_raise_warning_when_given_none_type_values(self,
                                                                              intermediate_precision_object):
        """
        Given a concentration data set with None type values,
        when two_way_anova is called,
        must return the correct object containing ANOVA properties
        """
        intermediate_precision = IntermediatePrecision(analytical_data=_data_with_none, intercept=2, slope=2,
                                                       alpha=0.05)
        intermediate_precision.calculate_obtained_concentrations()
        try:
            intermediate_precision.two_way_anova()
        except IncorrectIntermediatePrecisionData:
            pytest.fail("Unexpected MyError ..")

    def test_validate_intermediate_precision_must_return_true_if_data_is_validated(self,
                                                                                   intermediate_precision_object):
        """
        Given the correct data that meets the specifications,
        when validate_intermediate_precision is called,
        must return True
        """
        intermediate_precision = intermediate_precision_object
        intermediate_precision.validate_intermediate_precision()
        assert intermediate_precision.is_intermediate_precise is True

    def test_validate_intermediate_precision_must_return_false_if_data_is_not_validated(self,
                                                                                        intermediate_precision_object):
        """
        Given the correct data that doesn't meet the intermediate precision specifications,
        when validate_intermediate_precision is called,
        must return False
        """
        not_precise_data = [30192, 321, 123,
                            8320, 31231, 3123,
                            765, 342, 356,
                            987, 738, 123]
        intermediate_precision = IntermediatePrecision(analytical_data=not_precise_data, intercept=2, slope=2,
                                                       alpha=0.05)
        intermediate_precision.validate_intermediate_precision()
        assert intermediate_precision.is_intermediate_precise is False
