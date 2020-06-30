import json

from flask_restful import Resource, reqparse

from analytical_validation.validators.linearity_validator import LinearityValidator

parser = reqparse.RequestParser()
parser.add_argument('analytical_data')
parser.add_argument('concentration_data')


class LinearityValidation(Resource):
    def post(self):
        args = parser.parse_args()
        print(args)
        analytical_data = json.loads(args['analytical_data'])
        concentration_data = json.loads(args['concentration_data'])
        try:
            linearity_validator = LinearityValidator(analytical_data, concentration_data)
            linearity_validator.ordinary_least_squares_linear_regression()
            linearity_validator.run_shapiro_wilk_test()
            # linearity_validator.check_outliers()
            linearity_validator.run_breusch_pagan_test()
            linearity_validator.check_residual_autocorrelation()
            return {
                       'regression': {'intercept': linearity_validator.intercept,
                                      'insiginificant_intercept': linearity_validator.insignificant_intercept,
                                      'slope': linearity_validator.slope,
                                      'significant_slope': linearity_validator.significant_slope,
                                      'r_squared': linearity_validator.r_squared,
                                      'valid_regression': linearity_validator.valid_regression_model},
                       'anova': {'sum_of_squares_model': linearity_validator.sum_of_squares_model,
                                 'sum_of_squares_residual': linearity_validator.sum_of_squares_resid,
                                 'sum_of_squares_total': linearity_validator.sum_of_squares_total,
                                 'degrees_of_freedom_model': linearity_validator.degrees_of_freedom_model,
                                 'degrees_of_freedom_residues': linearity_validator.degrees_of_freedom_residues,
                                 'degrees_of_freedom_total': linearity_validator.degrees_of_freedom_total,
                                 'mean_squared_error_model': linearity_validator.mean_squared_error_model,
                                 'mean_squared_error_residues': linearity_validator.mean_squared_error_residues,
                                 'anova_f_value': linearity_validator.anova_f_value,
                                 'anova_f_pvalue': linearity_validator.anova_f_pvalue, },
                        # TODO: Pass cleaned data
                       # 'cleaned_data': {'outliers': linearity_validator.outliers,
                       #                  'cleaned_analytical_data': linearity_validator.cleaned_data,
                       #                  'cleaned_concentration_data': linearity_validator.cleaned_concentration_data, },
                       'is_normal_distribution': linearity_validator.is_normal_distribution,
                       'is_homokedastic': linearity_validator.is_homokedastic,
                       'durbin_watson_value': linearity_validator.durbin_watson_value}, 201

        except Exception as err:
            return err, 400
