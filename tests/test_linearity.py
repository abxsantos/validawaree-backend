import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from modules.validation_analysis import Linearity
import math

# Example of inputs
analytical_data = [['0,188', '0,192', '0,203'], ['0,349', '0,346', '0,348'], ['0,489', '0,482', '0,492'], ['0,637', '0,641', '0,641'], ['0,762', '0,768', '0,786'], ['0,931', '0,924', '0,925']]
volume_of_samples = '50,00'
mass_of_samples = ['50,0', '50,1', '50,8']
number_of_replicas = 3

linearity_analysis = Linearity(analytical_data, volume_of_samples, mass_of_samples, number_of_replicas)

# Test with pytest

def test_grubbs_critical_value():
    # Test that if it can calculate the grubbs critical value from a int and float
    assert linearity_analysis.grubbs_critical_value_calculation(0, 0.5) == 1.1153550716512923, "Should be 1.1153550716512923"

def test_grubbs_critical_value_0_alpha():
    # Test that if it can calculate the grubbs critical value from a int and float
    assert math.isnan(linearity_analysis.grubbs_critical_value_calculation(0, 0)) == True, "Should be True, because is a nan"

def test_mean_result():
    (linearity_analysis.data_mean_calculation()) == [0.19433333333333333, 0.3476666666666666, 0.4876666666666667, 0.6396666666666667, 0.7719999999999999, 0.9266666666666667]

def test_standard_deviation_result():
    (linearity_analysis.data_std_calculation()) == [0.0077674534651540365, 0.0015275252316519481, 0.005131601439446889, 0.0023094010767585054, 0.012489995996796807, 0.0037859388972001857]

def test_grubbs_calculated_value_result():
    linearity_analysis.data_grubbs_calculated() == [[0.8153680433034604, 0.30039875279601097, 1.1157667960994748], [0.8728715609439816, 1.0910894511799498, 0.2182178902360045], [0.25982792098464513, 1.1042686641847796, 0.8444407432001129], [1.1547005383792674, 0.5773502691896096, 0.5773502691896096], [0.8006407690254268, 0.3202563076101654, 1.120897076635619], [1.1445861782233013, 0.7043607250605088, 0.4402254531628217]]

# TODO: Make better tests


if __name__ == "__main__":
    test_grubbs_critical_value()
    test_grubbs_critical_value_0_alpha()
    test_mean_result()
    test_standard_deviation_result()
    test_grubbs_calculated_value_result()
    print("Everything passed")
