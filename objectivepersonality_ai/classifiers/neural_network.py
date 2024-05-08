import os
import keras
from keras import layers
from matplotlib import pyplot as plt
import numpy as np
from sklearn.model_selection import StratifiedKFold
from .classifier_model import ClassifierModel


class NeuralNetworkClassifier(ClassifierModel):

    def __init__(self, plot_history=False):
        self.plot_history = plot_history

    def build_classification_model(self, input_size: int) -> keras.Model:
        inputs = x = keras.Input(shape=(input_size,))
        x = layers.Dense(input_size, activation="relu")(x)
        x = layers.Dense(1, activation="sigmoid")(x)
        return keras.Model(inputs=[inputs], outputs=x)

    def _evaluate(self, X, y, coin):
        kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        histories = {}
        callback = keras.callbacks.EarlyStopping(monitor="accuracy", patience=3)
        for fold, (train_index, test_index) in enumerate(kf.split(X, y)):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]

            model = self.build_classification_model(X.shape[1])
            model.compile(
                optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"]
            )

            history = model.fit(
                X_train,
                y_train,
                epochs=10,
                batch_size=32,
                verbose=0,
                validation_data=(X_test, y_test),
                callbacks=[callback],
            )

            histories[f"Fold {fold+1}"] = {
                "loss": history.history["loss"],
                "val_loss": history.history["val_loss"],
                "accuracy": history.history["accuracy"],
                "val_accuracy": history.history["val_accuracy"],
            }

        if self.plot_history:
            self.plot_history(histories, coin)

        mean_accuracy = np.mean(
            [history["val_accuracy"][-1] for history in histories.values()]
        )
        return mean_accuracy

    def plot_history(self, histories, coin_name):
        fig, axs = plt.subplots(2, figsize=(10, 10), sharex=True)
        for i, (label, history) in enumerate(histories.items()):
            axs[0].plot(history["loss"], label=f"Train Fold {i+1}")
            axs[0].plot(
                history["val_loss"], linestyle="--", label=f"Validation Fold {i+1}"
            )
            axs[1].plot(history["accuracy"], label=f"Train Fold {i+1}")
            axs[1].plot(
                history["val_accuracy"], linestyle="--", label=f"Validation Fold {i+1}"
            )

        axs[0].set_title("Model Loss")
        axs[0].set_ylabel("Loss")
        axs[0].legend()

        axs[1].set_title("Model Accuracy")
        axs[1].set_ylabel("Accuracy")
        axs[1].set_xlabel("Epoch")
        axs[1].legend()

        plt.savefig(f"plots/{coin_name}_learning_curves.png")
        plt.close()

    def _build_from_dataset(self, X, y, coin, save=False):
        callback = keras.callbacks.EarlyStopping(monitor="accuracy", patience=3)
        self.model = self.build_classification_model(X.shape[1])
        self.model.compile(
            optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"]
        )
        # Train the model on the entire dataset
        self.model.fit(X, y, epochs=10, batch_size=32, verbose=0, callbacks=[callback])
        if save:
            self.save_model(coin)

    def save_model(self, coin_name):
        if self.model is not None:
            model_dir = "models"
            os.makedirs(model_dir, exist_ok=True)
            model_path = os.path.join(model_dir, f"{coin_name}_model.keras")
            self.model.save(model_path)
            print(f"Model saved to {model_path}")
        else:
            print("Model is None. Cannot save.")
