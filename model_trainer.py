import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# Load the processed data
df = pd.read_csv('processed_energy_data.csv')

# Split into features and target
X = df.drop('ElectricityBill', axis=1)
y = df['ElectricityBill']

# Identify categorical columns
categorical_cols = ['City', 'Company']
numerical_cols = [col for col in X.columns if col not in categorical_cols]

# Define preprocessing: OneHotEncode categorical features
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols),
    ],
    remainder='passthrough'  # Pass through other columns unchanged
)

# Combine preprocessing and model in a pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', RandomForestRegressor(random_state=42))
])

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define hyperparameters for tuning
param_grid = {
    'model__n_estimators': [100, 150],
    'model__max_depth': [None, 20],
    'model__min_samples_split': [2, 5],
    'model__min_samples_leaf': [1, 2],
    'model__bootstrap': [True]
}

# GridSearch with cross-validation
grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, verbose=2, scoring='neg_mean_absolute_error')
grid_search.fit(X_train, y_train)

print(f'Best Hyperparameters: {grid_search.best_params_}')

# Get the best model pipeline
best_pipeline = grid_search.best_estimator_

# Predict and evaluate
y_pred = best_pipeline.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'MAE: {mae}')
print(f'MSE: {mse}')
print(f'R²: {r2}')

# Save the pipeline (encoder + model together)
joblib.dump(best_pipeline, 'energy_model_pipeline.pkl')
print("Pipeline saved as 'energy_model_pipeline.pkl'")
