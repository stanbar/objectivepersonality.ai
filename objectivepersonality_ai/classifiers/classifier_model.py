from abc import abstractmethod
import ast
import os
from dotenv import load_dotenv, find_dotenv
import numpy as np
import pandas as pd
from sklearn.utils import resample


from objectivepersonality_ai.ops import COINS_AUXILIARY, COINS_DICT

_ = load_dotenv(find_dotenv(usecwd=False, raise_error_if_not_found=True))

TRANSCRIPTS_WITH_EMBEDDINGS_CSV = os.getenv("TRANSCRIPTS_WITH_EMBEDDINGS_CSV")
if TRANSCRIPTS_WITH_EMBEDDINGS_CSV is None:
    raise ValueError("TRANSCRIPTS_WITH_EMBEDDINGS_CSV environment variable is not set")


coins = COINS_DICT | COINS_AUXILIARY


class ClassifierModel:

    @abstractmethod
    def _build_from_dataset(self, X, y, coin):
        pass

    @abstractmethod
    def _evaluate(self, X, y, coin):
        pass

    def build_from_dataset(self, save=False):
        df = self.load_data()
        X = np.array(
            [
                ast.literal_eval(emb) if isinstance(emb, str) else emb
                for emb in df["embeddings"]
            ]
        )

        X_tokens_size = df["transcript_tokens_length"].values

        for coin, classes in coins.items():
            y = df[coin].apply(lambda x: classes.index(x)).values

            # Scale features for neural network suitability
            # scaler = StandardScaler()
            # X = scaler.fit_transform(X)

            mean_accuracy = self._build_from_dataset(X, y, coin, X_tokens_size, save=save)
            print(f"Coin {coin}, average accuracy: {mean_accuracy}")

    def evaluate(self):
        df = self.load_data()
        X = np.array(
            [
                ast.literal_eval(emb) if isinstance(emb, str) else emb
                for emb in df["embeddings"]
            ]
        )
        
        X_tokens_size = df["transcript_tokens_length"].values

        for coin, classes in coins.items():
            y = df[coin].apply(lambda x: classes.index(x)).values
            # Balance the dataset
            X_balanced, y_balanced, X_tokens_size_balanced = self.balance_dataset(X, y, X_tokens_size)


            # Scale features for neural network suitability
            # scaler = StandardScaler()
            # X = scaler.fit_transform(X)

            mean_accuracy = self._evaluate(X_balanced, y_balanced, coin, X_tokens_size_balanced)
            print(f"Coin {coin}, average accuracy: {mean_accuracy}")

    def balance_dataset(self, X, y, weights):
        # Separate the majority and minority classes
        class_0_mask = (y == 0)
        class_1_mask = (y == 1)
        
        X_class_0 = X[class_0_mask]
        y_class_0 = y[class_0_mask]
        weights_class_0 = weights[class_0_mask]
        
        X_class_1 = X[class_1_mask]
        y_class_1 = y[class_1_mask]
        weights_class_1 = weights[class_1_mask]
        
        # Find the minority class size
        minority_size = min(len(y_class_0), len(y_class_1))
        
        # Undersample the majority class
        X_class_0_balanced, y_class_0_balanced, weights_class_0_balanced = resample(
            X_class_0, y_class_0, weights_class_0,
            replace=False,  # No oversampling
            n_samples=minority_size,
            random_state=42
        )
        
        X_class_1_balanced, y_class_1_balanced, weights_class_1_balanced = resample(
            X_class_1, y_class_1, weights_class_1,
            replace=False,  # No oversampling
            n_samples=minority_size,
            random_state=42
        )
        
        # Combine the balanced classes
        X_balanced = np.vstack((X_class_0_balanced, X_class_1_balanced))
        y_balanced = np.hstack((y_class_0_balanced, y_class_1_balanced))
        weights_balanced = np.hstack((weights_class_0_balanced, weights_class_1_balanced))
        
        return X_balanced, y_balanced, weights_balanced
    def load_data(self) -> pd.DataFrame:
        df = pd.read_csv(TRANSCRIPTS_WITH_EMBEDDINGS_CSV)

        df = df.dropna(subset=["embeddings"])

        df["ObserverAxis"] = np.select(
            [
                (df["OiOe"] == "Oi") & (df["SN"] == "S"),
                (df["OiOe"] == "Oi") & (df["SN"] == "N"),
                (df["OiOe"] == "Oe") & (df["SN"] == "S"),
                (df["OiOe"] == "Oe") & (df["SN"] == "N"),
            ],
            ["Ne/Si", "Se/Ni", "Se/Ni", "Ne/Si"],
        )

        df["DeciderAxis"] = np.select(
            [
                (df["DiDe"] == "Di") & (df["TF"] == "T"),
                (df["DiDe"] == "Di") & (df["TF"] == "F"),
                (df["DiDe"] == "De") & (df["TF"] == "T"),
                (df["DiDe"] == "De") & (df["TF"] == "F"),
            ],
            ["Fe/Ti", "Te/Fi", "Te/Fi", "Fe/Ti"],
        )

        return df
