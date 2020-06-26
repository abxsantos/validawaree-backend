from analytical_validation.validators.linearity_validator import LinearityValidator


class TestLinearityValidator(object):
    def test_is_homokedastic_return_true(self):
        analytical_data = [0.188, 0.192, 0.203, 0.349, 0.346, 0.348, 0.489, 0.482, 0.492, 0.637, 0.641, 0.641, 0.762,
                           0.768, 0.786, 0.931, 0.924,
                           0.925]
        concentration_data = [0.008, 0.008016, 0.008128, 0.016, 0.016032, 0.016256, 0.02, 0.02004, 0.02032,
                              0.027999996640000406, 0.028055996633280407, 0.02844799658624041, 0.032, 0.032064,
                              0.032512, 0.04, 0.04008, 0.04064]
        # Arrange
        linearity_validator = LinearityValidator(analytical_data, concentration_data)
        linearity_validator.ordinary_least_squares_linear_regression()
        linearity_validator.run_breusch_pagan_test()
        # Act & Assert
        # TODO: assert other real values.
        assert linearity_validator.is_homokedastic is True