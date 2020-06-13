import numpy as np
import scipy.stats as stats


class Linearity:
    def __init__(self, analytical_data, volume_of_samples, mass_of_samples, number_of_replicas, dilution_factor):
        self.analytical_data = analytical_data
        self.volume_of_samples = volume_of_samples
        self.mass_of_samples = mass_of_samples
        self.number_of_replicas = number_of_replicas
        self.dilution_factor = dilution_factor

    # Concentration = mass / volume in mg/mL
    def concentration_calculation(self):

        concentration_list = []
        # Organizing lists of concentrations
        for mass in self.mass_of_samples:
            initial_concentration = mass / self.volume_of_samples
            # print("The initial concentration is: {}".format(initial_concentration))
            concentration_set = []
            for factor in self.dilution_factor:
                concentration = initial_concentration / factor
                concentration_set.append(concentration)
            concentration_list.append(concentration_set)

        # Reorganizing the list to facilitate comparison of each calculated
        # concetration with its corresponding analytical value
        # Using map() + zip() to perform index list elements pairing

        concentration_data = list(map(list, zip(*concentration_list)))
        return concentration_data

    # Calculate the mean for each concentration data set
    def data_mean_calculation(self):
        data_mean = []
        for entries in self.analytical_data:
            mean = np.nanmean(entries)
            data_mean.append(mean)
        return (data_mean)

    # Calculate the STandard Deviation for each concentration data set
    def data_std_calculation(self):
        data_std = []
        for entries in self.analytical_data:
            std = np.nanstd(entries, ddof=1)
            data_std.append(std)
        return (data_std)

    # Flatten the concentration and analytical data lists as x and y axis
    def flatten_axis_data(self):
        concentration_data = self.concentration_calculation()
        analytical_data = self.analytical_data

        # Usefull snippet to flatten a list of arrays once
        def flatten(lst):
            return [x for y in lst for x in y]

        concentration_data_x_axis = flatten(concentration_data)
        analytical_data_y_axis = flatten(analytical_data)

        return concentration_data_x_axis, analytical_data_y_axis

    # Considering: y = m*x + b + e
    def linear_regression_coefficients(self):
        x,y = self.flatten_axis_data()
        slope, intercept, rvalue, pvalue, stderr = stats.linregress(x, y)
        '''
        Returns
        -------
        slope : float
            Slope of the regression line.
        intercept : float
            Intercept of the regression line.
        rvalue : float
            Correlation coefficient.
        pvalue : float
            Two-sided p-value for a hypothesis test whose null hypothesis is
            that the slope is zero, using Wald Test with t-distribution of
            the test statistic.
        stderr : float
            Standard error of the estimated gradient.
        '''
        return slope, intercept, rvalue, pvalue, stderr

    # TODO: Make ANOVA analysis of data

    # TODO: Verify if the slope IS significant at alpha = 5%

    # TODO: Verify if the intercept IS NOT significant at alpha = 5%

    # TODO: Verify if R² is above 0,990

    # TODO: Check homocedasticity with Breusch-Pagan test

    # TODO: ask for user alpha value input
    # Calculate the Grubbs critical value based on the number of replicas
    # (triplicate...) and alpha value (confidence level)
    def grubbs_critical_value_calculation(self, alpha):
        """Calculate the critical value with the formula given for example in
        https://en.wikipedia.org/wiki/Grubbs%27_test_for_outliers#Definition
        Args:
            ts (list or np.array): The timeseries to compute the critical value.
            alpha (float): The significance level.
        Returns:
            float: The critical value for this test.
        """
        t_dist = stats.t.ppf(1 - alpha / (2 * self.number_of_replicas), self.number_of_replicas - 2)
        numerator = (self.number_of_replicas - 1) * np.sqrt(np.square(t_dist))
        denominator = np.sqrt(self.number_of_replicas) * np.sqrt(self.number_of_replicas - 2 + np.square(t_dist))
        critical_value = numerator / denominator
        # print("Grubbs Critical Value: {} at a significance of".format(critical_value), alpha)
        return critical_value

    # Calculate the grubbs value for each item
    def data_grubbs_calculated(self):
        n = 0
        data_G_calc = []
        data_mean = self.data_mean_calculation()
        data_std = self.data_std_calculation()
        for data_set in self.analytical_data:
            index = 0
            G_calculated_set = []
            while index < len(data_set):
                G_calculated = abs(data_set[index] - data_mean[n]) / data_std[n]
                G_calculated_set.append(G_calculated)
                index = index + 1
            data_G_calc.append(G_calculated_set)
            n = n + 1
        return (data_G_calc)

    # TODO: Calculate de residues

    # TODO: Implement the Durbin-Watson test

if __name__ == '__main__':
    # Example of inputs
    analytical_data = [[0.188, 0.192, 0.203], [0.349, 0.346, 0.348], [0.489, 0.482, 0.492], [0.637, 0.641, 0.641],
                       [0.762, 0.768, 0.786], [0.931, 0.924, 0.925]]
    volume_of_samples = 50.00
    dilution_factor = [125.0, 62.5, 50.0, 35.71429, 31.25, 25.0]
    mass_of_samples = [50.0, 50.1, 50.8]
    number_of_replicas = 3

    test = Linearity(analytical_data, volume_of_samples, mass_of_samples, number_of_replicas, dilution_factor)
    #print(test.grubbs_critical_value_calculation(0.5))
    #print(test.concentration_calculation())
    slope, intercept, rvalue, pvalue, stderr = test.linear_regression_coefficients()

    print("The Slope is: {}".format(slope))
    print("The Intercept is: {}".format(intercept))
    print("The Correlation coefficient is: {}".format(rvalue))
    print("The Two-sided p-value is: {}".format(pvalue))
    print("The Standard error of estimated gradient is: {}".format(stderr))