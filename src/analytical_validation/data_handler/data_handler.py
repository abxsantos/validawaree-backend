from copy import deepcopy

from analytical_validation.exceptions import DataNotList, DataNotListOfLists, ValueNotValid, NegativeValue, \
    DataNotSymmetric


class DataHandler(object):
    def __init__(self, external_analytical_data, external_concentration_data):
        """
        Validate the linearity of the method.
        :param external_analytical_data: List containing all measured analytical signal.
        :type external_analytical_data: list[list]
        :param external_concentration_data: List containing the concentration for each analytical signal
        :type external_concentration_data: list[list]
        :raises

        """

        self.external_analytical_data = external_analytical_data
        self.external_concentration_data = external_concentration_data

        self.clean_analytical_data = []
        self.clean_concentration_data = []

    def check_is_list(data):
        """
        :param data: List containing analytical signal or concentration data.
        :type data: list
        :return:
        """
        if isinstance(data, list) is False:
            raise DataNotList()

    def check_list_of_lists(data):
        """
        :param data: List containing analytical signal or concentration data.
        :type data: list[list]
        :return:
        """

        def check_values(value):
            if isinstance(value, bool):
                raise ValueNotValid()
            if isinstance(value, str):
                value = value.replace(',', '.').replace(' ', '').replace('\n', '')
            try:
                if float(value) >= 0:
                    return float(value)
                else:
                    raise NegativeValue()
            except:
                raise ValueNotValid()

        float_data = []
        for data_set in data:
            if isinstance(data_set, list) is False:
                raise DataNotListOfLists()
            float_data_set = [check_values(value) for value in data_set]
            float_data.append(float_data_set)
        # TODO: Check if property needed
        return float_data

    def check_symmetric_data(self):
        if len(self.external_analytical_data) != len(self.external_concentration_data):
            raise DataNotSymmetric()

    def check_symmetric_data_set(self):
        if sum(list(map(lambda concentration_data_set: len(concentration_data_set),
                        self.external_concentration_data))) != sum(
                list(map(lambda analytical_data_set: len(analytical_data_set), self.external_analytical_data))):
            raise DataNotSymmetric()

    def replace_null_values(self):
        clean_analytical_data = deepcopy(self.external_analytical_data)
        clean_concentration_data = deepcopy(self.external_concentration_data)
        none_index = []
        for analytical_data_set in self.external_analytical_data:
            none_index.append([index for index, value in enumerate(analytical_data_set) if value is None])
        set_index = 0
        while set_index < len(clean_analytical_data):
            for i in none_index[set_index]:
                if none_index[set_index][0] != i:
                    i -= 1
                clean_analytical_data[set_index].pop(i)
                clean_concentration_data[set_index].pop(i)
            set_index += 1
        self.clean_analytical_data = clean_analytical_data
        self.clean_concentration_data = clean_concentration_data