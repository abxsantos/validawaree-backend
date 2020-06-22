
# Remove and place inside test functions
list_data = [['carvedilol', '', '', ''], ['volume', '50,00', '', ''], ['', 'sample1', 'sample2', 'sample3'],
             ['dilutionfactor', '50,0', '50,1', '50,8'], ['125,00000', '0,188', '0,192', '0,203'],
             ['62,50000', '0,349', '0,346', '0,348'], ['50,00000', '0,489', '0,482', '0,492'],
             ['35,71429', '0,637', '0,641', '0,641'], ['31,25000', '0,762', '0,768', '0,786'],
             ['25,00000', '0,931', '0,924', '0,925']]

#################
#   File rules  #
#################
# The input file should be separated by ";"
# All numbers can be separated using . or ,
# There should be no values < 0.
# the volume, dilution rate, mass and analytical data should be a number

################
#  Test cases  #
################

# Volume = 0 or Volume empty: should return error and ask for user to add value.
# Volume < 0: should return error and ask for user to change.
# Volume should return a float > 0

# Mass = 0 or Mass empty: should raise a warning. All values in this column shouldn't be used unless mass > 0.
# Mass < 0: should raise an error and ask for user to change.
# Mass should return a float > 0

# Dilution factor = 0 or empty: the concentration will be equal to initial concentration.
# Dilution factor < 0: should raise an error and ask for user to change.
# Dilution Factor should return a float > 0

# Analytical data = 0 or empty: should be ignored
# Analytical data < 0:  should raise an error and ask for user to change.
# Analytical data should return a float > 0

###############
from modules.read_csv_file import ReadAndOrganizeCSV
import pytest


file = './old_tests/csv-test-files/test.csv'
negative_file = './old_tests/csv-test-files/test_negative_values.csv'
wrong_header_file = './old_tests/csv-test-files/test_wrong_header.csv'
zero_value_file = './old_tests/csv-test-files/test_zero_values.csv'

read_file = ReadAndOrganizeCSV(file)

read_wrong_header_file = ReadAndOrganizeCSV(wrong_header_file)
read_zero_value_file = ReadAndOrganizeCSV(zero_value_file)

def test_read_csv_file():
    assert read_file.read_csv_file() == [['carvedilol', '', '', ''],
                                         ['volume', '50,00', '', ''],
                                         ['', 'sample1', 'sample2', 'sample3'],
                                         ['dilutionfactor', '50,0', '50,1', '50,8'],
                                         ['125,00000', '0,188', '0,192', '0,203'],
                                         ['62,50000', '0,349', '0,346', '0,348'],
                                         ['50,00000', '0,489', '0,482', '0,492'],
                                         ['35,71429', '0,637', '0,641', '0,641'],
                                         ['31,25000', '0,762', '0,768', '0,786'],
                                         ['25,00000', '0,931', '0,924', '0,925']]


def test_organize_analytical_data():
    assert read_file.organize_analytical_data(list_data) == [[0.188, 0.192, 0.203],
                                                             [0.349, 0.346, 0.348],
                                                             [0.489, 0.482, 0.492],
                                                             [0.637, 0.641, 0.641],
                                                             [0.762, 0.768, 0.786],
                                                             [0.931, 0.924, 0.925]]


def test_organize_volume_of_samples():
    assert read_file.organize_volume_of_samples(list_data) == 50.0


def test_organize_mass_of_samples():
    assert read_file.organize_mass_of_samples(list_data) == [50.0, 50.1, 50.8]


def test_organize_dilution_factor():
    assert read_file.organize_dilution_factor(list_data) == [125.0, 62.5, 50.0, 35.71429, 31.25, 25.0]


def test_negative_value_analytical_data():
    # Arrange
    read_negative_file = ReadAndOrganizeCSV(negative_file)
    list_data = [['carvedilol', '', '', ''], ['volume', '50,00', '', ''], ['', 'sample1', 'sample2', 'sample3'],
             ['dilutionfactor', '50,0', '50,1', '50,8'], ['125,00000', '-0,188', '0,192', '0,203'],
             ['62,50000', '0,349', '0,346', '0,348'], ['50,00000', '0,489', '0,482', '0,492'],
             ['35,71429', '0,637', '0,641', '0,641'], ['31,25000', '0,762', '0,768', '0,786'],
             ['25,00000', '0,931', '0,924', '0,925']]
    # Act
    with pytest.raises(Exception) as excinfo:
        read_negative_file.organize_analytical_data(list_data)
    # Assert
    assert "There is a negative value!" in str(excinfo.value)