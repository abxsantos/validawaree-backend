import csv


class ReadAndOrganizeCSV:
    def __init__(self, file):
        self.file = file

    def read_csv_file(self):
        list_data = []
        with open(self.file, "r") as csv_file:
            dialect = csv.Sniffer().sniff(csv_file.read(1024))
            csv_file.seek(0)
            csv_reader = csv.reader(csv_file, dialect)
            for clean_line in csv_reader:
                if clean_line != []:
                    list_data.append(clean_line)
        return list_data

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
                    print("There is a negative value!")
            float_data.append(set_data)

        analytical_data = float_data
        return analytical_data

    def organize_volume_of_samples(self, list_data):
        volume_of_samples = list_data[1][1]
        volume_of_samples = float(volume_of_samples.replace(",", "."))

        return volume_of_samples

    def organize_dilution_factor(self, list_data):
        # Convert the user input CSV data to a better input format
        dilution_data = list_data[4:]
        float_data=[]
        for dilution in dilution_data:
            clean_value = float(dilution[0].replace(",", "."))
            float_data.append(clean_value)
        dilution_data = float_data
        return dilution_data

    def organize_mass_of_samples(self, list_data):
        mass_of_samples = list_data[3][1:]
        mass_of_samples = [float(index.replace(",", ".")) for index in mass_of_samples]
        return mass_of_samples

    def organize_number_of_replicas(self, list_data):
        number_of_replicas = len(list_data[2][1:])
        return number_of_replicas


if __name__ == '__main__':
    file = '../file.csv'
    test = ReadAndOrganizeCSV(file)
    list_data = test.read_csv_file()
    print(list_data)
    print(test.organize_analytical_data(list_data))
    print(test.organize_volume_of_samples(list_data))
    print(test.organize_mass_of_samples(list_data))
    print(test.organize_dilution_factor(list_data))
    print(test.organize_number_of_replicas(list_data))


