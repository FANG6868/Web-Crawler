import pandas as pd
import statsmodels.api as sm
import numpy as np

# Load the data
df = pd.read_stata('E:/FangLin/Taobao/Finance/2.dta')

# Create a datetime column combining 'year' and 'month'
df['Date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

# Calculate the excess return for the market
df['Excess Market Return'] = df['market_premium'] - df['riskfree']

# Get unique stock names
stocks = df['code'].unique()

# Initialize a result dataframe
result_df = pd.DataFrame(columns=['Stock', 'Alpha', 'Beta', 'R-squared', 'Sharpe Ratio'])

# Loop through each stock
for stock in stocks:
    # Subset dataframe for the current stock
    df_stock = df[df['code'] == stock].copy()

    # Calculate the excess return for the stock
    df_stock['Excess Stock Return'] = df_stock['return'] - df_stock['riskfree']

    # Skip stocks with fewer than two data points
    if len(df_stock) < 2:
        continue

    # Define the independent variable (market excess return) and add a constant (for the intercept term)
    X = sm.add_constant(df_stock['Excess Market Return'])

    # Define the dependent variable (stock excess return)
    Y = df_stock['Excess Stock Return']

    # Run the OLS regression
    model = sm.OLS(Y, X)
    results = model.fit()

    # Check if the stock has sufficient data points for regression
    if len(results.params) < 2:
        continue

    # Get the alpha (intercept) and beta (slope)
    alpha = results.params[0]
    beta = results.params[1]

    # Get the R-squared
    rsquared = results.rsquared

    # Calculate the Sharpe Ratio
    sharpe_ratio = np.mean(df_stock['Excess Stock Return']) / np.std(df_stock['Excess Stock Return'])

    # Append the result to result dataframe
    new_row = pd.DataFrame({'Stock': [stock], 'Alpha': [alpha], 'Beta': [beta], 'R-squared': [rsquared], 'Sharpe Ratio': [sharpe_ratio]})
    result_df = pd.concat([result_df, new_row], ignore_index=True)

# Print the result
print(result_df)

mean_r_squared = result_df['R-squared'].mean()
mean_sharpe_ratio = result_df['Sharpe Ratio'].mean()

print('Mean R-squared:', mean_r_squared)
print('Mean Sharpe Ratio:', mean_sharpe_ratio)