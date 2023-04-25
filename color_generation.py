from sklearn import linear_model

# TODO: Can maybe use a better dataset or manually select more points based on these and other points for colors
# [Valence, Energy]
X = [[0, 0], [0, 1], [1, 0], [1, 1]]

# [Hue]
y = [240, 0, 180, 60]

regr = linear_model.LinearRegression()
regr.fit(X, y)


def getBaseHue(valence, energy):
    return regr.predict([[valence, energy]])
