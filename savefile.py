import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Step 1: Load the dataset
data = pd.read_csv('heart.csv')  # Ensure heart.csv is in the same directory

# Step 2: Define features and target
X = data.iloc[:, :-1].values  # All columns except the last as features
y = data["target"].values     # Last column as the target

# Step 3: Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Step 4: Scale the features
scaler = StandardScaler().fit(X_train)  # Fit scaler on the training data

# Save the scaler for later use
joblib.dump(scaler, 'scaler.save')
