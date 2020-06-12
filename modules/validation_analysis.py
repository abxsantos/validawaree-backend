import numpy as np
import scipy.stats as stats

# # Example of inputs
# analytical_data = [['0,188', '0,192', '0,203'], ['0,349', '0,346', '0,348'], ['0,489', '0,482', '0,492'], ['0,637', '0,641', '0,641'], ['0,762', '0,768', '0,786'], ['0,931', '0,924', '0,925']]
# volume_of_samples = '50,00'
# mass_of_samples = ['50,0', '50,1', '50,8']
# number_of_replicas = 3

class Linearity:
    def __init__(self, analytical_data, volume_of_samples, mass_of_samples, number_of_replicas):
        
        # Convert the user input CSV data to a better input format  
        float_data = []
        for measured_set in analytical_data:
            set_data = []
            for value in measured_set:      
                set_data.append(float(value.replace(",", ".")))
            float_data.append(set_data)
        
        self.analytical_data = float_data     

        self.volume_of_samples = float(volume_of_samples.replace(",", "."))
        
        self.mass_of_samples = [float(index.replace(",", ".")) for index in mass_of_samples]
        
        self.number_of_replicas = number_of_replicas
        
    def concentracao(self):
        print(self.analytical_data)
        print(self.volume_of_samples)
        print(self.mass_of_samples)
        print(self.number_of_replicas)

    # Calculate the Grubbs critical value based on the number of replicas (triplicate...) and alpha value (confidence level)
    def grubbsCriticalValue(self, number_of_replicas, alpha):
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
        #print("Grubbs Critical Value: {} at a significance of".format(critical_value), alpha)
        return critical_value     
    
    # Calculate the mean for each concentration data set
    def dataMeanCalculation(self): 
        data_mean = []
        for entries in self.analytical_data:
            mean = np.nanmean(entries)
            data_mean.append(mean)
        return(data_mean)

    # Calculate the STandard Deviation for each concentration data set
    def dataSTDCalculation(self): 
        data_std = []
        for entries in self.analytical_data:
            std = np.nanstd(entries, ddof=1)
            data_std.append(std)
        return(data_std)

    # Calculate the grubbs value for each item
    def dataGCalc(self): 
        n = 0
        data_G_calc = []
        data_mean = self.dataMeanCalculation()
        data_std = self.dataSTDCalculation()        
        for data_set in self.analytical_data:
            index = 0
            G_calculated_set = []
            while index < len(data_set):
                G_calculated = abs(data_set[index]-data_mean[n])/data_std[n]
                G_calculated_set.append(G_calculated)
                index = index + 1
            data_G_calc.append(G_calculated_set)
            n = n + 1   
        return (data_G_calc)


if __name__ == '__main__':
    # Example of inputs
    analytical_data = [['0,188', '0,192', '0,203'], ['0,349', '0,346', '0,348'], ['0,489', '0,482', '0,492'], ['0,637', '0,641', '0,641'], ['0,762', '0,768', '0,786'], ['0,931', '0,924', '0,925']]
    volume_of_samples = '50,00'
    mass_of_samples = ['50,0', '50,1', '50,8']
    number_of_replicas = 3
    
    teste = Linearity(analytical_data, volume_of_samples, mass_of_samples, number_of_replicas)
    teste.grubbsCriticalValue(0, 0.5)
    print(teste.dataMeanCalculation())
    print(teste.dataSTDCalculation())
    print(teste.dataGCalc())