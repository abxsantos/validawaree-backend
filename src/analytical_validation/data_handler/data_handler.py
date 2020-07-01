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

    # def replace_null_values(self):
    #     for analytical_data_set in self.external_analytical_data:



#
# # analytical_data = [[1.0, 1.0, 10.0], [2.0, 6.0, 2.0]]
# # concentration_data = [[1.0, 2.0, 3.0], [8.0, 9.0, 10.0]]
#
# def handle_data_from_react(react_analytical_data, react_concentration_data):
#     """Saves the day treating the data coming from frontend
#
#     Example
#         >>> analytical_data = [[1.0, 2.0, 3.0], [8.0, 9.0, 10.0]]
#         >>> concentration_data = [[1.0, 2.0, 3.0], [8.0, 9.0, 10.0]]
#     :param analytical_data: List containing all measured analytical signal.
#     :type analytical_data: list
#     :param concentration_data: List containing the concentration for each analytical signal
#     :type concentration_data: list
#     """
#     # check for data inconsistency
#     #  the analytical data must be completely symmetric with concentration data
#     #  check if it's a list
#     if not isinstance(react_analytical_data, list) or not isinstance(react_concentration_data, list):
#         raise DataNotList()
#     #  check if its a list containing lists (set of data)
#     if all(isinstance(analytical_data_set, list) for analytical_data_set in react_analytical_data) is False or all(
#             isinstance(concentration_data_set, list) for concentration_data_set in react_concentration_data) is False:
#         raise DataNotListOfLists()
#     #  check if the number of set of data is symmetric
#     if len(react_analytical_data) != len(react_concentration_data):
#         raise DataSetNotSymmetric()
#     #       check if the number of values in the data sets are symmetric
#     for analytical_data_set, concentration_data_set in zip(react_analytical_data, react_concentration_data):
#         if len(analytical_data_set) != len(concentration_data_set):
#             raise DataSetNotSymmetric()
#     #       check if values are numbers and convert to float
#
#     float_analytical_data = []
#     for analytical_data_set in react_analytical_data:
#         try:
#             float_data_set = list(map((lambda value: float(check_for_negative(value))), analytical_data_set))
#             float_analytical_data.append(float_data_set)
#         except:
#             raise ValueNotValid()
#
#     float_concentration_data = []
#     for concentration_data_set in react_concentration_data:
#         try:
#             float_data_set = list(map((lambda value: float(check_for_negative(value))), concentration_data_set))
#             float_concentration_data.append(float_data_set)
#         except:
#             raise ValueNotValid()
#
# def check_for_negative(value):
#     if value > 0:
#         float(value)
#         return value
#     else:
#         raise NegativeValue()
#
#
#     # try:
#     #     for analytical_data_set in react_analytical_data:
#     #         for value in analytical_data_set:
#     #             if isinstance(value, bool):
#     #                 raise AnalyticalValueNotNumber()
#     #             value = float(value)
#     #             if value < 0:
#     #                 raise AnalyticalValueNegative()
#     # except (TypeError, ValueError):
#     #     raise AnalyticalValueNotNumber()
#     # try:
#     #     for concentration_data_set in react_concentration_data:
#     #         for value in concentration_data_set:
#     #             if isinstance(value, bool):
#     #                 raise ConcentrationValueNotNumber()
#     #             float_value = float(value)
#     #             if float_value < 0:
#     #                 raise ConcentrationValueNegative()
#     #
#     # except (TypeError, ValueError):
#     #     raise ConcentrationValueNotNumber()
#     #       check if there are invalid numbers (negative, null)
#     #       clean up non real float values
#
