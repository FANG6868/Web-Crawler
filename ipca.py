import pandas as pd
import numpy as np
from sklearn.decomposition import IncrementalPCA
from sklearn.preprocessing import StandardScaler

# Load the data
df = pd.read_stata('E:\\FangLin\\Taobao\\Finance\\1.dta')

# Subset the relevant columns for IPCA
returns = df.drop(['code', 'year', 'month'], axis=1)

# Drop rows with missing values
returns = returns.dropna()

# Identify non-numerical columns
non_numerical_columns = returns.select_dtypes(exclude=[np.number]).columns

# Drop non-numerical columns
returns = returns.drop(non_numerical_columns, axis=1)

# Standardize the data
scaler = StandardScaler()
returns_scaled = pd.DataFrame(scaler.fit_transform(returns), columns=returns.columns)

# Define the IPCA model
n_components = 10  # Change this to your desired number of components
batch_size = 500  # Adjust this based on your memory capacity and dataset size
ipca = IncrementalPCA(n_components=n_components, batch_size=batch_size)

# Fit the model and transform the data in batches
components = None
for i in range(0, len(returns_scaled), batch_size):
    batch = returns_scaled.iloc[i:i+batch_size]
    batch_transformed = ipca.fit_transform(batch)
    if components is None:
        components = batch_transformed
    else:
        components = np.concatenate((components, batch_transformed), axis=0)

# Create a DataFrame for the transformed components
components_df = pd.DataFrame(components, columns=[f'PC{i+1}' for i in range(n_components)])

# Calculate R-square
explained_variance_ratio = ipca.explained_variance_ratio_
r_squared = np.sum(explained_variance_ratio[:n_components])
print(f"R-Square: {r_squared}")

# Assume a risk-free rate of 0, you need to adjust the risk-free rate
risk_free_rate = 0

# Calculate excess returns by subtracting the risk-free rate from the first principal component
excess_returns = components_df['PC1'] - risk_free_rate

# Calculate the Sharpe Ratio
sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns)
print(f"Sharpe Ratio: {sharpe_ratio}")

# Get the absolute loadings of the first principal component
importances = np.abs(ipca.components_[0])

# Create a dictionary to associate each characteristic with its importance score
characteristic_importance = dict(zip(returns.columns, importances))

# Sort the characteristics based on their importance scores in descending order
sorted_characteristic_importance = sorted(characteristic_importance.items(), key=lambda x: x[1], reverse=True)

# Display the importance scores for each characteristic
for characteristic, importance_score in sorted_characteristic_importance:
    print(f"{characteristic}: {importance_score}")

# Print the components DataFrame
print(components_df)
