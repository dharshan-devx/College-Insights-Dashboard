import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import logging
import os
from src.load_data import load_all_data

# Set up logging for clear, informative feedback
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_prediction_model(df):
    """
    Trains a logistic regression model to predict student pass/fail status
    and saves the trained model to the outputs folder.

    Args:
        df (pd.DataFrame): The main DataFrame containing student data.
    
    Returns:
        tuple or None: A tuple containing the trained model, test features, and test target,
                       or None if an error occurs.
    """
    output_dir = 'outputs/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. Define Features (X) and Target (y)
    features = ['attendance', 'marks']
    target = 'pass_status'

    if not all(col in df.columns for col in features + [target]):
        logging.error("❌ Required columns not found in DataFrame.")
        return None

    X = df[features]
    y = df[target].map({'Pass': 1, 'Fail': 0})  # Encode target: Pass=1, Fail=0

    # 2. Split the Data
    # Stratify=y ensures the training and test sets have the same proportion of classes as the original dataset.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    logging.info(f"Data split into training ({len(X_train)} samples) and testing ({len(X_test)} samples).")

    # 3. Initialize and Train the Model
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    logging.info("✅ Logistic Regression model trained successfully.")

    # 4. Evaluate the Model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=['Fail', 'Pass'])

    logging.info("\n🧠 Model Evaluation Results:")
    logging.info(f"Accuracy on test set: {accuracy:.2f}")
    logging.info(f"Classification Report:\n{report}")

    # 5. Save the Trained Model
    model_path = os.path.join(output_dir, 'model.pkl')
    try:
        joblib.dump(model, model_path)
        logging.info(f"💾 Trained model successfully saved to: {model_path}")
    except Exception as e:
        logging.error(f"❌ Failed to save model: {e}")
        
    return model, X_test, y_test

if __name__ == '__main__':
    # This block allows for direct execution to train the model and save it
    df = load_all_data(path='../data/')
    if df is not None:
        train_prediction_model(df)