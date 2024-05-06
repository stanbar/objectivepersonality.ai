import os
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from .classifier_model import ClassifierModel

class PrototypicalNetwork(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(PrototypicalNetwork, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_size, 1024),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(1024, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, 1)  # Output a single logit for binary classification
        )
        
    def forward(self, x):
        return self.fc(x)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class ProtoNetworksClassifier(ClassifierModel):

    model: PrototypicalNetwork

    def build_classification_model(self, input_size: int) -> PrototypicalNetwork:
        self.model = PrototypicalNetwork(input_size, 1024).to(device)
        return self.model


    def _evaluate(self, X, y, coin):
        kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        accuracies = []
        for fold, (train_index, test_index) in enumerate(kf.split(X, y)):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]

            model = self.build_classification_model(X.shape[1])
            optimizer = optim.Adam(model.parameters(), lr=0.001)
            criterion = nn.BCEWithLogitsLoss()  # Use Binary Cross-Entropy with logits

            dataset = TensorDataset(torch.Tensor(X_train), torch.Tensor(y_train))
            loader = DataLoader(dataset, batch_size=20, shuffle=True)
            
            model.train()
            for epoch in range(100):
                for data, target in loader:
                    data, target = data.to(device), target.to(device)
                    optimizer.zero_grad()
                    logits = model(data)
                    loss = criterion(logits.view(-1), target.float())  # Ensure the target is float and logits are squeezed
                    loss.backward()
                    optimizer.step()
        
            y_pred = self.predict(model, X_test)
            accuracy = accuracy_score(y_test, y_pred)
            accuracies.append(accuracy)

        return np.mean(accuracies)


    def predict(self, net, X_test):
        net.to(device)
        net.eval()
        with torch.no_grad():
            X_test_tensor = torch.Tensor(X_test).to(device)
            logits = net(X_test_tensor)
            predictions = torch.sigmoid(logits).round()  # Sigmoid and round to get binary predictions
            return predictions.cpu().numpy()


    def _build_from_dataset(self, X, y, coin, save=False):
        self.model = self.build_classification_model(X.shape[1])
        optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        criterion = nn.BCEWithLogitsLoss()  # Use Binary Cross-Entropy with logits

        dataset = TensorDataset(torch.Tensor(X), torch.Tensor(y))
        loader = DataLoader(dataset, batch_size=20, shuffle=True)
        
        self.model.train()
        for epoch in range(100):
            for data, target in loader:
                data, target = data.to(device), target.to(device)
                optimizer.zero_grad()
                logits = self.model(data)
                loss = criterion(logits.view(-1), target.float())  # Ensure the target is float and logits are squeezed
                loss.backward()
                optimizer.step()
    
        if save:
            self.save_model(coin)



    def save_model(self, coin_name):
        if self.model is not None:
            model_dir = "proto_models"
            os.makedirs(model_dir, exist_ok=True)
            model_path = os.path.join(model_dir, f"{coin_name}_proto_model.pt")
            torch.save(self.model.state_dict(), model_path)
            print(f"Model saved to {model_path}")
        else:
            print("Model is None. Cannot save.")