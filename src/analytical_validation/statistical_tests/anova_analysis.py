import numpy
import scipy.stats as stats

from analytical_validation.exceptions import AnalyticalValueNegative, AverageValueNotNumber, AnalyticalValueNotNumber, \
    AverageValueNegative


class AnovaValidator(object):
    """Determine the influence of independent variables (concentration) have on the dependant variables
    (analytical signal) in a regression study.

    The results of anova analysis consists of:

    Sum of squares between groups (SSB) which is the sum of the squared differences between each
                            treatment (or group) mean and the overall mean.

    Sum of squares within groups (SSE) which is the sum of the squared differences between each individual
                            value and its group mean.
    Total sum of squared errors (SST) which is is the variability of the data

    Treatment degrees of freedom (dfb) number of samples (k) - 1

    Error degrees of freedom (dfe) n (number of data points) - k

    Total degrees of freedom (dft) n -1

    Mean squares between treatments (MSB) which is the SSB / dfb

    Mean squares of residues (MSE) which is the SSE / dfe

    F-ratio which is the statistic which measures if the means of
    different samples are significantly different or not.
    If F-ratio > Fcrit, the null hyphothesis is rejected and the assumption
    of one of samples has statistically different mean can be accepted.

    Example:
        >>> anova = AnovaValidator(samples_data=[[1,2,3],[4,5,6]], samples_averages=[2,5])
        >>> anova.anova_degrees_of_freedom()
        >>> anova_sum_of_squares()
    """

    def __init__(self, analytical_data, averages_data):
        """
        Validate the linearity of the method.
        :param analytical_data: List of lists containing all measured analytical signal separated in sets.
        :type analytical_data: list
        :param averages_data: List containing the average for each set of analytical signal with the same concentration
        :type averages_data: list
        """
        self.analytical_data = analytical_data
        self.averages_data = averages_data

        self.degrees_of_freedom_btwn_treatments = 0
        self.total_degrees_of_freedom = 0
        self.residual_degrees_of_freedom = 0

        self.sum_of_squares_total = 0
        self.sum_of_squares_residual = 0
        self.sum_of_squares_btwn_treatments = 0

        self.mean_squares_btwn_treatments = 0
        self.mean_squares_of_residues = 0

        self.f_anova = None
        self.p_anova = None

        # Check for values != float or negative
        for data_set in self.analytical_data:
            if not all(isinstance(value, float) for value in data_set):
                raise AnalyticalValueNotNumber()
        if not all(isinstance(value, float) for value in self.averages_data):
            raise AverageValueNotNumber()
        for data_set in self.analytical_data:
            if not all(value > 0 for value in data_set):
                raise AnalyticalValueNegative()
        if not all(value > 0 for value in self.averages_data):
            raise AverageValueNegative()

    def anova_degrees_of_freedom(self):
        """Degrees of freedom are related to sample size (n-1).
        If the df increases, it also stands that the sample
        size is increasing; the graph of the t-distribution
        will have skinnier tails, pushing the critical value
        towards the mean."""

        # Degrees_of freedom between treatments
        self.degrees_of_freedom_btwn_treatments = len(self.analytical_data) - 1
        flat_analytical_data = numpy.hstack(self.analytical_data)
        #                   Within-treatments
        # Degrees of freedom population error variance
        self.residual_degrees_of_freedom = flat_analytical_data.shape[0] - len(self.analytical_data)
        # Degrees of freedom population dep. variable variance
        self.total_degrees_of_freedom = flat_analytical_data.shape[0] - 1

    def anova_sum_of_squares(self):
        """It is the sum of the squares of the deviations of all
        the observations, yi, from their mean, . In the context
        of ANOVA, this quantity is called the total sum of squares
        (abbreviated SST) because it relates to the total
        variance of the observations.
        For the perfect model, the model sum of squares, SSR, equals
        the total sum of squares, SST, because all estimated values
        obtained using the model, , will equal the corresponding
        observations, yi."""

        # Residual/Error sum of squares
        index = 0
        self.sum_of_squares_residual = 0
        while index < len(self.analytical_data):
            for data_set in self.analytical_data:
                for value in data_set:
                    self.sum_of_squares_residual = self.sum_of_squares_residual + (
                            (value - self.averages_data[index]) ** 2)
                index = index + 1
        # Overall average
        overall_analytical_average = sum(numpy.hstack(self.analytical_data)) / len(numpy.hstack(self.analytical_data))
        # Sum of squares between treatments
        index = 0
        for value in self.averages_data:
            self.sum_of_squares_btwn_treatments = self.sum_of_squares_btwn_treatments + \
                                                  len(self.analytical_data[index]) * (
                                                          (value - overall_analytical_average) ** 2)
            index = index + 1
        # Total Sum of squares
        self.sum_of_squares_total = self.sum_of_squares_btwn_treatments + self.sum_of_squares_residual

    def anova_mean_squares(self):
        self.mean_squares_btwn_treatments = self.sum_of_squares_btwn_treatments / self.degrees_of_freedom_btwn_treatments
        self.mean_squares_of_residues = self.sum_of_squares_residual / self.residual_degrees_of_freedom

    def anova_f_ratio(self):
        """F ratio is the ratio of two mean square values.
        If the null hypothesis is true, you expect F to
        have a value close to 1.0 most of the time.
        A large F ratio means that the variation among
        group means is more than you'd expect to see by chance."""
        self.f_anova, self.p_anova = stats.f_oneway(*self.analytical_data)
