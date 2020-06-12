from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


def read_csv(data):
  read_file = data
  print(read_file)
  print("The CSV was read")

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        file = request.form['upload-file']
        data = pd.read_excel(file)
        read_csv(data)
        return render_template('data.html')



if __name__ == '__main__':
    app.run()