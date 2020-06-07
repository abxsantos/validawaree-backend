import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

#================== Linearity ========================

# User inputs
#n_of_samples = 3 # Number of stock solutions
n_of_samples = 11
mass_of_samples = [50.0, 50.1, 50.8] # Known mass of analite in each stock solution
vol_of_samples = [50.0, 50.0, 50.0] # Volume of stock solutions
k_concentration = [0.03, 0.054, 0.078, 0.1020, 0.1260, 0,1500] # Known concentration of each measured sample
n_of_analysis = len(k_concentration)    # Number of analysis for each sample

#  Measured data
#analytical_data = [[0.188, 0.192, 0.203],[0.349, 0.346, 0.348],[0.489, 0.482,0.492],[0.637,0.641,0.641],[0.762,0.768,0.786],[0.931,0.924,0.925]] # carvedilol data
analytical_data = [[
11.89896,
11.9596,
11.89856,
11.91408,
12.04252,
12.1531,
11.94553,
11.8682,
11.85949,
12.13373,
12.6,
]]

arr_data = np.array([np.array(xi) for xi in analytical_data])
arr_data = np.array(analytical_data)
length = max(map(len, analytical_data))

y_arr = np.array([xi+[None]*(length-len(xi)) for xi in analytical_data])
x_arr = np.array(k_concentration)

i = 0
data_mean = []
data_std = []
data_var = []
data_G_calc = []

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
    print("Grubbs Critical Value: {} at a significance of".format(critical_value), alpha)
    return critical_value

def dataMeanCalculation(data_mean, i): # Calculate the mean for each concentration data set   
    while i < len(y_arr):
        data_mean.append(np.mean(y_arr[i]))    
        i = i + 1
    return data_mean

def dataSTDCalculation(data_std, i): # Calculate the standard deviation for each concentration data set
    while i < len(y_arr):
        data_std.append(np.std(y_arr[i], ddof=1)) # ddof = 1 for sample; if is population use ddof = 0
        i = i + 1
    return data_std

dataMeanCalculation(data_mean, 0)
dataSTDCalculation(data_std, 0)

def dataGCalc(data_G_calc, i): # Calculate the grubbs value for each item
    while i < len(analytical_data[0]):      
        G_calculated = abs((analytical_data[0][i]-data_mean[0])/data_std[0])
        data_G_calc.append(G_calculated)
        i = i + 1
    return data_G_calc

G_critical = grubbsCriticalValue(n_of_samples, 0.05)
dataGCalc(data_G_calc, 0)

# TODO: Create a new list with corrected values
# TODO: Rerun grubbs test with the corrected values
for G_calculated in data_G_calc:
    i = i + 1        
    if G_calculated > G_critical:
        print("outlier is in position {}".format(i))
    else:
        print("ok")
    