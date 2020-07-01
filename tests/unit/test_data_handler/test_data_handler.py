import pytest

from analytical_validation.data_handler.data_handler import DataHandler
from analytical_validation.exceptions import DataNotList, DataNotListOfLists, ValueNotValid, DataNotSymmetric


class TestDataHandler(object):

    #  check for data inconsistency
    #  the analytical data must be completely symmetric with concentration data
    #  check if it's a list
    #  check if its a list containing lists (set of data)
    #  check if the number of set of data is symmetric
    #  check if the number of values in the data sets are symmetric
    #  check if values are numbers and convert to float
    #  check if there are invalid numbers (negative, null)
    #  clean up non real float values

    @pytest.mark.parametrize('param_data', [
        "STR", {}, 1, 0.990, (0, 1)
    ])
    def test_DataHandler_must_raise_exception_when_not_list(self, param_data):
        """
        Given data of different types
        when data_is_list is called
        must raise an exception
        """
        with pytest.raises(DataNotList):
            DataHandler.check_is_list(param_data)

    @pytest.mark.parametrize('param_data', [
        ["STR"], [{}], [1], [0.990], [(0, 1)]
    ])
    def test_DataHandler_must_raise_exception_when_not_list_of_lists(self, param_data):
        """
        Given data that it's not a list of lists
        when DataHandler is called
        must raise an exception
        """
        with pytest.raises(DataNotListOfLists):
            DataHandler.check_list_of_lists(param_data)

    @pytest.mark.parametrize('param_data', [
        ([["STR", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["NaNananana BATMAN", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["NULL", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["123.EE4", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["infinity and BEYOND", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["12.34.56", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["#56", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["56%", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["x86E0", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["86-5", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["True", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["+1e1^5", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["56%", 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([[True, 0.2, 0.1], [0.1, 0.2, 0.1]]),
    ])
    def test_check_list_of_lists_must_raise_exception_when_value_not_valid(self, param_data):
        """Given a list of lists with not number value(s)
        when check_list_of_lists is called,
        Must raise an ValueNotValid"""
        with pytest.raises(ValueNotValid):
            DataHandler.check_list_of_lists(param_data)

    @pytest.mark.parametrize('param_data, expected_result', [
        ([["1,234", 0.2, 0.1], [0.1, 0.2, 0.1]], [[1.234, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([[",1", 0.2, 0.1], [0.1, 0.2, 0.1]], [[0.1, 0.2, 0.1], [0.1, 0.2, 0.1]])
    ])
    def test_check_list_of_lists_must_convert_number_with_comma_to_float(self, param_data, expected_result):
        """Given a list of lists containing strings with comma separated decimals
        When check_list_of_lists is called
        Must pass returning the values converted to float"""
        assert DataHandler.check_list_of_lists(param_data) == expected_result

    @pytest.mark.parametrize('param_data, expected_result', [
        ([["1.234", 0.2, 0.1], [0.1, 0.2, 0.1]], [[1.234, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["123.E4", 0.2, 0.1], [0.1, 0.2, 0.1]], [[123.E4, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([[".1", 0.2, 0.1], [0.1, 0.2, 0.1]], [[0.1, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["6.523537535629999e-07", 0.2, 0.1], [0.1, 0.2, 0.1]], [[6.523537535629999e-07, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["6e777777", 0.2, 0.1], [0.1, 0.2, 0.1]], [[6e777777, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["1.797693e+308", 0.2, 0.1], [0.1, 0.2, 0.1]], [[1.797693e+308, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["0E0", 0.2, 0.1], [0.1, 0.2, 0.1]], [[0.0, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["+1e1", 0.2, 0.1], [0.1, 0.2, 0.1]], [[+1e1, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["  1.23  ", 0.2, 0.1], [0.1, 0.2, 0.1]], [[1.23, 0.2, 0.1], [0.1, 0.2, 0.1]]),
        ([["  \n    1.23    \n\n", 0.2, 0.1], [0.1, 0.2, 0.1]], [[1.23, 0.2, 0.1], [0.1, 0.2, 0.1]]),

    ])
    def test_check_list_of_lists_must_pass_when_value_is_conversible_to_float(self, param_data, expected_result):
        """Given a list of lists, with not float number value(s)
        when check _list_of_lists is called,
        Must create a list containing floats"""
        assert DataHandler.check_list_of_lists(param_data) == expected_result

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
        ])
    def test_replace_null_values(self, param_analytical_data, param_concentration_data, expected_analytical_result, expected_concentration_result):
        """Given data with null/none/undefined values,
        when replace_null_values is called,
        Must remove NoneType from both sets of lists
        """
        data_handler = DataHandler(param_analytical_data, param_concentration_data)
        clean_analytical_data, clean_concentration_data = data_handler.replace_null_values()
        assert clean_analytical_data == expected_analytical_result
        assert clean_concentration_data == expected_concentration_result
