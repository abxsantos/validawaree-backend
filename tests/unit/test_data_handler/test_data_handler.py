import pytest

from analytical_validation.data_handler.data_handler import handle_data_from_react
from analytical_validation.exceptions import DataNotList, DataNotListOfLists, DataSetNotSymmetric, \
    AnalyticalValueNotNumber, ConcentrationValueNotNumber, ConcentrationValueNegative, AnalyticalValueNegative


class TestDataHandler(object):
    # check for data inconsistency
    #  the analytical data must be completely symmetric with concentration data
    #  check if it's a list
    #  check if its a list containing lists (set of data)
    #  check if the number of set of data is symmetric
    #       check if the number of values in the data sets are symmetric
    #       check if values are numbers and convert to float
    #       check if there are invalid numbers (negative, undefined)
    #       clean up non real float values

    def test_data_handler(self):
        analytical_data = [[1.0, 1.0, 10.0], [2.0, 6.0, 2.0]]
        concentration_data = [[1.0, 2.0, 3.0], [8.0, 9.0, 10.0]]
        handle_data_from_react(analytical_data, concentration_data)
        assert handle_data_from_react.handled_analytical_data == analytical_data
        assert handle_data_from_react.handled_concentration_data == concentration_data

    @pytest.mark.parametrize('param_analytical_data', [
        ("STR", -1, 10, 0.09, True, {}, (0, 1))
    ])
    def test_data_handler_must_raise_an_exception_when_data_is_not_a_list(self, param_analytical_data):
        concentration_data = [[1.0, 1.0, 10.0], [2.0, 6.0, 2.0]]
        with pytest.raises(DataNotList):
            handle_data_from_react(param_analytical_data, concentration_data)

    @pytest.mark.parametrize('param_concentration_data', [
        ("STR", -1, 10, 0.09, True, {}, (0, 1))
    ])
    def test_data_handler_must_raise_an_exception_when_concentration_data_is_not_a_list(self, param_concentration_data):
        analytical_data = [[1.0, 1.0, 10.0], [2.0, 6.0, 2.0]]
        with pytest.raises(DataNotList):
            handle_data_from_react(analytical_data, param_concentration_data)

    @pytest.mark.parametrize('param_analytical_data', [
        (["STR"], [-1], [10], [0.09], [True], [{}], [(0, 1)])
    ])
    def test_data_handler_must_raise_an_exception_when_concentration_data_set_is_not_a_list(self,
                                                                                            param_analytical_data):
        concentration_data = [[1.0, 1.0, 10.0], [2.0, 6.0, 2.0]]
        with pytest.raises(DataNotListOfLists):
            handle_data_from_react(param_analytical_data, concentration_data)

    @pytest.mark.parametrize('param_concentration_data', [
        (["STR"], [-1], [10], [0.09], [True], [{}], [(0, 1)])
    ])
    def test_data_handler_must_raise_an_exception_when_concentration_data_set_is_not_a_list(self,
                                                                                            param_concentration_data):
        analytical_data = [[1.0, 1.0, 10.0], [2.0, 6.0, 2.0]]
        with pytest.raises(DataNotListOfLists):
            handle_data_from_react(analytical_data, param_concentration_data)

    @pytest.mark.parametrize('param_analytical_data', [
        ([[1.0, 1.0, 10.0], [2.0, 6.0]]),
        ([[1.0, 1.0, 10.0], [2.0, 6.0, 2.0, 3.0]]),
        ([[2.0, 6.0], [1.0, 1.0, 10.0]]),
        ([[2.0, 6.0, 2.0, 3.0], [1.0, 1.0, 10.0]]),
        ([[1.0, 1.0, 10.0], [1.0, 1.0, 10.0], [1.0, 1.0, 10.0]]),
    ])
    def test_data_handler_must_raise_an_exception_when_analytical_data_set_not_symmetric(self, param_analytical_data):
        concentration_data = [[1.0, 1.0, 10.0], [2.0, 6.0, 2.0]]
        with pytest.raises(DataSetNotSymmetric):
            handle_data_from_react(param_analytical_data, concentration_data)

    @pytest.mark.parametrize('param_concentration_data', [
        ([[1.0, 1.0, 10.0], [2.0, 6.0]]),
        ([[1.0, 1.0, 10.0], [2.0, 6.0, 2.0, 3.0]]),
        ([[2.0, 6.0], [1.0, 1.0, 10.0]]),
        ([[2.0, 6.0, 2.0, 3.0], [1.0, 1.0, 10.0]]),
        ([[1.0, 1.0, 10.0], [1.0, 1.0, 10.0], [1.0, 1.0, 10.0]])
    ])
    def test_data_handler_must_raise_an_exception_when_analytical_data_set_not_symmetric(self,
                                                                                         param_concentration_data):
        analytical_data = [[1.0, 1.0, 10.0], [2.0, 6.0, 2.0]]
        with pytest.raises(DataSetNotSymmetric):
            handle_data_from_react(analytical_data, param_concentration_data)

    @pytest.mark.parametrize('param_analytical_data', [
        ([['', 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([['NaNananana BATMAN', 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["1,234", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["NULL", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([[",1", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["123.EE4", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["12.34.56", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([[True, 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([[(0, 1), 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([[[0.1], 1.0, 10.0], [2.0, 6.0, 2.0]]),
    ])
    def test_data_handler_must_raise_an_exception_when_a_analytical_value_not_float(self, param_analytical_data):
        concentration_data = [[1.0, 1.0, 10.0], [2.0, 6.0, 2.0]]
        with pytest.raises(AnalyticalValueNotNumber):
            handle_data_from_react(param_analytical_data, concentration_data)

    @pytest.mark.parametrize('param_concentration_data', [
        ([['', 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([['NaNananana BATMAN', 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["1,234", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["NULL", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([[",1", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["123.EE4", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["12.34.56", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([[True, 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([[12e3, 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([[(0, 1), 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([[[0.1], 1.0, 10.0], [2.0, 6.0, 2.0]]),
    ])
    def test_data_handler_must_raise_an_exception_when_a_analytical_value_not_float(self, param_concentration_data):
        analytical_data = [[1.0, 1.0, 10.0], [2.0, 6.0, 2.0]]
        with pytest.raises(ConcentrationValueNotNumber):
            handle_data_from_react(analytical_data, param_concentration_data)

    @pytest.mark.parametrize('param_analytical_data', [
        ([['1234567', 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([['NaN', 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["1.234", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["123.E4", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([[".1", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["6.523537535629999e-07", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["6e777777", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["-iNF", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["1.797693e+308", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["infinity", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["0E0", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["+1e1", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["  1.23  ", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["  \n  \t   1.23    \n\t\n", 1.0, 10.0], [2.0, 6.0, 2.0]]),

    ])
    def test_data_must_convert_analytical_values_if_possible(self, param_analytical_data):
        concentration_data = [[1.0, 1.0, 10.0], [2.0, 6.0, 2.0]]
        handle_data_from_react(param_analytical_data, concentration_data)
        assert handle_data_from_react.is_valid_data

    @pytest.mark.parametrize('param_concentration_data', [
        ([['1234567', 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([['NaN', 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["1.234", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["123.E4", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([[".1", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["6.523537535629999e-07", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["6e777777", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["-iNF", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["1.797693e+308", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["infinity", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["0E0", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["+1e1", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["  1.23  ", 1.0, 10.0], [2.0, 6.0, 2.0]]),
        ([["  \n  \t   1.23    \n\t\n", 1.0, 10.0], [2.0, 6.0, 2.0]]),

    ])
    def test_data_must_convert_concentration_values_if_possible(self, param_concentration_data):
        analytical_data = [[1.0, 1.0, 10.0], [2.0, 6.0, 2.0]]
        handle_data_from_react(analytical_data, param_concentration_data)
        assert handle_data_from_react.is_valid_data

    def test_data_must_raise_an_exception_when_concentration_data_has_negative_values(self):
        analytical_data = [[1.0, 1.0, 10.0], [2.0, 6.0, 2.0]]
        concentration_data = [[-1.0, 1.0, 10.0], [2.0, 6.0, 2.0]]
        with pytest.raises(ConcentrationValueNegative):
            handle_data_from_react(analytical_data, concentration_data)

    def test_data_must_raise_an_exception_when_analytical_data_has_negative_values(self):
        analytical_data = [[-1.0, 1.0, 10.0], [2.0, 6.0, 2.0]]
        concentration_data = [[1.0, 1.0, 10.0], [2.0, 6.0, 2.0]]
        with pytest.raises(AnalyticalValueNegative):
            handle_data_from_react(analytical_data, concentration_data)

    @pytest.mark.parametrize('param_analytical_data, param_concentration_data', [
        ([[1.0, 1.0, 10.0], [2.0, 6.0, 2.0]], [[1.0, None, 10.0], [2.0, 6.0, 2.0]]),
        ([[1.0, None, 10.0], [2.0, 6.0, 2.0]], [[1.0, 3.0, 10.0], [2.0, 6.0, 2.0]])
    ])
    def test_data_must_clean_nan(self, param_analytical_data, param_concentration_data):
        handle_data_from_react(param_analytical_data, param_concentration_data)
        assert handle_data_from_react.handled_analytical_data == [[1.0, 10.0], [2.0, 6.0, 2.0]]
        assert handle_data_from_react.handled_concentration_data == [[1.0, 10.0], [2.0, 6.0, 2.0]]
