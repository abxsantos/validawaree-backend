from analytical_validation.data_handler.data_handler import DataHandler
from analytical_validation.validators.linearity_validator import LinearityValidator


class TestLinearityValidator(object):

    def test_linearity_validator_integration_with_methods(self):
        input_analytical_data = [[0.188, 0.192, 0.203], [0.349, 0.346, 0.348], [0.489, 0.482, 0.492],
                                 [0.637, 0.641, 0.641],
                                 [0.762,
                                  0.768, 0.786], [0.931, 0.924, 0.925]]
        input_concentration_data = [[0.008, 0.008016, 0.008128], [0.016, 0.016032, 0.016256], [0.02, 0.02004, 0.02032],
                                    [0.027999996640000406, 0.028055996633280407, 0.02844799658624041], [0.032, 0.032064,
                                                                                                        0.032512],
                                    [0.04, 0.04008, 0.04064]]
        # Arrange
        data_handler = DataHandler(input_analytical_data, input_concentration_data)
        checked_analytical_data, checked_concentration_data = data_handler.handle_data()
        linearity_validator = LinearityValidator(checked_analytical_data, checked_concentration_data)
        # Act
        linearity_validator.validate_linearity()
        # Assert
        assert linearity_validator.intercept is not None
        assert linearity_validator.slope is not None
        assert linearity_validator.r_squared is not None
        assert linearity_validator.significant_slope
        assert linearity_validator.insignificant_intercept
        assert linearity_validator.valid_r_squared
        assert linearity_validator.valid_regression_model
        assert linearity_validator.sum_of_squares_model is not None
        assert linearity_validator.sum_of_squares_resid is not None
        assert linearity_validator.sum_of_squares_total is not None
        assert linearity_validator.degrees_of_freedom_model is not None
        assert linearity_validator.degrees_of_freedom_residues is not None
        assert linearity_validator.degrees_of_freedom_total is not None
        assert linearity_validator.mean_squared_error_model is not None
        assert linearity_validator.mean_squared_error_residues is not None
        assert linearity_validator.anova_f_value is not None
        assert linearity_validator.anova_f_pvalue is not None
        assert linearity_validator.is_normal_distribution
        assert linearity_validator.is_homoscedastic
        assert linearity_validator.durbin_watson_value is not None

    def test_linearity_validator_integration_with_react_values(self):
        input_analytical_data = [['1', '1', '1'], ['3123', '132', None], [None, None, None]]
        input_concentration_data = [[0.2, 0.2, 0.2], [0.006230529595015576, 0.006230529595015576, 0.006230529595015576],
                                    [None, None, None]]
        # Arrange
        data_handler = DataHandler(input_analytical_data, input_concentration_data)
        checked_analytical_data, checked_concentration_data = data_handler.handle_data()
        linearity_validator = LinearityValidator(checked_analytical_data, checked_concentration_data)
        # Assert
        linearity_validator.validate_linearity()
        # Act
        assert linearity_validator.intercept is not None
        assert linearity_validator.slope is not None
        assert linearity_validator.r_squared is not None
        assert linearity_validator.significant_slope is False
        assert linearity_validator.insignificant_intercept
        assert linearity_validator.valid_r_squared is False
        assert linearity_validator.valid_regression_model is False
        assert linearity_validator.sum_of_squares_model is not None
        assert linearity_validator.sum_of_squares_resid is not None
        assert linearity_validator.sum_of_squares_total is not None
        assert linearity_validator.degrees_of_freedom_model is not None
        assert linearity_validator.degrees_of_freedom_residues is not None
        assert linearity_validator.degrees_of_freedom_total is not None
        assert linearity_validator.mean_squared_error_model is not None
        assert linearity_validator.mean_squared_error_residues is not None
        assert linearity_validator.anova_f_value is not None
        assert linearity_validator.anova_f_pvalue is not None
        assert linearity_validator.is_normal_distribution is False
        assert linearity_validator.is_homoscedastic is False
        assert linearity_validator.durbin_watson_value is not None

    def test_hplc_values(self):
        input_analytical_data = [[88269, 86954, 88492], [99580, 101235, 100228], [108238, 109725, 110970],
                           [118102, 119044, 118292], [129714, 129481, 130213]]
        input_concentration_data = [[31800, 31680, 31600], [36080, 36600, 36150], [39641, 40108, 40190],
                              [43564, 43800, 43776], [47680, 47800, 47341]]
        # Arrange
        data_handler = DataHandler(input_analytical_data, input_concentration_data)
        checked_analytical_data, checked_concentration_data = data_handler.handle_data()
        linearity_validator = LinearityValidator(checked_analytical_data, checked_concentration_data)
        # Act
        outliers, cleaned_analytical_data, cleaned_concentration_data, linearity_is_valid = linearity_validator.validate_linearity()
        intercept = linearity_validator.intercept
        slope = linearity_validator.slope
        r_squared = linearity_validator.r_squared
        significant_slope = linearity_validator.significant_slope
        insignificant_intercept = linearity_validator.insignificant_intercept
        valid_r_squared = linearity_validator.valid_r_squared
        valid_regression_model =  linearity_validator.valid_regression_model
        sum_of_squares_model = linearity_validator.sum_of_squares_model
        sum_of_squares_resid = linearity_validator.sum_of_squares_resid
        sum_of_squares_total = linearity_validator.sum_of_squares_total
        degrees_of_freedom_model = linearity_validator.degrees_of_freedom_model
        degrees_of_freedom_residues = linearity_validator.degrees_of_freedom_residues
        degrees_of_freedom_total = linearity_validator.degrees_of_freedom_total
        mean_squared_error_model = linearity_validator.mean_squared_error_model
        mean_squared_error_residues = linearity_validator.mean_squared_error_residues
        anova_f_value = linearity_validator.anova_f_value
        anova_f_pvalue = linearity_validator.anova_f_pvalue
        is_normal_distribution = linearity_validator.is_normal_distribution
        is_homoscedastic = linearity_validator.is_homoscedastic
        durbin_watson_value = linearity_validator.durbin_watson_value
        shapiro_pvalue = linearity_validator.shapiro_pvalue
        breusch_pagan_pvalue = linearity_validator.breusch_pagan_pvalue
        linearity_is_valid = linearity_validator.linearity_is_valid
        # Assert
        assert intercept == 5739.794788269286
        assert slope == 2.596878737685822
        assert r_squared == 0.9975294485602224
        assert significant_slope
        assert insignificant_intercept is False
        assert valid_r_squared
        assert valid_regression_model is False
        assert sum_of_squares_model == 3127367965.4154825
        assert sum_of_squares_resid == 7745458.98451753
        assert sum_of_squares_total == 3135113424.4
        assert degrees_of_freedom_model == 1
        assert degrees_of_freedom_residues == 13
        assert degrees_of_freedom_total == 14
        assert mean_squared_error_model == 3127367965.4154825
        assert mean_squared_error_residues == 595804.5372705793
        assert anova_f_value == 5248.983130847184
        assert anova_f_pvalue == 2.456125525312856e-18
        assert is_normal_distribution
        assert is_homoscedastic
        assert durbin_watson_value == 2.015779987671755
        assert shapiro_pvalue == 0.24514977633953094
        assert breusch_pagan_pvalue == 0.37048855993099217
        assert outliers == [[], [], [], [], []]
        assert cleaned_analytical_data == input_analytical_data
        assert cleaned_concentration_data == input_concentration_data
        assert linearity_is_valid is False
