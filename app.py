from flask import Flask, render_template, request
from modules.validation_analysis import Linearity
from modules.read_csv_file import ReadAndOrganizeCSV

app = Flask(__name__)

# Render a home page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# Upload CSV file
@app.route('/data', methods=['POST'])
def upload_csv():

    if request.method == 'POST':
        file = request.form['upload-file']
        # Read the file and separate its rows into lists
        read_uploaded_file = ReadAndOrganizeCSV(file)
        list_data = read_uploaded_file.read_csv_file()

        # Organize the data lists and check for some negative values
        analytical_data = read_uploaded_file.organize_analytical_data(list_data)
        volume_of_samples = read_uploaded_file.organize_volume_of_samples(list_data)
        mass_of_samples = read_uploaded_file.organize_mass_of_samples(list_data)
        number_of_replicas = read_uploaded_file.organize_number_of_replicas(list_data)
        dilution_factor = read_uploaded_file.organize_dilution_factor(list_data)
                
        # Using the imported Linearity class to run statistical analysis on imported csv data
        linearity_analysis = Linearity(analytical_data, volume_of_samples, mass_of_samples, number_of_replicas, dilution_factor)

        print("The average of each replicate is: {}".format(linearity_analysis.data_mean_calculation()))
        print("The Standard Deviation of each replicate is: {}".format(linearity_analysis.data_std_calculation()))

        slope, intercept, rvalue, pvalue, stderr = linearity_analysis.linear_regression_coefficients()

        print("############################################################################")
        print("#    The Slope is: {}".format(slope))
        print("#    The Intercept is: {}".format(intercept))
        print("#    The Correlation coefficient is: {}".format(rvalue))
        print("#    The Two-sided p-value is: {}".format(pvalue))
        print("#    The Standard error of estimated gradient is: {}".format(stderr))
        print("############################################################################")
        return render_template('data.html')

if __name__ == '__main__':
    app.run(debug=True)