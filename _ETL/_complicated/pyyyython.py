import pandas as pd
from sklearn.preprocessing import StandardScaler
import sqlalchemy as sa
import urllib as ur

df = pd.read_csv(r'D:\Programowanie\Workplace\Code\Data_Science_brick_by_brick\DataScienceSummerStudy\_ETL\_complicated\wine\wine.data', delimiter=',', header=None)
df.columns = ['Class', 'Alcohol', 'Malic acid', 'Ash', 'Alcalinity of ash', 'Magnesium', 'Total phenols', 'Flavanoids', 'Nonflavanoid phenols', 'Proanthocyanins', 'Color intensity', 'Hue', 'OD280/OD315 of diluted wines', 'Proline']
print(df.head())

scaler = StandardScaler()
# Normalizacja i standaryzacja
df[['Alcohol', 'Malic acid', 'Ash']] = scaler.fit_transform(df[['Alcohol', 'Malic acid', 'Ash']])
print(df.head())

# Agregacje i grupowania
grouped_df = df.groupby('Class').agg({'Alcohol': 'mean', 'Malic acid': 'mean', 'Ash': 'mean'})
print(grouped_df)

# Pivotowanie
pivot_df = df.pivot_table(index='Class', values='Alcohol', aggfunc='mean')
print(pivot_df)

connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=FIRSTONE;'
    'DATABASE=Nauka;'
    'Trusted_Connection=yes;'
)

params = ur.parse.quote_plus(connection_string)
engine = sa.create_engine(f'mssql+pyodbc:///?odbc_connect={params}')

df.to_sql('wine_data', engine, if_exists='replace', index=False)
df.to_csv(r'D:\Programowanie\Workplace\Code\Data_Science_brick_by_brick\DataScienceSummerStudy\_ETL\_complicated\transformed_wine_data.csv', index=False)