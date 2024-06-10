import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
from .classifier_model import ClassifierModel

class RandomForestClassifierModel(ClassifierModel):

    def __init__(self, plot_history=False):
        self.plot_history = plot_history

    def build_classification_model(self) -> RandomForestClassifier:
        return RandomForestClassifier(n_estimators=100, random_state=42)

    def _evaluate(self, X, y, coin, X_tokens_size):
        kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        histories = {}

        accuracies = []
        for fold, (train_index, test_index) in enumerate(kf.split(X, y)):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]

            model = self.build_classification_model()
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            accuracies.append(accuracy)

            histories[f"Fold {fold+1}"] = accuracy

        if self.plot_history:
            self.plot_history(histories, coin)

        mean_accuracy = np.mean(accuracies)
        return mean_accuracy

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
