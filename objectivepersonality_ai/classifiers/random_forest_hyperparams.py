import os
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, GridSearchCV, ShuffleSplit, StratifiedShuffleSplit, cross_validate
from sklearn.metrics import accuracy_score, classification_report, balanced_accuracy_score
from imblearn.pipeline import Pipeline
import matplotlib.pyplot as plt
from .classifier_model import ClassifierModel
from imblearn.over_sampling import SMOTE

class RandomForestClassifierModel(ClassifierModel):

    def __init__(self, plot_history=False):
        self.save_plot_history = plot_history

    def build_classification_model(self) -> RandomForestClassifier:
        return RandomForestClassifier(
            n_estimators=100,  # Start with a reasonable number of trees
            # max_depth=5,       # Limit tree depth to prevent overfitting
            # min_samples_split=5,  # Require a minimum number of samples to split a node
            # min_samples_leaf=2,  # Require a minimum number of samples in a leaf
            class_weight="balanced",  # Handle imbalanced classes (if applicable)
            random_state=42    # For reproducibility
        )

    def _evaluate(self, X, y, coin, X_tokens_size):

        pipeline = Pipeline(
            steps=[
                ('smote', SMOTE()),
                (
                    'classifier',
                    RandomForestClassifier(
                        n_estimators=100, class_weight="balanced", random_state=42
                    ),
                ),
            ]
        )

        param_grid = {
            'classifier__n_estimators': [50, 100, 150],
            'classifier__max_depth': [None, 10, 20],
            'classifier__min_samples_split': [2, 5, 10],
            'classifier__min_samples_leaf': [1, 2, 4],
            'classifier__class_weight': ["balanced", None]
        }

        grid_search = GridSearchCV(pipeline, param_grid=param_grid, cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42), scoring=['accuracy', 'f1'], refit='f1')  # Use 'f1' as refit criteria

        grid_search.fit(X, y)

        best_params = grid_search.best_params_
        best_estimator = grid_search.best_estimator_

        # Cross-validation with Best Model
        skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
        scores = cross_validate(best_estimator, X, y, cv=skf, scoring=['accuracy', 'f1'])

        # Evaluate results
        print(f"Best parameters: {best_params}")
        print(f"Mean accuracy: {scores['test_accuracy'].mean()}")
        print(f"Mean F1-score: {scores['test_f1'].mean()}")

        return scores['test_accuracy'].mean()

    def plot_history(self, histories, coin_name):
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(list(histories.keys()), list(histories.values()), marker='o', linestyle='-')
        
        ax.set_title(f"Model Accuracy per Fold for {coin_name}")
        ax.set_ylabel("Accuracy")
        ax.set_xlabel("Fold")
        ax.legend(["Accuracy"])

        plt.savefig(f"plots/{coin_name}_accuracy.png")
        plt.close()

    def _build_from_dataset(self, X, y, coin, X_tokens_size, save=False):
        self.model = self.build_classification_model()
        self.model.fit(X, y)
        if save:
            self.save_model(coin)

    def save_model(self, coin_name):
        if self.model is not None:
            model_dir = "models"
            os.makedirs(model_dir, exist_ok=True)
            model_path = os.path.join(model_dir, f"{coin_name}_model.pkl")
            joblib.dump(self.model, model_path)
            print(f"Model saved to {model_path}")
        else:
            print("Model is None. Cannot save.")
