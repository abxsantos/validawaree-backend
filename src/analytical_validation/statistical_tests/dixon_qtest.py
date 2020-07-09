from analytical_validation.exceptions import DataNotList, DataNotNumber, DataIsEmpty, AlphaNotValid, DirectionNotBoolean


class DixonQTest(object):
    """
     Check if the given data has outliers,
     if it has, returns the cleaned data
     set and the outlier values.

     Example:
         >>> data_set = [1.0, 1.0, 1.0, 2.0]
         >>> dixon_qtest(data_set)
         >>> cleaned_data = [1.0, 1.0, 1.0]
         >>> outliers = [2.0]

     :param data: List containing a set of measured data points (float or int).
     :type data: list
     :param left: Q-test of minimum value in the ordered list if True.
     :type left: bool
     :param right: Q-test of maximum value in the ordered list if True.
     :type left: bool
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

        self.cleaned_data = []
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
        self.q_min = ''
        self.q_max = ''
        self.q_mindiff = ''
        self.q_maxdiff = ''

    def check_dixon_q_test_input_data(self):
        if isinstance(self.left, bool) is False or isinstance(self.right, bool) is False:
            raise DirectionNotBoolean()
        if self.alpha not in self.valid_alpha:
            raise AlphaNotValid()
        if isinstance(self.data, list) is False:
            raise DataNotList()
        if not self.data:
            raise DataIsEmpty()
        if len(self.data) < 3 or len(self.data) > 28:
            self.cleaned_data = self.data
            self.outliers = []
        if all(isinstance(value, (int, float)) for value in self.data) is False:
            raise DataNotNumber()

    @property
    def q_values(self):
        if self.alpha == 0.10:
            QVALUES = self.QVALUES['alpha_10']
        elif self.alpha == 0.05:
            QVALUES = self.QVALUES['alpha_05']
        elif self.alpha == 0.01:
            QVALUES = self.QVALUES['alpha_01']

        return {n: q for n, q in zip(range(3, len(QVALUES) + 1), QVALUES)}

    @property
    def sorted_data(self):
        return sorted(self.data)

    def check_if_one_or_two_sided_test(self):
        if self.left:
            self.q_min = (self.sorted_data[1] - self.sorted_data[0])
            try:
                self.q_min /= (self.sorted_data[-1] - self.sorted_data[0])
            except ZeroDivisionError:
                pass
            self.q_mindiff = (self.q_min - self.q_values[len(self.data)], self.sorted_data[0])
        if self.right:
            self.q_max = abs((self.sorted_data[-2] - self.sorted_data[-1]))
            try:
                self.q_max /= abs((self.sorted_data[0] - self.sorted_data[-1]))
            except ZeroDivisionError:
                pass
            self.q_maxdiff = (self.q_max - self.q_values[len(self.data)], self.sorted_data[-1])

    def remove_outliers(self):
        self.cleaned_data = self.data
        if not self.q_mindiff[0] > 0 and not self.q_maxdiff[0] > 0:
            return self.outliers, self.cleaned_data
        elif self.q_mindiff[0] == self.q_maxdiff[0]:
            outliers = [self.q_mindiff[1], self.q_maxdiff[1]]
            (self.cleaned_data.remove(outliers[0])).remove(outliers[1])
        elif self.q_mindiff[0] > self.q_maxdiff[0]:
            self.outliers = [self.q_mindiff[1]]
            self.cleaned_data.remove(self.outliers[0])
        else:
            self.outliers = [self.q_maxdiff[1]]
            self.cleaned_data.remove(self.outliers[0])

    def check_data_for_outliers(self):
        self.check_dixon_q_test_input_data()
        self.check_if_one_or_two_sided_test()
        self.remove_outliers()
        return self.outliers, self.cleaned_data

    # q_dict = {n: q for n, q in zip(range(3, len(q_value) + 1), q_value)}
    # sdata = sorted(data)
    # q_mindiff, q_maxdiff = (0, 0), (0, 0)
    # cleaned_data = data
    # outliers = []
    # if left:
    #     q_min = (sdata[1] - sdata[0])
    #     try:
    #         q_min /= (sdata[-1] - sdata[0])
    #     except ZeroDivisionError:
    #         pass
    #     q_mindiff = (q_min - q_dict[len(data)], sdata[0])
    # if right:
    #     q_max = abs((sdata[-2] - sdata[-1]))
    #     try:
    #         q_max /= abs((sdata[0] - sdata[-1]))
    #     except ZeroDivisionError:
    #         pass
    #     q_maxdiff = (q_max - q_dict[len(data)], sdata[-1])
    # if not q_mindiff[0] > 0 and not q_maxdiff[0] > 0:
    #     return outliers, cleaned_data
    # elif q_mindiff[0] == q_maxdiff[0]:
    #     outliers = [q_mindiff[1], q_maxdiff[1]]
    #     (cleaned_data.remove(outliers[0])).remove(outliers[1])
    # elif q_mindiff[0] > q_maxdiff[0]:
    #     outliers = [q_mindiff[1]]
    #     cleaned_data.remove(outliers[0])
    # else:
    #     outliers = [q_maxdiff[1]]
    #     cleaned_data.remove(outliers[0])
    # return outliers, cleaned_data
