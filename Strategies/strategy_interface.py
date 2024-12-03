from abc import ABC, abstractmethod
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

class TradingStrategy(ABC):
    def __init__(self, stop_loss, smoothing_period=14):
        """
        Initialize the trading strategy with stop_loss and smoothing_period.
        The smoothing_period is used for smoothing indicators like macd, rsi, etc.
        """
        self.stop_loss = stop_loss  # Shared functionality, for example, stop loss
        self.smoothing_period = smoothing_period  # Smoothing period for indicators
        self.model = RandomForestClassifier(class_weight='balanced')  # Common model for all strategies

    def execute_strategy(self, row, df):
        """
        Template method to execute the strategy workflow.
        1. Label data
        2. Train the model
        3. Extract features
        4. Decide action
        """
        # Step 1: Label data
        df = self.label_data(df, self.label_logic)

        # Step 2: Train the model
        self.train_model(df, self.feature_columns(), self.label_logic)

        # Step 3: Extract features for prediction
        features = self._get_features(row, self.feature_columns())

        # Step 4: Decide action
        action = self.decide_action(features)
        return action

    @abstractmethod
    def label_logic(self, row):
        """Abstract method to provide labeling logic for the strategy."""
        pass

    @abstractmethod
    def feature_columns(self):
        """Abstract method to provide feature column names for the strategy."""
        pass

    def decide_action(self, features):
        """Common decision-making logic using the trained model."""
        prediction = self.model.predict(features)[0]
        print(f"Predicted action: {prediction}")
        return prediction

    def label_data(self, df, label_logic):
        """Apply labeling logic to the DataFrame."""
        labels = [label_logic(row) for _, row in df.iterrows()]
        df['Action'] = labels
        return df

    def train_model(self, df, features_list, label_logic):
        """Train the model on historical data."""
        # Extract features and labels
        features = df[features_list]
        labels = df['Action']
        self.model.fit(features, labels)

    def _get_features(self, row, features_list):
        """Extract features for prediction as a DataFrame."""
        return pd.DataFrame([row[features_list]], columns=features_list)
