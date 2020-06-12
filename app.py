from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

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

        analytical_data = list_data[4:]
        volume_of_samples = list_data[1][1]
        mass_of_samples = list_data[3]
        number_of_replicas = len(list_data[2])

        print(analytical_data)
        print(volume_of_samples)
        print(mass_of_samples)
        print(number_of_replicas)

        return render_template('data.html')
        #TODO: retrieve the data so i can use outside this

if __name__ == '__main__':
    app.run()