from abc import abstractmethod
import ast
import os
from dotenv import load_dotenv, find_dotenv
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.discriminant_analysis import StandardScaler
from sklearn.model_selection import StratifiedKFold

from ops.ops import COINS_AUXILIARY, COINS_DICT

_ = load_dotenv(find_dotenv(usecwd=False, raise_error_if_not_found=True))

TRANSCRIPTS_WITH_EMBEDDINGS_CSV = os.getenv("TRANSCRIPTS_WITH_EMBEDDINGS_CSV")
if TRANSCRIPTS_WITH_EMBEDDINGS_CSV is None:
    raise ValueError("TRANSCRIPTS_WITH_EMBEDDINGS_CSV environment variable is not set")


coins = COINS_DICT | COINS_AUXILIARY

class ClassifierModel:

    @abstractmethod
    def _build_from_dataset(X, y, coin):
      pass
        
    @abstractmethod
    def _evaluate(X, y, coin):
      pass

    def build_from_dataset(self, save=False):
      df = self.load_data()
      X = np.array([ast.literal_eval(emb) if isinstance(emb, str) else emb for emb in df['embeddings']])

      for coin, classes in coins.items():
          y = df[coin].apply(lambda x: classes.index(x)).values

          # Scale features for neural network suitability
          # scaler = StandardScaler()
          # X = scaler.fit_transform(X)

          mean_accuracy = self._build_from_dataset(X, y, coin, save=save)
          print(f"Coin {coin}, average accuracy: {mean_accuracy}")


    def evaluate(self):
      df = self.load_data()
      X = np.array([ast.literal_eval(emb) if isinstance(emb, str) else emb for emb in df['embeddings']])

      for coin, classes in coins.items():
          y = df[coin].apply(lambda x: classes.index(x)).values

          # Scale features for neural network suitability
          # scaler = StandardScaler()
          # X = scaler.fit_transform(X)

          mean_accuracy = self._evaluate(X, y, coin)
          print(f"Coin {coin}, average accuracy: {mean_accuracy}")


    def load_data(self) -> pd.DataFrame:
      df = pd.read_csv(TRANSCRIPTS_WITH_EMBEDDINGS_CSV)

      df['ObserverAxis'] = np.select(
          [
              (df['OiOe'] == 'Oi') & (df['SN'] == 'S'),
              (df['OiOe'] == 'Oi') & (df['SN'] == 'N'),
              (df['OiOe'] == 'Oe') & (df['SN'] == 'S'),
              (df['OiOe'] == 'Oe') & (df['SN'] == 'N')
          ],
          ['Ne/Si', 'Se/Ni', 'Se/Ni', 'Ne/Si'],
      )

      df['DeciderAxis'] = np.select(
          [
              (df['DiDe'] == 'Di') & (df['TF'] == 'T'),
              (df['DiDe'] == 'Di') & (df['TF'] == 'F'),
              (df['DiDe'] == 'De') & (df['TF'] == 'T'),
              (df['DiDe'] == 'De') & (df['TF'] == 'F')
          ],
          ['Fe/Ti', 'Te/Fi', 'Te/Fi', 'Fe/Ti'],
      )

      return df