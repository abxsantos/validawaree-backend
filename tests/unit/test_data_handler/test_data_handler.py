import pytest

from analytical_validation.data_handler.data_handler import DataHandler, check_values, check_is_list, check_list_of_lists
from analytical_validation.exceptions import DataNotList, DataNotListOfLists, ValueNotValid, DataNotSymmetric


class TestDataHandlerHelper(object):

    @pytest.mark.parametrize('param_value', [
        1, 0.1, .1, "1.234", "123.E4", ".1", "6.523537535629999e-07", "6e777777", "1.797693e+308", "0E0", "+1e1",
         "+1e1", "  1.23  ", "  \n    1.23    \n\n", None
    ])
    def test_check_value_must_return_float_when_given_positive_numbers(self, param_value):
        """Given positive numbers,
        When check value is called
        must return the value parsed to float"""
        assert isinstance(check_values(param_value), float) is True or check_values(param_value) is None

    @pytest.mark.parametrize('param_data', [
        "STR", {}, 1, 0.990, (0, 1)
    ])
    def test_check_is_list_must_raise_exception_when_not_list(self, param_data):
        """
        Given data of different types
        when check_is_list is called
        must raise an DataNotList
        """
        with pytest.raises(DataNotList):
            check_is_list(param_data)

    @pytest.mark.parametrize('param_data', [
        ["STR"], [{}], [1], [0.990], [(0, 1)]
    ])
    def test_check_list_of_lists_must_raise_exception_when_not_list_of_lists(self, param_data):
        """
        Given data that it's not a list of lists
        when check_list_of_lists is called
        must raise an DataNotListOfLists
        """
        with pytest.raises(DataNotListOfLists):
            check_list_of_lists(param_data)

    @pytest.mark.parametrize('param_data', [
        ([["STR", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["NaNananana BATMAN", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["NULL", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["123.EE4", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([[0.1, 0.2, 0.1], [0.1, "infinity and BEYOND", 0.1]]),
        ([["12.34.56", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["#56", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["56%", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([[0.1, 0.2, 0.1], [0.1, "x86E0", 0.1]]),
        ([["86-5", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([[0.1, 0.2, 0.1], [0.1, 0.2, "True"]]),
        ([["+1e1^5", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["56%", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([[True, 0.2, 0.1], [0.1, 0.2, 0.1]]),
    ])
    def test_check_list_of_lists_must_raise_exception_when_value_not_valid(self, param_data):
        """Given a list of lists with not number value(s)
        when check_list_of_lists is called,
        Must raise an ValueNotValid"""
        with pytest.raises(ValueNotValid):
            check_list_of_lists(param_data)

    @pytest.mark.parametrize('param_data, expected_result', [
        ([["1,234", 0.2, 0.1], [0.1, 0.2, 0.1]], [[1.234, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([[",1", 0.2, 0.1], [0.1, 0.2, 0.1]], [[0.1, 0.2, 0.1], [0.1, 0.2, 0.1]])
    ])
    def test_check_list_of_lists_must_convert_number_with_comma_to_float(self, param_data, expected_result):
        """Given a list of lists containing strings with comma separated decimals
        When check_list_of_lists is called
        Must pass returning the values converted to float"""
        assert check_list_of_lists(param_data) == expected_result

    @pytest.mark.parametrize('param_data, expected_result', [
        ([["1.234", 0.2, 0.1], [0.1, 0.2, 0.1]], [[1.234, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["123.E4", 0.2, 0.1], [0.1, 0.2, 0.1]], [[123.E4, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([[".1", 0.2, 0.1], [0.1, 0.2, 0.1]], [[0.1, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["6.523537535629999e-07", 0.2, 0.1], [0.1, 0.2, 0.1]], [[6.523537535629999e-07, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["6e777777", 0.2, 0.1], [0.1, 0.2, 0.1]], [[6e777777, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["1.797693e+308", 0.2, 0.1], [0.1, 0.2, 0.1]], [[1.797693e+308, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([[0.1, 0.2, 0.1], ["0E0", 0.2, 0.1]], [[0.1, 0.2, 0.1], [0.0, 0.2, 0.1]]),
        ([[0.2, "+1e1", 0.1], [0.1, 0.2, 0.1]], [[0.2, +1e1, 0.1], [0.1, 0.2, 0.1]]),
        ([["  1.23  ", 0.2, 0.1], [0.1, 0.2, 0.1]], [[1.23, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["  \n    1.23    \n\n", 0.2, 0.1], [0.1, 0.2, 0.1]], [[1.23, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([[None, 0.2, 0.1], [0.1, 0.2, 0.1]], [[None, 0.2, 0.1], [0.1, 0.2, 0.1]]),

    ])
    def test_check_list_of_lists_must_pass_when_value_is_conversible_to_float(self, param_data, expected_result):
        """Given a list of lists, with not float number value(s)
        when check _list_of_lists is called,
        Must create a list containing floats"""
        assert check_list_of_lists(param_data) == expected_result


class TestDataHandler(object):

    @pytest.mark.parametrize('param_analytical_data, param_concentration_data', [
        ([[1, 2, 3]], [[1, 2, 3], [4, 5, 6]]),
        ([[1, 2, 3], [4, 5, 6]], [[1, 2, 3]]),
        ([[1, 2, 3]], [[1, 2, 3], [4, 5, 6]]),
    ])
    def test_check_symmetric_data(self, param_analytical_data, param_concentration_data):
        """Given an asymetric list
        when check_symmetric_data is called
        must raise DataNotSymmetric"""
        with pytest.raises(DataNotSymmetric):
            DataHandler(param_analytical_data, param_concentration_data).check_symmetric_data()

    @pytest.mark.parametrize('param_analytical_data, param_concentration_data', [
        ([[1, 2, 3], [4, 5, 6, 8]], [[1, 2, 3], [4, 5, 6]]),
        ([[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6, 8]]),
        ([[1, 2, 3, 4], [5, 6, 8]], [[1, 2, 3], [4, 5, 6]]),
        ([[1, 2, 3], [4, 5, 6]], [[1, 2, 3, 4], [4, 5, 6, 8]]),

    ])
    def test_check_symmetric_data_set(self, param_analytical_data, param_concentration_data):
        """Given an asymetric data set
        when check_symmetric_data_set is called
        must raise DataNotSymmetric"""
        with pytest.raises(DataNotSymmetric):
            DataHandler(param_analytical_data, param_concentration_data).check_symmetric_data_set()

    @pytest.mark.parametrize(
        'param_analytical_data, param_concentration_data, expected_analytical_result, expected_concentration_result', [
            ([[1, 2, 3], [4, 5, None]], [[7, 8, 9], [10, 11, 12]], [[1, 2, 3], [4, 5]], [[7, 8, 9], [10, 11]]),
            ([[None, 2, 3], [4, 5, None]], [[7, 8, 9], [10, 11, 12]], [[2, 3], [4, 5]], [[8, 9], [10, 11]]),
            ([[None, 2, 3], [4, None, None]], [[7, 8, 9], [10, 11, 12]], [[2, 3], [4]], [[8, 9], [10]]),
            ([[None, 2, 3], [None, None, None]], [[7, 8, 9], [10, 11, 12]], [[2, 3]], [[8, 9]]),

        ])
    def test_replace_null_values(self, param_analytical_data, param_concentration_data, expected_analytical_result,
                                 expected_concentration_result):
        """Given data with null/none/undefined values,
        when replace_null_values is called,
        Must remove NoneType from both sets of lists
        """
        data_handler = DataHandler(param_analytical_data, param_concentration_data)
        clean_analytical_data, clean_concentration_data = data_handler.replace_null_values()
        assert clean_analytical_data == expected_analytical_result
        assert clean_concentration_data == expected_concentration_result

    def test_data_handler_must_pass_given_adequate_data(self):
        """Given analytical data and concentration data, in a list of lists,
        When handle_data is called
        must return a symmetrical list of lists containing only float values."""

        analytical_data = [
            [0.188, 0.192, 0.203],
            [0.349, 0.346, 0.348],
            [0.489, 0.482, 0.492],
            [0.637, 0.641, 0.641],
            [0.762, 0.768, 0.786],
            [0.931, 0.924, 0.925],
        ]
        concentration_data = [
            [0.008, 0.008, 0.008],
            [0.016, 0.016, 0.016],
            [0.02, 0.02, 0.02],
            [0.028, 0.028, 0.028],
            [0.032, 0.032, 0.032],
            [0.04, 0.04, 0.04],
        ]
        checked_analytical_data, checked_concentration_data = DataHandler(analytical_data,
                                                                          concentration_data).handle_data()
        assert checked_analytical_data == analytical_data
        assert checked_concentration_data == concentration_data
