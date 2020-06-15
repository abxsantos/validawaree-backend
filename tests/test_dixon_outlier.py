
import modules.dixon_outlier as dixon_outlier


test_data1 = [0.142, 0.153, 0.135, 0.002, 0.175]
test_data2 = [0.542, 0.153, 0.135, 0.002, 0.175]

def test_min_max_values_dixon_outlier_with_outliers_data():
	assert dixon_outlier.dixon_test(test_data1) == [0.002, None], 'expect [0.002, None]'

def test_min_values_dixon_outlier_with_outliers_data():
	assert(dixon_outlier.dixon_test(test_data1, right=False) == [0.002, None]), 'expect [0.002, None]'

def test_min_max_values_dixon_outlier_with_no_outliers_data():
	assert dixon_outlier.dixon_test(test_data2) == [None, None], 'expect [None, None]'

def test_min_max_values_dixon_outlier_with_other_alpha():
	assert(dixon_outlier.dixon_test(test_data2, alpha=0.10) == [None, 0.542]), 'expect [None, 0.542]'