import pytest

from analytical_validation.exceptions import DataNotNumber, DataIsEmpty, \
    DataNotList, AlphaNotValid, DirectionNotBoolean

from analytical_validation.statistical_tests.dixon_qtest import DixonQTest


class TestDixonQTest(object):

    @pytest.mark.parametrize("param_alpha", [
        10, 0.049, 0.051, 0.11, 0.09, 0.011, -1, True, "Not Number", None
    ])
    def test_qtest_must_raise_exception_when_alpha_not_valid(self, param_alpha):
        """Given a alpha value
        When check_dixon_q_test_input_data is called
        Should raise an exception"""
        # Arrange
        data = [1, 1, 1]
        dixon_qtest = DixonQTest(data, alpha=param_alpha)
        # Act &  Assert
        with pytest.raises(AlphaNotValid):
            dixon_qtest.check_dixon_q_test_input_data()

    @pytest.mark.parametrize("param_left", [0, "", 0.1, "STRING", [' '], (1, 0), -1, {'key': 'value'}])
    @pytest.mark.parametrize("param_right", [0, "", 0.1, "STRING", [' '], (1, 0), -1, {'key': 'value'}])
    def test_qtest_must_raise_exception_when_left_not_bool(self, param_left, param_right):
        """Given non bool left or right value
        when check_dixon_q_test_input_data is called
        should raise exception"""
        # Arrange
        data = [0.100, 0.150, 0.200]
        dixon_qtest = DixonQTest(data, right=param_right, left=param_left)
        # Act & Assert
        with pytest.raises(DirectionNotBoolean):
            dixon_qtest.check_dixon_q_test_input_data()

    @pytest.mark.parametrize('param_data, expected_result', [
        ("Not List", DataNotList),
        ({"key": "value"}, DataNotList),
        ((0, 1, 2, 3, 4), DataNotList),
        (True, DataNotList),
        (0.05, DataNotList),
        (10, DataNotList),
        ([], DataIsEmpty),
        (["String", 1, 2, 3, 2], DataNotNumber),
        ([[], 1, 2, 3, 2], DataNotNumber)
    ])
    def test_qtest_must_raise_exception(self, param_data, expected_result):
        """Given data that's not
        a list of lists
        when check_dixon_q_test_input_data is called
        should raise exception"""
        """Given data that's not
        a list of lists
        when check_dixon_q_test_input_data is called
        should raise exception"""
        """Given data with not float value
        when check_dixon_q_test_input_data is called
        should raise an exception"""
        # Arrange
        # Act &  Assert
        dixon_qtest = DixonQTest(param_data)
        with pytest.raises(expected_result):
            dixon_qtest.check_dixon_q_test_input_data()

    @pytest.mark.parametrize(
        'param_data, expected_outliers, expected_cleaned_data, param_alpha, param_left, param_right', [
            ([0.100, 0.150, 0.200, 0.100, 0.200, 10.0], [10.0], [0.100, 0.150, 0.200, 0.100, 0.200], 0.05, True, True),
            ([0.142, 0.153, 0.135, 0.002, 0.175], [0.002], [0.142, 0.153, 0.135, 0.175], 0.05, True, True),
            ([0.542, 0.153, 0.135, 0.002, 0.175], [], [0.542, 0.153, 0.135, 0.002, 0.175], 0.05, True, True),
            ([0.542, 0.153, 0.135, 0.002, 0.175], [0.542], [0.153, 0.135, 0.002, 0.175], 0.10, True, True),
            ([0.142, 0.153, 0.135, 0.002, 0.175, 0.542], [0.542], [0.142, 0.153, 0.135, 0.002, 0.175], 0.05, False,
             True),
            ([0.142, 0.153, 0.135, 0.002, 0.175], [0.002], [0.142, 0.153, 0.135, 0.175], 0.05, True, False),
        ])
    def test_qtest_must_return_list_of_numbers_when_data_contains_outliers(self, param_data, expected_outliers,
                                                                           expected_cleaned_data, param_alpha,
                                                                           param_left, param_right):
        """Given data with and without outliers
        When check_data_for_outliers is called
        should return list of lists containing the expected result numbers"""
        # Arrange
        dixon_qtest = DixonQTest(param_data, alpha=param_alpha, left=param_left, right=param_right)
        # Act
        outliers, cleaned_data = dixon_qtest.check_data_for_outliers()
        # Assert
        assert outliers == expected_outliers
        assert cleaned_data == expected_cleaned_data

    @pytest.mark.parametrize('param_data', [
        [1, 1], list(range(1, 31))
    ])
    def test_qtest_must_pass_when_number_of_data_points_is_less_than_3(self, param_data):
        """Given data with less than 3 or more than 30
        When check_data_for_outliers is called
        Should not check data for outliers"""
        # Arrange
        dixon_qtest = DixonQTest(param_data)
        # Act
        outliers, cleaned_data = dixon_qtest.check_data_for_outliers()
        # Assert
        assert cleaned_data == param_data
        assert outliers == []
