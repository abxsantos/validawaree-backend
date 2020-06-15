def dixon_test(data, left=True, right=True, alpha=0.05):

    valid_alpha = {0.01, 0.05, 0.10}
    if alpha not in valid_alpha:
        raise ValueError("dixon_test: The alpha value must be one of %r." % valid_alpha)
    """
    Keyword arguments:
        data = A ordered or unordered list of data points (int or float).
        left = Q-test of minimum value in the ordered list if True.
        right = Q-test of maximum value in the ordered list if True.
        q_dict = A dictionary of Q-values for a given confidence level,
            where the dict. keys are sample sizes N, and the associated values
            are the corresponding critical Q values. E.g.,
            {3: 0.97, 4: 0.829, 5: 0.71, 6: 0.625, ...}

    Returns a list of 2 values for the outliers, or None.
    E.g.,
       for [1,1,1] -> [None, None]
       for [5,1,1] -> [None, 5]
       for [5,1,5] -> [1, None]

    """

    if alpha == 0.10:
        q_value = [0.941, 0.765, 0.642, 0.56, 0.507, 0.468, 0.437,
           0.412, 0.392, 0.376, 0.361, 0.349, 0.338, 0.329,
           0.32, 0.313, 0.306, 0.3, 0.295, 0.29, 0.285, 0.281,
           0.277, 0.273, 0.269, 0.266, 0.263, 0.26
           ]
    elif alpha == 0.05:
        q_value = [0.97, 0.829, 0.71, 0.625, 0.568, 0.526, 0.493, 0.466,
           0.444, 0.426, 0.41, 0.396, 0.384, 0.374, 0.365, 0.356,
           0.349, 0.342, 0.337, 0.331, 0.326, 0.321, 0.317, 0.312,
           0.308, 0.305, 0.301, 0.29
           ]
    elif alpha == 0.01:
        q_value = [0.994, 0.926, 0.821, 0.74, 0.68, 0.634, 0.598, 0.568,
           0.542, 0.522, 0.503, 0.488, 0.475, 0.463, 0.452, 0.442,
           0.433, 0.425, 0.418, 0.411, 0.404, 0.399, 0.393, 0.388,
           0.384, 0.38, 0.376, 0.372
           ]

    q_dict = {n: q for n, q in zip(range(3, len(q_value) + 1), q_value)}

    assert(left or right), 'At least one of the variables, `left` or `right`, must be True.'
    assert(len(data) >= 3), 'At least 3 data points are required'
    assert(len(data) <= max(q_dict.keys())), 'Sample size too large'

    sdata = sorted(data)
    Q_mindiff, Q_maxdiff = (0,0), (0,0)

    if left:
        Q_min = (sdata[1] - sdata[0])
        try:
            Q_min /= (sdata[-1] - sdata[0])
        except ZeroDivisionError:
            pass
        Q_mindiff = (Q_min - q_dict[len(data)], sdata[0])

    if right:
        Q_max = abs((sdata[-2] - sdata[-1]))
        try:
            Q_max /= abs((sdata[0] - sdata[-1]))
        except ZeroDivisionError:
            pass
        Q_maxdiff = (Q_max - q_dict[len(data)], sdata[-1])

    if not Q_mindiff[0] > 0 and not Q_maxdiff[0] > 0:
        outliers = [None, None]

    elif Q_mindiff[0] == Q_maxdiff[0]:
        outliers = [Q_mindiff[1], Q_maxdiff[1]]

    elif Q_mindiff[0] > Q_maxdiff[0]:
        outliers = [Q_mindiff[1], None]

    else:
        outliers = [None, Q_maxdiff[1]]

    return outliers

