import pandas as pd
import sqlalchemy as sa
import urllib as ur

df = pd.read_excel('D:\Programowanie\Workplace\Code\Data_Science_brick_by_brick\DataScienceSummerStudy\_ETL\_simple\Data.xlsx')
df['FullName'] = df['FirstName'] + ' ' + df['LastName']
print(df)

connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=FIRSTONE;'
    'DATABASE=Nauka;'
    'Trusted_Connection=yes;'
)

params = ur.parse.quote_plus(connection_string)
print(params)

# Stwórz engine z SQLAlchemy
engine = sa.create_engine(f'mssql+pyodbc:///?odbc_connect={params}')

df.to_sql(name='DimEmployee', con=engine, index=False, if_exists='fail')



