from sklearn.linear_model import Ridge

def train_surrogate(X, y, weights):
    model = Ridge(alpha=1.0)
    model.fit(X, y, sample_weight=weights)
    return model
