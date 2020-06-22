class LinearityValidator(object):
    """

    Example:
        >>> l = LinearityValidator(samples=[])
        >>> l.validate()
        False

        >>> l = LinearityValidator(samples=[1, 2, 3])
        >>> l.validate()
        True
    """
    def __init__(self):
        self.slope_pvalue = None

    def validate(self):
        """Validate the given data.

        :return: True if data is valid; otherwise, False.
        :rtype: bool
        """
        pass

    def ordinary_least_squares_linear_regression(self):
        """Fit the data using the ordinary least squares method of Linear Regression.

        :return: Returns slope_pvalue, intercept_pvalue, r_squared, slope, intercept, stderr
        """
        pass
