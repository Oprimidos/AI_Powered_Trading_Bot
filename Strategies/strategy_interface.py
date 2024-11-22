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
        self.is_trained = False  # To track whether the model has been trained

    @abstractmethod
    def decide_action(self, row, df):
        """Abstract method to decide action based on strategy."""
        pass

    def _get_features(self, row, features_list):
        """Common feature extraction method."""
        # Return as a DataFrame to preserve feature names
        return pd.DataFrame([row[features_list]], columns=features_list)

    def label_data(self, df, label_logic):
        """
        Method to label the data based on the specific strategy's logic.
        This is implemented in the strategy class.
        """
        labels = []
        for index, row in df.iterrows():
            labels.append(label_logic(row))  # Apply the strategy's labeling logic
        df['Action'] = labels
        return df

    def train_model(self, df, features_list, label_logic):
        """
        Trains the model on historical data with common logic.
        This method is used in the strategy class for training.
        """
        # Label the data using strategy-specific logic
        labeled_df = self.label_data(df, label_logic)

        # Extract features and labels
        features = labeled_df[features_list]
        labels = labeled_df['Action']

        # Train the model
        self.model.fit(features, labels)
        self.is_trained = True  # Mark the model as trained
