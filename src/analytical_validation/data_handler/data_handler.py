from copy import deepcopy

from analytical_validation.exceptions import DataNotList, DataNotListOfLists, ValueNotValid, NegativeValue, \
    DataNotSymmetric


def check_values(value):
    """
    Check for numbers converting it to float type.
    :param value: analytical signal or concentration value.
    :type value: any
    :raise ValueNotValid:
    :raise NegativeValue:
    :return value: A positive number converted to float.
    :rtype: float
    """
    if value is None:

        return value
    elif isinstance(value, bool):
        raise ValueNotValid()
    elif isinstance(value, str):
        value = value.replace(',', '.').replace(' ', '').replace('"', '').replace('\n', '').replace('"\\"', '')
    try:
        if float(value) >= 0:
            return float(value)
        else:
            raise NegativeValue()
    except Exception:
        raise ValueNotValid()


class DataHandlerHelper(object):
    def __init__(self, data):
        """
        Helper class to make individual data checks.
        :param data:
        :type data: list[list[float]]
        """
        self.data = data

    def check_is_list(self):
        """
        Check if the given data is a list.
        :raises:DataNotList
        """
        if isinstance(self.data, list) is False:
            raise DataNotList()

    def check_list_of_lists(self):
        """
        Check for numbers converting it to float type.
        :raise NegativeValue:
        :raise ValueNotValid:
        :raise DataNotListOfLists:
        :return float_data: List containing float only values.
        :rtype: list[list[float]]
        """
        float_data = []
        for data_set in self.data:
            if isinstance(data_set, list) is False:
                raise DataNotListOfLists()
            float_data_set = [check_values(value) for value in data_set]
            float_data.append(float_data_set)
        return float_data


class DataHandler(object):
    def __init__(self, external_analytical_data, external_concentration_data):
        """
         Prepare the data coming from the front end for analysis.
        :param external_analytical_data: List containing all measured analytical signal.
        :type external_analytical_data: list[list[float]]
        :param external_concentration_data: List containing the concentration for each analytical signal
        :type external_concentration_data: list[list[float]]
        """
        self.external_analytical_data = external_analytical_data
        self.external_concentration_data = external_concentration_data

    def check_symmetric_data(self):
        """
        Check if the analytical data and concentration
        data have the same number of data sets.
        :raises DataNotSymmetric:
        """
        if len(self.external_analytical_data) != len(self.external_concentration_data):
            raise DataNotSymmetric()

    def check_symmetric_data_set(self):
        """
        Check if the analytical data sets and concentration
        data sets have the same number of values.
        :raises DataNotSymmetric:
        """
        if sum(list(map(lambda concentration_data_set: len(concentration_data_set),
                        self.external_concentration_data))) != sum(
            list(map(lambda analytical_data_set: len(analytical_data_set), self.external_analytical_data))):
            raise DataNotSymmetric()

    def replace_null_values(self):
        """
        Checks for NoneType values in the analytical data set.
        If the data set has a None value, the method removes it from the
        analytical list and also removes the corresponding concentration value.
        :return clean_analytical_data: List without NoneType.
        :rtype: list[list[float]]
        :return clean_concentration_data: List without corresponding index value of NoneType.
        :rtype: list[list[float]]
        """
        clean_analytical_data = deepcopy(self.external_analytical_data)
        clean_concentration_data = deepcopy(self.external_concentration_data)
        none_index = []
        for analytical_data_set in self.external_analytical_data:
            none_index.append([index for index, value in enumerate(analytical_data_set) if value is None])
        set_index = 0
        while set_index < len(clean_analytical_data):
            index_pop_correction = 0
            for index_pop in none_index[set_index]:             # Corrects the index when there is more than 1 NoneType
                index_pop -= list(range(len(none_index[set_index])))[index_pop_correction]
                clean_analytical_data[set_index].pop(index_pop)
                clean_concentration_data[set_index].pop(index_pop)
                index_pop_correction += 1
            set_index += 1

        def clean_empty_lists(data):
            return [data_set for data_set in data if data_set != []]

        return clean_empty_lists(clean_analytical_data), clean_empty_lists(clean_concentration_data)

    def handle_data(self):
        """
        Prepare the data coming from the React-Redux Front-end for Linearity validation analysis.
        :returns analytical_data: List containing the analytical data, ready to be validated.
        :rtype analytical_data: list[list[float]]]
        :returns analytical_data: List containing the concentration data, ready to be validated.
        :rtype analytical_data: list[list[float]]]
        """
        DataHandlerHelper(self.external_analytical_data).check_is_list()
        DataHandlerHelper(self.external_concentration_data).check_is_list()
        analytical_data = DataHandlerHelper(self.external_analytical_data).check_list_of_lists()
        concentration_data = DataHandlerHelper(self.external_concentration_data).check_list_of_lists()
        DataHandler(analytical_data, concentration_data).check_symmetric_data()
        DataHandler(analytical_data, concentration_data).check_symmetric_data_set()
        checked_analytical_data, checked_concentration_data = DataHandler(analytical_data, concentration_data).replace_null_values()
        return checked_analytical_data, checked_concentration_data
