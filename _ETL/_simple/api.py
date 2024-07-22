import requests
import pandas as pd

url = 'https://jsonplaceholder.typicode.com/posts'
response = requests.get(url)

if response.status_code == 200:
    print('Pomyślnie pobrano dane!')
else:
    print('Błąd w pobieraniu danych:', response.status_code)

data = response.json()
df = pd.DataFrame(data)

# Wyświetlenie pierwszych kilku wierszy DataFrame
print(df.head())
