from flask import Flask, render_template, request, make_response
from flask_restful import Resource, Api
from modules.validation_analysis import Linearity
from modules.read_csv_file import ReadAndOrganizeCSV

app = Flask(__name__)
api = Api(app)


class UploadData(Resource):

    def get(self):
        return make_response(render_template('index.html'))


class ViewData(Resource):

    def post(self):
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
        ################
        alpha = 0.05
        ################
        linearity_analysis = Linearity(analytical_data, volume_of_samples, mass_of_samples,
                                       number_of_replicas, dilution_factor, alpha)

        slope, intercept, stderr, slope_pvalue, intercept_pvalue, r_squared, \
        breusch_pagan_pvalue, residues, durbin_watson_value = linearity_analysis.ordinary_least_squares_linear_regression()

        degrees_of_freedom_regression, sum_of_squares_regression, regression_mean_square, \
        degrees_of_freedom_residual, sum_of_squares_residual, residual_mean_square, \
        sum_of_squares_total, degrees_of_freedom, f_anova, p_anova = linearity_analysis.anova_analysis()

        print("Submitted!")

        return make_response(render_template('data.html'))


api.add_resource(UploadData, '/')
api.add_resource(ViewData, '/data')

if __name__ == '__main__':
    app.run(debug=True)
