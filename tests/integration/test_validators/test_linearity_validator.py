import pytest

from analytical_validation.validators.linearity_validator import LinearityValidator


class TestLinearityValidator(object):
    def test_is_homokedastic_return_true(self):
        analytical_data = [[0.188, 0.192, 0.203], [0.349, 0.346, 0.348], [0.489, 0.482, 0.492], [0.637, 0.641, 0.641], [0.762,
                           0.768, 0.786], [0.931, 0.924, 0.925]]
        concentration_data = [[0.008, 0.008016, 0.008128], [0.016, 0.016032, 0.016256], [0.02, 0.02004, 0.02032],
                              [0.027999996640000406, 0.028055996633280407, 0.02844799658624041], [0.032, 0.032064,
                              0.032512], [0.04, 0.04008, 0.04064]]
        # Arrange
        linearity_validator = LinearityValidator(analytical_data, concentration_data)
        linearity_validator.ordinary_least_squares_linear_regression()
        linearity_validator.run_shapiro_wilk_test()
        linearity_validator.run_breusch_pagan_test()
        linearity_validator.check_residual_autocorrelation()
        # Act & Assert
        # TODO: assert other real values.
        assert linearity_validator.sum_of_squares_model is not None
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
        assert linearity_validator.is_homokedastic
        assert linearity_validator.durbin_watson_value is not None

    def test_hplc_values(self):
        analytical_data = [[88269, 86954, 88269], [99580, 101235, 100228], [108238, 109725, 110970],
                           [118102, 119044, 118292], [129714, 129481, 130213]]
        concentration_data = [[31800, 31680, 31600], [36080, 36600, 36150], [39641, 40108, 40190],
                              [43564, 43800, 43776], [47680, 47800, 47341]]
        # Arrange
        linearity_validator = LinearityValidator(analytical_data, concentration_data)
        linearity_validator.ordinary_least_squares_linear_regression()
        linearity_validator.run_shapiro_wilk_test()
        linearity_validator.run_breusch_pagan_test()
        linearity_validator.check_residual_autocorrelation()
        # Act & Assert
        # TODO: assert other real values.
        assert linearity_validator.sum_of_squares_model is not None
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
        assert linearity_validator.is_homokedastic
        assert linearity_validator.durbin_watson_value is not None

        #TODO: make integration test for only one set of concentration and analytical data. Must raise exception.