import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Downloading and preparing data
df = pd.read_csv('D:\Programowanie\Workplace\Code\Data_Science_brick_by_brick\DataScienceSummerStudy\_machine_learning\_fundamentals\lifesat.csv')
print(df)
x = df[['GDP per capita (USD)']].values # 2 dimension data, DataFrame
y = df[['Life satisfaction']].values # 2 dimension data, DataFrame

# X = df['GDP per capita (USD)'].values # 1 dimension data

# Visualize data
df.plot(kind='scatter', x='GDP per capita (USD)', y='Life satisfaction', grid=True)
plt.axis([20000, 62000, 3, 10])
plt.show()

# Select a linear model
model = LinearRegression()

# Train the model
model.fit(x, y)

x_new = [[37655.2]] 
print(model.predict(x_new))

