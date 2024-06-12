from abc import abstractmethod
import ast
import os
from dotenv import load_dotenv, find_dotenv
import numpy as np
import pandas as pd
from sklearn.utils import resample
from imblearn.over_sampling import SMOTE

from objectivepersonality_ai.ops import COINS_AUXILIARY, COINS_DICT

_ = load_dotenv(find_dotenv(usecwd=False, raise_error_if_not_found=True))

TRANSCRIPTS_WITH_EMBEDDINGS_CSV = os.getenv("SAVIORS_AND_DEMONS_WITH_EMBEDDINGS_CSV")
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

        if "transcript_tokens_length" not in df.columns:
            df["transcript_tokens_length"] = 1

        X_tokens_size = df["transcript_tokens_length"].values

        for coin, classes in coins.items():
            y = df[coin].apply(lambda x: classes.index(x)).values
            # Balance the dataset
            # X_balanced, y_balanced, X_tokens_size_balanced = X, y, X_tokens_size
            X_balanced, y_balanced, X_tokens_size_balanced = self.oversampling(
                X, y, X_tokens_size
            )

            mean_accuracy = self._build_from_dataset(X_balanced, y_balanced, coin, X_tokens_size, save=save)
            print(f"Coin {coin}, average accuracy: {mean_accuracy}")

    def evaluate(self):
        df = self.load_data()
        X = np.array(
            [
                ast.literal_eval(emb) if isinstance(emb, str) else emb
                for emb in df["embeddings"]
            ]
        )
        
        if "transcript_tokens_length" not in df.columns:
            df["transcript_tokens_length"] = 1

        X_tokens_size = df["transcript_tokens_length"].values

        for coin, classes in coins.items():
            y = df[coin].apply(lambda x: classes.index(x)).values
            # Balance the dataset
            # X_balanced, y_balanced, X_tokens_size_balanced = X, y, X_tokens_size
            X_balanced, y_balanced, X_tokens_size_balanced = self.oversampling(
                X, y, X_tokens_size
            )

            mean_accuracy = self._evaluate(X_balanced, y_balanced, coin, X_tokens_size_balanced)
            print(f"Coin {coin}, average accuracy: {mean_accuracy}")

    def oversampling(self, X, y, X_tokens_size):
        smote = SMOTE()
        X_balanced, y_balanced = smote.fit_resample(X, y)
        X_tokens_size_balanced = np.ones(X_balanced.shape[0])

        return X_balanced, y_balanced, X_tokens_size_balanced

    def undersampling(self, X, y, weights):
        # Combine data
        data = np.column_stack((X, y, weights))
        
        # Separate classes
        class_0 = data[data[:, -2] == 0]
        class_1 = data[data[:, -2] == 1]
        
        # Sort classes by weights (last column)
        class_0 = class_0[class_0[:, -1].argsort()]
        class_1 = class_1[class_1[:, -1].argsort()]
        
        # Find minority size
        minority_size = min(len(class_0), len(class_1))
        
        # Keep the highest-weighted entries for balancing
        class_0_balanced = class_0[-minority_size:]
        class_1_balanced = class_1[-minority_size:]
        
        # Combine balanced classes
        balanced_data = np.vstack((class_0_balanced, class_1_balanced))
        
        # Split balanced data
        X_balanced = balanced_data[:, :-2]
        y_balanced = balanced_data[:, -2].astype(int)
        weights_balanced = balanced_data[:, -1]
        
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
