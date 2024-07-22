import requests
import pandas as pd

# URL API
url = 'https://api.github.com/repos/pandas-dev/pandas/issues'

# Uwierzytelnienie
headers = {
    'Authorization': 'token YOUR_GITHUB_TOKEN'
}

# Wysyłanie zapytania GET do API
response = requests.get(url, headers=headers)

# Sprawdzenie statusu odpowiedzi
if response.status_code == 200:
    # Konwersja danych JSON na DataFrame
    data = response.json()
    df = pd.DataFrame(data)
    print('Pomyślnie pobrano dane!')
    print(df.head())
else:
    print('Błąd w pobieraniu danych:', response.status_code)
