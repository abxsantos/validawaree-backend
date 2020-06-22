import csv

# r = ReadAndOrganizeCsv("/home/arquivo.csv")
# r.read()

# Linearity(r.mass, r.volume)


class ReadAndOrganizeCSV:
    def __init__(self, file):
        self.file = file
        self.analytica_data = []
        self.mass = []
        self.volume = []

    def read(self):
        self.read_csv_file()
        self.analytica_data = self.organize_analytical_data()
        self.mass = self.organize_mass_of_samples()
        self.volume = self.organize_volume_of_samples()

    def organize_analytical_data(self, x, y):
        """summary

        :param x: lista de dados
        :type x: int
        :param y: lista
        :type y: list
        :returns: A list of organized data
        :rtype: list
        """
        pass

    def organize_volume_of_samples(self, list_data):
        volume_of_samples = list_data[1][1]
        if volume_of_samples == '':
            print("There should be a value for volume.")
        try:
            volume_of_samples = float(volume_of_samples.replace(",", "."))
            if volume_of_samples < 0.0:
                raise ["The volume can't be a negative number. Change it."]
            elif volume_of_samples == 0.0:
                print("There should be a value for volume.")
            return volume_of_samples
        # TODO: Handle a message for each exception
        except:
            raise["Something is wrong with the volume."]

    def organize_dilution_factor(self, list_data):
        # Convert the user input CSV data to a better input format
        dilution_data = list_data[4:]
        float_data = []
        try:
            for dilution in dilution_data:
                clean_value = float(dilution[0].replace(",", "."))
                if clean_value < 0.0:
                    raise["The dilution factor can't be a negative number. Change it."]
                float_data.append(clean_value)
            dilution_data = float_data
            return dilution_data
        except:
            raise ["Something is wrong with the dilution factors."]

    def organize_mass_of_samples(self, list_data):
        list_of_mass = list_data[3][1:]
        mass_of_samples = []
        try:
            for mass in list_of_mass:
                mass = float(mass.replace(",", "."))
                if mass < 0.0:
                    raise["The mass can't be a negative number. Change it."]
                elif mass == 0:
                    raise["Warning! There is a 0 value in mass"]
                mass_of_samples.append(mass)
            return mass_of_samples
        except:
            raise["Something is wrong with the mass values."]

    # Isn't it better to check the number of replicas each time in the statistical analysis?
    def organize_number_of_replicas(self, list_data):
        number_of_replicas = len(list_data[2][1:])
        return number_of_replicas

















class ReadAndOrganizeCSV:
    def __init__(self, file):
        self.file = file

    def read_csv_file(self):
        list_data = []
        try:
            with open(self.file, "r") as csv_file:
                dialect = csv.Sniffer().sniff(csv_file.read(1024))
                csv_file.seek(0)
                csv_reader = csv.reader(csv_file, dialect)
                for clean_line in csv_reader:
                    if clean_line != []:
                        list_data.append(clean_line)
            return list_data
        except:
            raise["Couldn't open the file."]

    def organize_analytical_data(self, list_data):
        analytical_data = list_data[4:]
        # Convert the user input CSV data to a better input format
        float_data = []
        for measured_set in analytical_data:
            set_data = []
            for value in measured_set[1:]:
                clean_value = float(value.replace(",", "."))
                # Check for incorrect stuff
                if clean_value >= 0:
                    set_data.append(clean_value)
                else:
                    raise Exception("There is a negative value!")
            float_data.append(set_data)

        analytical_data = float_data
        return analytical_data

    def organize_volume_of_samples(self, list_data):
        volume_of_samples = list_data[1][1]
        if volume_of_samples == '':
            print("There should be a value for volume.")
        try:
            volume_of_samples = float(volume_of_samples.replace(",", "."))
            if volume_of_samples < 0.0:
                raise ["The volume can't be a negative number. Change it."]
            elif volume_of_samples == 0.0:
                print("There should be a value for volume.")
            return volume_of_samples
        # TODO: Handle a message for each exception
        except:
            raise["Something is wrong with the volume."]

    def organize_dilution_factor(self, list_data):
        # Convert the user input CSV data to a better input format
        dilution_data = list_data[4:]
        float_data = []
        try:
            for dilution in dilution_data:
                clean_value = float(dilution[0].replace(",", "."))
                if clean_value < 0.0:
                    raise["The dilution factor can't be a negative number. Change it."]
                float_data.append(clean_value)
            dilution_data = float_data
            return dilution_data
        except:
            raise ["Something is wrong with the dilution factors."]

    def organize_mass_of_samples(self, list_data):
        list_of_mass = list_data[3][1:]
        mass_of_samples = []
        try:
            for mass in list_of_mass:
                mass = float(mass.replace(",", "."))
                if mass < 0.0:
                    raise["The mass can't be a negative number. Change it."]
                elif mass == 0:
                    raise["Warning! There is a 0 value in mass"]
                mass_of_samples.append(mass)
            return mass_of_samples
        except:
            raise["Something is wrong with the mass values."]

    # Isn't it better to check the number of replicas each time in the statistical analysis?
    def organize_number_of_replicas(self, list_data):
        number_of_replicas = len(list_data[2][1:])
        return number_of_replicas


if __name__ == '__main__':
    file = '../file.csv'
    test = ReadAndOrganizeCSV(file)
    list_data = test.read_csv_file()
    # print(list_data)
    # print(test.organize_analytical_data(list_data))
    # print(test.organize_volume_of_samples(list_data))
    # print(test.organize_mass_of_samples(list_data))
    print(test.organize_dilution_factor(list_data))
    # print(test.organize_number_of_replicas(list_data))


