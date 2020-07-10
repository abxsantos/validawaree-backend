from analytical_validation.exceptions import DataNotList, DataNotNumber, DataIsEmpty, AlphaNotValid, DirectionNotBoolean


class DixonQTest(object):
    """
     Check if the given data has outliers,
     if it has, returns the cleaned data
     set and the outlier values.

     Example:
         >>> data_set = [1.0, 1.0, 1.0, 2.0]
         >>> DixonQTest(data_set)
         >>> DixonQTest.check_data_for_outliers()
         >>> cleaned_data = [1.0, 1.0, 1.0]
         >>> outliers = [2.0]

     :param data: List containing a set of measured data points (float or int).
     :type data: list
     :param left: Q-test of minimum value in the ordered list if True.
     :type left: bool
     :param right: Q-test of maximum value in the ordered list if True.
     :type right: bool
     :param alpha: Significance (default value = 0.05)
     :type alpha: float
     :returns outliers: List containing all the outliers removed.
     :rtype outliers: list
     :returns cleaned_data: List without oulier values.
     :rtype cleaned_data: list
     :raises AnalyticalValueNotNumber: When a value in analytical data isn't a float.
     :raises AnalyticalValueNegative: When a value in analytical data is negative.
     :raises AlphaValueNotValid: When the alpha value is not a float.
     """

    def __init__(self, data, left=True, right=True, alpha=0.05):
        self.data = data
        self.left = left
        self.right = right
        self.alpha = alpha

        self.cleaned_data = data
        self.outliers = []

        self.valid_alpha = {0.01, 0.05, 0.10}
        self.QVALUES = {
            'alpha_10': [0.941, 0.765, 0.642, 0.56, 0.507, 0.468, 0.437,
                         0.412, 0.392, 0.376, 0.361, 0.349, 0.338, 0.329,
                         0.32, 0.313, 0.306, 0.3, 0.295, 0.29, 0.285, 0.281,
                         0.277, 0.273, 0.269, 0.266, 0.263, 0.26
                         ],
            'alpha_05': [0.97, 0.829, 0.71, 0.625, 0.568, 0.526, 0.493, 0.466,
                         0.444, 0.426, 0.41, 0.396, 0.384, 0.374, 0.365, 0.356,
                         0.349, 0.342, 0.337, 0.331, 0.326, 0.321, 0.317, 0.312,
                         0.308, 0.305, 0.301, 0.29
                         ],
            'alpha_01': [0.994, 0.926, 0.821, 0.74, 0.68, 0.634, 0.598, 0.568,
                         0.542, 0.522, 0.503, 0.488, 0.475, 0.463, 0.452, 0.442,
                         0.433, 0.425, 0.418, 0.411, 0.404, 0.399, 0.393, 0.388,
                         0.384, 0.38, 0.376, 0.372
                         ],
        }

        self.q_left = None
        self.q_right = None

    def check_dixon_q_test_input_data(self):
        if isinstance(self.left, bool) is False and isinstance(self.right, bool) is False:
            raise DirectionNotBoolean()
        if self.alpha not in self.valid_alpha:
            raise AlphaNotValid()
        if isinstance(self.data, list) is False:
            raise DataNotList()
        if not self.data:
            raise DataIsEmpty()
        if len(self.data) < 3 or len(self.data) > 30:
            return False
        if all(isinstance(value, (int, float)) for value in self.data) is False:
            raise DataNotNumber()
        return True

    @property
    def q_critical(self):
        """
        The dixon Q test critical value based on number of observations and the alpha value.
        :return q_critical: The critical Q value for the given data.
        :rtype q_critical: float
        """
        alpha_q_values = None
        if self.alpha == 0.10:
            alpha_q_values = self.QVALUES['alpha_10']
        elif self.alpha == 0.05:
            alpha_q_values = self.QVALUES['alpha_05']
        elif self.alpha == 0.01:
            alpha_q_values = self.QVALUES['alpha_01']
        return {n: q for n, q in zip(range(3, len(alpha_q_values) + 1), alpha_q_values)}[len(self.data)]

    @property
    def sorted_data(self):
        """
        Sorts the given data in an ascending order.
        :return sorted_data: Data sorted out in ascendind order.
        :rtype sorted_data: list
        """
        return sorted(self.data)

    @property
    def calculated_q_value(self):
        """
        Calculate the Q value for the suspected outliers.
        :return calculated_q_value: Calculated Q values.
        :rtype calculated_q_value: tuple(float, float)
        """
        q_left = None
        q_right = None
        if self.left:
            q_left = self.q_value_calculation(self.sorted_data[1], self.sorted_data[0])
        if self.right:
            q_right = self.q_value_calculation(self.sorted_data[-2], self.sorted_data[-1])
        return {'left': q_left, 'right': q_right}

    def q_value_calculation(self, value, reference):
        """
        Calculate the Q value for the suspected outliers.
        :return calculated_q_value: Calculated Q value.
        :rtype calculated_q_value: float
        """
        try:
            return round(abs((reference - value) / (self.sorted_data[-1] - self.sorted_data[0])), 3)
        except ZeroDivisionError:
            pass

    def remove_outliers(self):
        """
        Remove based on the left (minimum value) and right (greater value)
        Q calculated values, the outliers from data set.
        :return outliers: List containing outliers in the data set based on Dixon Q test
        :rtype outliers: list[list]
        :return cleaned_data: List containing the data set without the outliers.
        :rtype cleaned_data:list[list]
        """
        if self.calculated_q_value['left'] is None and self.calculated_q_value['right'] is None:
            return self.outliers, self.cleaned_data

        elif self.calculated_q_value['left'] == self.calculated_q_value['right']:
            return self.outliers, self.cleaned_data

        elif self.left is True and self.calculated_q_value['left'] > self.q_critical:
            self.outliers = [self.sorted_data[0]]
            self.cleaned_data.remove(self.outliers[0])

        elif self.right is True and self.calculated_q_value['right'] > self.q_critical:
            self.outliers = [self.sorted_data[-1]]
            self.cleaned_data.remove(self.outliers[0])

        return self.outliers, self.cleaned_data

    def check_data_for_outliers(self):
        if self.check_dixon_q_test_input_data() is True:
            return self.remove_outliers()
        else:
            return [], self.data
