from flask import Flask, render_template, request
from modules.validation_analysis import Linearity

app = Flask(__name__)

# Render a home page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# Upload CSV file
@app.route('/data', methods=['GET', 'POST'])
def upload_csv():

    list_data = []
    analytical_data = []
    volume_of_samples = 0
    mass_of_samples = []
    number_of_replicas = 0

    if request.method == 'POST':
        file = request.form['upload-file']

        with open(file, "r") as csv_file:
            csv_data = csv_file.readlines()
            for line in csv_data:        
                list_data.append((line.strip("\n")).split(";"))

        # Separete the user imput CSV into variables
        analytical_data = list_data[4:]
        volume_of_samples = list_data[1][1]
        mass_of_samples = list_data[3]
        number_of_replicas = len(list_data[2])
        
        # Using the imported Linearity class to run statistical analysis on imported csv data
        linearity_analysis = Linearity(analytical_data, volume_of_samples, mass_of_samples, number_of_replicas)
        
        print("Grubbs Critical Value: {} at a significance of".format(linearity_analysis.grubbsCriticalValue(0, 0.5)))
        print("The mean of each replicate is: {}".format(linearity_analysis.dataMeanCalculation()))
        print("The Standar Deviation of each replicate is: {}".format(linearity_analysis.dataSTDCalculation()))
        print("The Grubbs calculated value for each item is: {}".format(linearity_analysis.dataGCalc()))

        return render_template('data.html')
        

if __name__ == '__main__':
    app.run()