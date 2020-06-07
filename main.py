import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

#================== Linearity ========================

# User inputs
n_of_samples = 3 # Number of stock solutions
mass_of_samples = [50.0, 50.1, 50.8] # Known mass of analite in each stock solution
vol_of_samples = [50.0, 50.0, 50.0] # Volume of stock solutions
k_concentration = [0.03, 0.054, 0.078, 0.1020, 0.1260, 0,1500] # Known concentration of each measured sample
n_of_analysis = len(k_concentration)    # Number of analysis for each sample

#  Measured data
analytical_data = [[0.188, 0.192, 0.203],[2.349, 0.346, 0.348],[0.489, 0.482,0.492],[3.637,0.641,0.641],[0.762,0.768,0.786],[0.931,0.924,0.925]] # carvedilol data

def grubbsCriticalValue(sample_size, alpha):
    """Calculate the critical value with the formula given for example in
    https://en.wikipedia.org/wiki/Grubbs%27_test_for_outliers#Definition
    Args:
        ts (list or np.array): The timeseries to compute the critical value.
        alpha (float): The significance level.
    Returns:
        float: The critical value for this test.
    """
    t_dist = stats.t.ppf(1 - alpha / (2 * sample_size), sample_size - 2)
    numerator = (sample_size - 1) * np.sqrt(np.square(t_dist))
    denominator = np.sqrt(sample_size) * np.sqrt(sample_size - 2 + np.square(t_dist))
    critical_value = numerator / denominator
    # print("Grubbs Critical Value: {} at a significance of".format(critical_value), alpha)
    return critical_value

def dataMeanCalculation(data_mean, i): # Calculate the mean for each concentration data set
    for entries in analytical_data:    
        mean = np.mean(entries)
        data_mean.append(mean)
    return(data_mean)

def dataSTDCalculation(data_std, i): # Calculate the standard deviation for each concentration data set
    for entries in analytical_data:    
        std = np.std(entries, ddof=1)
        data_std.append(std)
    return(data_std) 

def dataGCalc(data_G_calc): # Calculate the grubbs value for each item
    data_mean = dataMeanCalculation([], 0)
    data_std = dataSTDCalculation([], 0)
    n = 0
    for data_set in analytical_data:
        index = 0
        G_calculated_set = []
        while index < len(data_set):
            G_calculated = abs(data_set[index]-data_mean[n])/data_std[n]
            G_calculated_set.append(G_calculated)
            index = index + 1
        data_G_calc.append(G_calculated_set)
        n = n + 1   
    return (data_G_calc)

def removeOutliers(): # Test the hipothesis and remove all values > Gcrit
    data_G_calc = []
    G_critical = grubbsCriticalValue(n_of_samples, 0.05)
    dataGCalc([])
    outlier_dict = {"index_array": [],"index_value": [], "value": []} # Set the outlier values and coordinates to this dict
    index_array_list = []
    index_value_list = []
    outlier_list = []
    index_array = 0
    for G_data_set in data_G_calc:
        index_value = 0
        for G_calculated in G_data_set:
            if G_calculated > G_critical:
                index_array_list.append(index_array)            
                index_value_list.append(index_value)            
                outlier_list.append((analytical_data[index_array]).pop(index_value))         
                outlier_dict.update({"index_array": index_array_list, "index_value": index_value_list, "value": outlier_list})
                index_value = index_value + 1
            else:
                index_value = index_value + 1
        index_array = index_array + 1
    index_array = 0
    index_value = 0