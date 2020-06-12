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
            print(csv_data)
            
            if csv_data[1].startswith("volume;"): # set condition to check header
                
                for line in csv_data:
                    clean_line = ((line.strip("\n")).split(";"))        
                    list_data.append(clean_line)

                # Separete the user imput CSV into variables
                analytical_data = list_data[4:]
                volume_of_samples = list_data[1][1]
                mass_of_samples = list_data[3]
                number_of_replicas = len(list_data[2])
                
                # Using the imported Linearity class to run statistical analysis on imported csv data
                linearity_analysis = Linearity(analytical_data, volume_of_samples, mass_of_samples, number_of_replicas)
                
                #TODO: ask for user alpha value input
                print("Grubbs Critical Value: {} at a significance of".format(linearity_analysis.grubbsCriticalValue(0, 0.5)))
                print("The mean of each replicate is: {}".format(linearity_analysis.dataMeanCalculation()))
                print("The Standar Deviation of each replicate is: {}".format(linearity_analysis.dataSTDCalculation()))
                print("The Grubbs calculated value for each item is: {}".format(linearity_analysis.dataGCalc()))
                    
                return render_template('data.html')
            else:
                print("Inserir na segunda linha primeira coluna 'volume'")
                return render_template('index.html')

"""
['carvedilol;;\n', 'volume;50,00;\n', 'sample1;sample2;sample3\n', '50,0;50,1;50,8\n', '0,188;0,192;0,203\n', '0,349;0,346;0,348\n', '0,489;0,482;0,492\n', '0,637;0,641;0,641\n', '0,762;0,768;0,786\n', '0,931;0,924;0,925\n']
"""

if __name__ == '__main__':
    app.run()