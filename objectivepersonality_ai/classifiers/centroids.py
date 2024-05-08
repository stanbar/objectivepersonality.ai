import os
import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from scipy.spatial.distance import cdist

from .classifier_model import ClassifierModel


class CentroidsClassifier(ClassifierModel):
    def build_classification_model(self, X, y):
        # With binary classification, we always have two classes: 0 and 1
        prototypes = np.zeros((2, X.shape[1]))
        for i in range(
            2
        ):  # Directly use 2 instead of num_classes for binary classification
            prototypes[i] = X[y == i].mean(axis=0)
        return prototypes

    def classify_prototypes(self, X, prototypes):
        # Calculate distances to prototypes using cosine distance
        distances = cdist(X, prototypes, "cosine")
        # Assign labels based on the closest prototype
        return np.argmin(distances, axis=1)

    def _evaluate(self, X, y, coin):
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        accuracies = []

        for train_index, test_index in kf.split(X):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]

            prototypes = self.build_classification_model(X_train, y_train)
            y_pred = self.classify_prototypes(X_test, prototypes)
            accuracies.append(accuracy_score(y_test, y_pred))

        # Cross-validation mean accuracy
        return np.mean(accuracies)

    def _build_from_dataset(self, X, y, coin, save=False):
        # Final model evaluation with a different split
        prototypes = self.build_classification_model(X, y)

        if save:
            self.save_model(coin, prototypes)

    def save_model(self, coin_name, prototypes):
        if prototypes is not None:
            model_dir = "proto_models"
            os.makedirs(model_dir, exist_ok=True)
            model_path = os.path.join(model_dir, f"{coin_name}_proto_model.pt")
            np.save(model_path, prototypes)
            print(f"Model saved to {model_path}")
        else:
            print("Model is None. Cannot save.")
