import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score, KFold
from sklearn.base import clone

# Load Data
df = pd.read_excel("merged_data_with_day_of_year.xlsx")

temp_cols = ['Temperature'] + [f'Temperature_{i}d_ago' for i in range(1, 6)] # Get all temp columns including lags
df_imputed = df.copy() # Create a copy for filling in the missing data

# Impute each temperature column using polynomial regression (with cross-validation and lasso)
for col in temp_cols: 
    print(f"Evaluating best polynomial degree for {col}...")
    known = df[df[col].notna()] # Get known data (non-missing values)
    missing = df[df[col].isna()] # Get missing data
    X = known[['day_of_year']].values # We want to predict the temperature based on the day of the year
    y = known[col].values # The known temperature values

    # Select best degree
    degrees = range(2, 7)  # Try polynomial degrees 2 through 6
    best_score = -np.inf
    best_degree = None

    for d in degrees:
        model = Lasso(alpha=0.1, max_iter=10000) # Regularize with lasso
        scores = [] 
        kf = KFold(n_splits=5) # 5-fold cross-validation
        
        for train_index, test_index in kf.split(X): # Run for each fold
            X_train, X_test = X[train_index], X[test_index] # Split the data into training and testing sets
            y_train, y_test = y[train_index], y[test_index] 

            poly = PolynomialFeatures(d) # Create polynomial features
            X_train_poly = poly.fit_transform(X_train) # Map the training data to polynomial features (kernelize)
            X_test_poly = poly.transform(X_test) # Map the testing data to polynomial features (don't fit again because this is the testing data)

            model_fold = clone(model) 
            model_fold.fit(X_train_poly, y_train) # Fit the model to the kernelized training data
            y_predict = model_fold.predict(X_test_poly) # Predict the testing output using the fitted model
            error = np.mean((y_test - y_predict) ** 2) # Calculate the mean squared error
            scores.append(error)

        mean_score = np.mean(scores) 
        print(f"Degree {d}: Avg MSE = {mean_score:.4f}") # Print the average mean squared error for this degree

        if mean_score < best_score or best_degree is None:  # Check to see if this is the best score so far
            best_score = mean_score
            best_degree = d

    print(f"Best degree for {col}: {best_degree} (Avg MSE = {best_score:.4f})") 

    # Fit final model
    final_model = PolynomialFeatures(best_degree) # Create polynomial features with the best degree
    X_poly = final_model.fit_transform(X) # Transform X to polynomial features
    model = Lasso(alpha=0.1, max_iter=10000) # Regularize with lasso
    model.fit(X_poly, y) # Fit the model to the known data
    print(f"Fitting final model for {col} with degree {best_degree}...")

    # Impute missing values
    X_missing = missing[['day_of_year']].values # Get the missing data
    X_missing_poly = final_model.transform(X_missing) # Transform the missing data to polynomial features
    y_missing = model.predict(X_missing_poly) # Predict the missing values
    df_imputed.loc[df_imputed[col].isna(), col] = y_missing # Fill in the missing values
    print(f"Imputed {col} using polynomial degree {best_degree} and Lasso regression.")

# Save result 
df_imputed.to_excel("imputed_temperature_columns_by_day_poly_lasso_cv.xlsx", index=False)
print("All temperature columns imputed using cross-validated polynomial + Lasso regression.")
