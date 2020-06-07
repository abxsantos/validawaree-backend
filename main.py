import pandas as pd
from scipy import stats
import numpy as np

n_of_samples = 3 # Number of stock solutions
mass_of_samples = [50.0, 50.1, 50.8] # Known mass of analite in each stock solution
vol_of_samples = [50.0, 50.0, 50.0] # Volume of stock solutions
k_concentration = [0.008, 0.009, 0.010, 0.011, 0.012] # Known concentration of each measured sample
n_of_analysis = len(k_concentration)    # Number of analysis for each sample
df_k_concentration = pd.DataFrame(k_concentration) # Concentration pandas dataframe

#TODO: Implement outlier cochrane test for the Analytical responses
#TODO: Remove the outliers and replace with NaN
analytical_response = { # Analytical responses for each concentration of each sample
    "Sample 1": [0.590, 0.548, 0.651, 0.710, 0.773],
    "Sample 2": [0.526, 0.544, 0.609, 0.698, 0.559],
    "Sample 3": [0.560, 0.582, 0.692, 0.696, 0.830]
}

df_analytical_response = pd.DataFrame(data=analytical_response) # Analytical pandas dataframe
mean_analytical_response = df_analytical_response.mean(axis = 1)# MEAN pandas dataframe
std_analytical_response = df_analytical_response.std(axis = 1) # STD pandas dataframe

df_analytical_response.insert(0, 'Concentration', df_k_concentration) # Inserting concentration into main dataframe
df_analytical_response = (pd.concat([df_analytical_response, mean_analytical_response], axis=1)).rename(columns={0:'Mean'}) # Inserting MEAN into main dataframe
main_df = (pd.concat([df_analytical_response, std_analytical_response], axis=1)).rename(columns={0:'STD'}) # Inserting STD into main dataframe

#print(main_df)