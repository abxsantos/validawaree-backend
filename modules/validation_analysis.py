import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
import statsmodels.stats.api as sms
from statsmodels.stats.stattools import durbin_watson

# TODO: refactor this spaghetti!

class Linearity:
    def __init__(self, analytical_data, volume_of_samples, mass_of_samples,
                       number_of_replicas, dilution_factor, alpha):
        self.analytical_data = analytical_data
        self.volume_of_samples = volume_of_samples
        self.mass_of_samples = mass_of_samples
        self.number_of_replicas = number_of_replicas
        self.dilution_factor = dilution_factor
        self.alpha = alpha


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
        # concentration with its corresponding analytical value
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
        self.analytical_data

        # Usefull snippet to flatten a list of arrays once
        def flatten(lst):
            return [x for y in lst for x in y]

        concentration_data_x_axis = flatten(concentration_data)
        analytical_data_y_axis = flatten(self.analytical_data)

        return concentration_data_x_axis, analytical_data_y_axis

    # Considering: y = slope*x + intercept + stderr
    def ordinary_least_squares_linear_regression(self):

        x, y = self.flatten_axis_data()
        X = sm.add_constant(x)
        model = sm.OLS(y, X)
        fitted_result = model.fit()

        #summary = results.summary(alpha=self.alpha, title="Ordinary Least Square Results")
        #print(summary)

        # Retrieve some parameters
        slope_pvalue = fitted_result.pvalues[1]
        intercept_pvalue = fitted_result.pvalues[0]
        r_squared = fitted_result.rsquared

        # Check the hypothesis
        # H0: a = 0
        # H1: a != 0
        # Consider P>|t| as your p-value

        # p-value < 0.05 the slope is != 0
        # if slope_pvalue < self.alpha:
        #     print("The slope is significative at 0.05. Can be considered != 0\nIt's p-value is: {}\n".format(slope_pvalue))
        #     # p-value > 0.05 the intercept = 0
        #     if intercept_pvalue > self.alpha:
        #         print("The intercept is NOT significative at 0.05. Can be considered = 0\nIt's p-value is: {}\n".format(intercept_pvalue))
        #         # Minimum value of R² defined by ANVISA
        #         if r_squared >= 0.990:
        #             print("The R² is: {}".format(r_squared))
        #     else:
        #         print("The intercept is significative at 0.05. Can be considered != 0\nIt's p-value is: {}\n".format(intercept_pvalue))
        # else:
        #     print("The slope is NOT significative at 0.05. Can be considered = 0\nIt's p-value is: {}\n".format(slope_pvalue))

        # TODO: retrieve only if the conditions above are accepted?
        # Retrieve the other parameters.
        slope = fitted_result.params[0]
        intercept = fitted_result.params[1]
        stderr = fitted_result.bse[1]

        # TODO: Deal with heteroskedastic, removing outliers or using Weighted Least Squares Regression
        # Run the Breusch-Pagan test to check homoskedasticity
        # If the (p-value) > 0.05, the method is homoskedastic, else is heteroskedastic
        breusch_pagan_pvalue = self.breusch_pagan_test(fitted_result)

        # Receive the residues from fitted model
        residues = fitted_result.resid

        # TODO: Implement another correlation test for double checking
        # Durbin-Watson Correlation test
        """The closer to 0 the statistic, the 
        more evidence for positive serial correlation.
        The closer to 4, the more evidence for negative 
        serial correlation."""
        durbin_watson_value = durbin_watson(residues)

        return slope, intercept, stderr, slope_pvalue, intercept_pvalue, r_squared, \
               breusch_pagan_pvalue, residues, durbin_watson_value

    # ANOVA test
    def anova_analysis(self):

        anova_set = {}
        index = 0
        while index < 3:
            data_set = []
            for data in self.analytical_data:
                data_set.append(data[index])
            anova_set['sample{}'.format(index + 1)] = data_set
            index = index + 1

        f_anova, p_anova = stats.f_oneway(*anova_set.values())

        # TODO: Try calculating ANOVA without using sklearn, or refitting the data
        x, y = self.flatten_axis_data()
        x = np.array(x)[:, np.newaxis]
        y = np.array(y)[:, np.newaxis]
        reg = LinearRegression()

        degrees_of_freedom_regression = 1
        ## degrees of freedom population dep. variable variance
        degrees_of_freedom = x.shape[0] - 1
        ## degrees of freedom population error variance
        degrees_of_freedom_residual = x.shape[0] - 2

        # Total sum of squared errors (actual vs avg(actual))
        # SST
        avg_y = np.mean(y)
        squared_errors = (y - avg_y) ** 2
        sum_of_squares_total = np.sum(squared_errors)

        # Sum of Squares Residual (SSR)
        data_mean = self.data_mean_calculation()
        sum_of_squares_residual = 0.0
        for average in data_mean:
           sum_of_squares_residual = sum_of_squares_residual + ((avg_y - average)**2)

        # Sum of Squares in Regression
        sum_of_squares_regression = sum_of_squares_residual + sum_of_squares_total

        # Regression mean square
        regression_mean_square =  sum_of_squares_regression

        # Residual mean square
        residual_mean_square = sum_of_squares_residual / degrees_of_freedom_residual

        # print(sum_of_squares_regression)
        # print(sum_of_squares_residual)
        # print(sum_of_squares_total)
        # print(degrees_of_freedom_regression)
        # print(degrees_of_freedom_residual)
        # print(degrees_of_freedom)
        # print(regression_mean_square)
        # print(residual_mean_square)

        return degrees_of_freedom_regression, sum_of_squares_regression, regression_mean_square, \
               degrees_of_freedom_residual, sum_of_squares_residual, residual_mean_square, \
               sum_of_squares_total, degrees_of_freedom, f_anova, p_anova

    # Test the Breusch-Pagan homokedasticity
    def breusch_pagan_test(self, fitted_result):

        # Calculate the redisues based on fitted model of linear regression
        breusch_pagan_test = sms.het_breuschpagan(fitted_result.resid, fitted_result.model.exog)
        # labels = ["LM Statistic", "LM-Test p-value", "F-Statistic", "F-Test p-value"]
        breusch_pagan_pvalue = breusch_pagan_test[3]

        # Check Heteroskedasticity
        if breusch_pagan_pvalue < self.alpha:
            print("Using the Breusch-Pagan test, {} (p-value) < 0.05 and thus this method is heteroskedastic.".format(breusch_pagan_pvalue))
        else:
            print("Using the Breusch-Pagan test, {} (p-value) > 0.05 and thus this method is homoskedastic.".format(breusch_pagan_pvalue))

        return breusch_pagan_pvalue

    # TODO: ask for user alpha value input

    # TODO: Deal with removing outliers via Grubbs test

    # Calculate the Grubbs critical value based on the number of replicas
    # (triplicate...) and alpha value (confidence level)
    def grubbs_critical_value_calculation(self):
        """Calculate the critical value with the formula given for example in
        https://en.wikipedia.org/wiki/Grubbs%27_test_for_outliers#Definition
        Args:
            ts (list or np.array): The timeseries to compute the critical value.
            alpha (float): The significance level.
        Returns:
            float: The critical value for this test.
        """
        t_dist = stats.t.ppf(1 - self.alpha / (2 * self.number_of_replicas), self.number_of_replicas - 2)
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

if __name__ == '__main__':
    # Example of inputs
    analytical_data = [[0.188, 0.192, 0.203], [0.349, 0.346, 0.348], [0.489, 0.482, 0.492], [0.637, 0.641, 0.641],
                       [0.762, 0.768, 0.786], [0.931, 0.924, 0.925]]
    volume_of_samples = 50.00
    dilution_factor = [125.0, 62.5, 50.0, 35.71429, 31.25, 25.0]
    mass_of_samples = [50.0, 50.1, 50.8]
    number_of_replicas = 3
    alpha = 0.05

    test = Linearity(analytical_data, volume_of_samples, mass_of_samples, number_of_replicas, dilution_factor, alpha)
    #print(test.grubbs_critical_value_calculation())
    #print(test.concentration_calculation())
    # slope, intercept, rvalue, pvalue, stderr = test.linear_regression_coefficients()
    # print("The Slope is: {}".format(slope))
    # print("The Intercept is: {}".format(intercept))
    # print("The Correlation coefficient is: {}".format(rvalue))
    # print("The Two-sided p-value is: {}".format(pvalue))
    # print("The Standard error of estimated gradient is: {}".format(stderr))
    test.ordinary_least_squares_linear_regression()
    #test.anova_analysis()

