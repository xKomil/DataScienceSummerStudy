Ten projekt służy do pobierania i analizowania danych pogodowych z wykorzystaniem biblioteki meteostat. Aplikacja umożliwia użytkownikowi wybór miasta oraz okresu czasu, a następnie pobiera dane pogodowe, agreguje je do danych tygodniowych i wyświetla w aplikacji Streamlit.

## Wymagania
Aby uruchomić aplikację, należy zainstalować następujące biblioteki:
- pandas
- meteostat
- streamlit
- streamlit-folium
- folium

Można zainstalować wymagane zależności za pomocą pip:
pip install pandas meteostat streamlit streamlit-folium folium

## Uruchomienie aplikacji

W terminalu należy uruchomić kod za pomocą tego polecenia:
streamlit run app.py

## Odpowiedzi na pytania:
1. Które zmienne z przedstawianych przez meteostat w Twojej opinii są ważne w kontekście predykcji sprzedaży wody gazowanej?
Zmienne takie jak średnia temperatura, maksymalna, oraz minimalna - większa sprzedaż w cieplejsze dni.
Opady mogą wpływać na wyjścia ludzi z domu a tym samym na zakupy.
Ciśnienie może wpływać na samopoczucie i tym samym wyjścia z domu i na zakupy.

2. Jakie statystyki agregaty (np. średnia) z danych dziennych warto by wykorzystać także do przeprowadzenia analizy na danych tygodniowych?
- średnia wartośc dla temperatury, ciśnienia, predkości wiatru
- Suma opadów
- max i min dla temperatury

3. Jak poradzić z pojedynczymi brakami danych dla poszczególnych zmiennych?
Można użyc średniej z pewnego okresu, użycie mediany, lub wartości z pobliskich dni

4. Czy warto brać pod uwagę zmienne pogodowe z dużą liczbą braków danych?
Nie warto, ponieważ może to dodać szumu do analizy, a później modelu predykcyjnego

5. Które dodaktowe zmienne sezonowe (oprócz pogodowych, np. pora roku) warto uwzględnić, starając się wyjaśnić zmienność sprzedaży wody gazowanej?
- pory roku
- dnia tygodnia czyli weekend a dni robocze
