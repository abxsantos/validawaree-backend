import pytest

from analytical_validation.exceptions import DataNotNumber, DataIsEmpty, \
    DataNotList, AlphaNotValid, DirectionNotBoolean
from analytical_validation.statistical_tests.dixon_qtest import dixon_qtest


class TestDixonQTest(object):
    @pytest.mark.parametrize("param_alpha", [
        10, 0.049, 0.051, 0.11, 0.09, 0.011, -1, True, "Not Number", None
    ])
    def test_qtest_must_raise_exception_when_alpha_not_valid(self, param_alpha):
        """Given a alpha value
        When q_test is called
        Should raise an exception"""
        # Arrange
        data = [1, 1, 1]
        # Act &  Assert
        with pytest.raises(AlphaNotValid):
            dixon_qtest(data, alpha=param_alpha)

    def test_qtest_must_raise_exception_when_left_not_bool(self):
        """Given non bool left value
        when q-test is called
        should raise exception"""
        # Arrange
        data = [0.100, 0.150, 0.200]
        left = "NOT BOOL"
        # Act & Assert
        with pytest.raises(DirectionNotBoolean):
            dixon_qtest(data, left=left)

    def test_qtest_must_raise_exception_when_right_not_bool(self):
        """Given non bool left value
        when q-test is called
        should raise exception"""
        # Arrange
        data = [0.100, 0.150, 0.200]
        right = "NOT BOOL"
        # Act &  Assert
        with pytest.raises(DirectionNotBoolean):
            dixon_qtest(data, right=right)

    @pytest.mark.parametrize('param_data, expected_result', [
        ("Not List", DataNotList), ({"key": "value"}, DataNotList), ((0, 1, 2, 3, 4), DataNotList), (True, DataNotList),
        (0.05, DataNotList), (10, DataNotList), ([], DataIsEmpty), (["String", 1, 2, 3, 2], DataNotNumber),
        ([True, 1, 2, 3, 2], DataNotNumber), ([[], 1, 2, 3, 2], DataNotNumber)
    ])
    def test_qtest_must_raise_exception(self, param_data, expected_result):
        """Given data that's not
        a list of lists
        when q_test is called
        should raise exception"""
        """Given data that's not
        a list of lists
        when q_test is called
        should raise exception"""
        """Given data with not float value
        when q_test is called
        should raise an exception"""
        # Arrange
        data = "Not list"
        # Act &  Assert
        with pytest.raises(DataNotList):
            dixon_qtest(data)

    def test_qtest_must_return_list_of_numbers_when_data_contains_outliers(self):
        """Given data with outliers
        when q_test is called
        should return list of lists containing numbers"""
        # Arrange
        data = [0.100, 0.150, 0.200, 0.100, 0.200, 10.0]
        # Act
        outliers, cleaned_data = dixon_qtest(data)
        # Assert
        assert outliers == [10.0]
        assert cleaned_data == [0.100, 0.150, 0.200, 0.100, 0.200]

    def test_qtest_must_return_empty_list_when_no_outliers(self):
        """Given data with no outliers
        when q_test is called
        should return an empty list"""
        # Arrange
        data = [0.100, 0.150, 0.200]
        # Act
        outliers, cleaned_data = dixon_qtest(data)
        # Assert
        assert outliers == []

    def test_qtest_must_pass_when_number_of_data_points_is_less_than_3(self):
        """Given data with less than 3
        When q_test is called
        should pass returning the not cleaned data"""
        # Arrange
        data = [1, 1]
        # Act
        outliers, cleaned_data = dixon_qtest(data)
        # Assert
        assert cleaned_data == data
        assert outliers == []

    def test_qtest_must_pass_when_number_of_data_points_is_greater_than_29(self):
        """Given data with more than 28 numbers
        When q_test is called
        should pass returning the not cleaned data"""
        # Arrange
        data = list(range(1, 29))
        # Act
        outliers, cleaned_data = dixon_qtest(data)
        # Assert
        assert cleaned_data == data
        assert outliers == []

    def test_qtest_must_pass_when_float_analytical_data_values(self):
        """Given float analytical data,
        when q_test is called
        should pass the test"""
        # Arrange
        data = [0.100, 0.150, 0.200]
        # Act
        outliers, cleaned_data = dixon_qtest(data)
        # Assert
        assert outliers == []
        assert cleaned_data == [0.100, 0.150, 0.200]
