list_data = [['carvedilol', '', '', ''], ['volume', '50,00', '', ''], ['', 'sample1', 'sample2', 'sample3'],
             ['dilutionfactor', '50,0', '50,1', '50,8'], ['125,00000', '0,188', '0,192', '0,203'],
             ['62,50000', '0,349', '0,346', '0,348'], ['50,00000', '0,489', '0,482', '0,492'],
             ['35,71429', '0,637', '0,641', '0,641'], ['31,25000', '0,762', '0,768', '0,786'],
             ['25,00000', '0,931', '0,924', '0,925']]
# [[0.188, 0.192, 0.203], [0.349, 0.346, 0.348], [0.489, 0.482, 0.492], [0.637, 0.641, 0.641], [0.762, 0.768, 0.786], [0.931, 0.924, 0.925]]
# 50.0
# [50.0, 50.1, 50.8]
# [125.0, 62.5, 50.0, 35.71429, 31.25, 25.0]
# 3
from modules.read_csv_file import ReadAndOrganizeCSV

file = 'file.csv'
read_file = ReadAndOrganizeCSV(file)


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


def test_organize_dilution_factor():
    assert read_file.organize_dilution_factor(list_data) == [50.0, 50.1, 50.8]


def test_organize_mass_of_samples():
    assert read_file.organize_mass_of_samples(list_data) == [125.0, 62.5, 50.0, 35.71429, 31.25, 25.0]


def test_organize_number_of_replicas():
    assert read_file.organize_number_of_replicas(list_data) == 3
