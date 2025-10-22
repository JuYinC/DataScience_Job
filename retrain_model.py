import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pickle

print("Loading data...")
df = pd.read_csv('data_cleaned.csv')

# Selecting relevant features
features = ['Rating','Size','Type of ownership','Industry','Sector','Revenue','State','age','python','excel','aws','sql','tableau','spark','machine learning',
            'job_simp','employee_expriece','desc_len']
target = 'avg_salary'

print("Handling missing values...")
# Handle missing values by filling with the mode for categorical columns and mean for numeric columns
for feature in features:
    if df[feature].dtype == 'object':
        df[feature].fillna(df[feature].mode()[0], inplace=True)
    else:
        df[feature].fillna(df[feature].mean(), inplace=True)

print("Encoding categorical variables...")
# Convert categorical variables using one-hot encoding
data_encoded = pd.get_dummies(df[features], drop_first=True)

print("Splitting data into train/test sets...")
# Splitting data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(data_encoded, df[target], test_size=0.2, random_state=42)

print("Training Random Forest model with GridSearch...")
# Hyperparameters grid for Random Forest
rf_params = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Grid search with cross-validation for Random Forest
rf_grid = GridSearchCV(RandomForestRegressor(random_state=42), rf_params, cv=5, scoring='neg_mean_absolute_error', n_jobs=-1, verbose=1)
rf_grid.fit(X_train, y_train)

# Best parameters and score for Random Forest
print(f"\nBest parameters: {rf_grid.best_params_}")
print(f"Best cross-validation MAE: {-rf_grid.best_score_:.2f}")

# Get the best model
rf_best_model = rf_grid.best_estimator_

# Evaluate on test set
rf_test_predictions = rf_best_model.predict(X_test)
rf_mae_test = mean_absolute_error(y_test, rf_test_predictions)
rf_rmse_test = np.sqrt(mean_squared_error(y_test, rf_test_predictions))

print(f"\nTest Set Performance:")
print(f"MAE: {rf_mae_test:.2f}")
print(f"RMSE: {rf_rmse_test:.2f}")

# Save the model with feature names and example data
print("\nSaving model to FlaskAPI/models/model_file.p...")
pickl = {
    'model': rf_best_model,
    'feature_names': list(data_encoded.columns),
    'example_features': features
}
pickle.dump(pickl, open('FlaskAPI/models/model_file.p', "wb"))

print("\n✓ Model retrained and saved successfully!")
print(f"Scikit-learn version: {__import__('sklearn').__version__}")
