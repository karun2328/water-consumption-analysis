import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.linear_model import LinearRegression
import numpy as np
def load_data():
    df = pd.read_csv('cleaned_global_water_consumption.csv')
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    return df

def total_consumption_trend(df):
    global_trend = df.groupby('Year')['Total Water Consumption (Billion Cubic Meters)'].sum()
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=global_trend.index, y=global_trend.values)
    plt.title('Global Total Water Consumption Over Time')
    plt.xlabel('Year')
    plt.ylabel('Total Water Consumption (Billion Cubic Meters)')
    plt.savefig('graphs/total_water_consumption_trend.png', bbox_inches='tight')
    plt.show()

def rainfall_vs_consumption(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Rainfall Impact (Annual Precipitation in mm)',
                    y='Total Water Consumption (Billion Cubic Meters)',
                    data=df)
    plt.title('Rainfall Impact vs. Total Water Consumption')
    plt.xlabel('Rainfall Impact (Annual Precipitation in mm)')
    plt.ylabel('Total Water Consumption (Billion Cubic Meters)')
    plt.savefig('graphs/rainfall_vs_total_consumption.png', bbox_inches='tight')
    plt.show()

    corr = df['Rainfall Impact (Annual Precipitation in mm)'].corr(
        df['Total Water Consumption (Billion Cubic Meters)']
    )
    print(f' Correlation between Rainfall Impact and Total Water Consumption: {corr:.2f}')

def sector_usage_trend(df):
    sector_trend = df.groupby('Year')[
        ['Agricultural Water Use (%)', 'Industrial Water Use (%)', 'Household Water Use (%)']
    ].mean()
    plt.figure(figsize=(10, 6))
    sector_trend.plot()
    plt.title('Average Sector-wise Water Use Over Time')
    plt.xlabel('Year')
    plt.ylabel('Percentage of Total Water Use')
    plt.savefig('graphs/sector_usage_trend.png', bbox_inches='tight')
    plt.show()

def per_capita_usage_trend(df):
    cap_trend = df.groupby('Year')['Per Capita Water Use (Liters per Day)'].mean()
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=cap_trend.index, y=cap_trend.values)
    plt.title('Per Capita Water Use Over Time')
    plt.xlabel('Year')
    plt.ylabel('Per Capita Water Use (Liters per Day)')
    plt.savefig('graphs/per_capita_usage_trend.png', bbox_inches='tight')
    plt.show()

    X = np.array(cap_trend.index).reshape(-1, 1)
    y = cap_trend.values
    model = LinearRegression()
    model.fit(X, y)
    future_years = np.arange(cap_trend.index.max() + 1, cap_trend.index.max() + 6).reshape(-1, 1)
    future_preds = model.predict(future_years)

    print("Predicted Per Capita Water Use for next 5 years:")
    for year, pred in zip(future_years.flatten(), future_preds):
        print(f"Year {year}: {pred:.2f} Liters per Day")

def correlation_heatmap(df):
    numeric_cols = df.select_dtypes(include=['float64', 'int64'])
    corr = numeric_cols.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap of Numeric Variables')
    plt.savefig('graphs/correlation_heatmap.png', bbox_inches='tight')
    plt.show()

# MAIN program
if __name__ == "__main__":
    df = load_data()
    print(" Data loaded successfully.\n")

    total_consumption_trend(df)
    rainfall_vs_consumption(df)
    sector_usage_trend(df)
    per_capita_usage_trend(df)
    correlation_heatmap(df)



